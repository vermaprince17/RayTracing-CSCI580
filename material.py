from abc import ABC, abstractmethod
import math, random
from studio import random_in_unit_sphere, Vec, Ray, dot, unit_vector

class Material(ABC):
    @abstractmethod
    def scatter(self, r_in, intersection_record, scatter_record):
        pass

class ScatterRecord:
    def __init__(self):
        self.is_specular = False
        self.attenuation = Vec(0.0,0.0,0.0)
        self.specular_ray = Ray(Vec(0.0, 0.0, 0.0), Vec(0.0, 0.0, 0.0))
        self.pdf_ptr = None


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo # The proportion of the incident light or radiation that is reflected by a surface

    def scatter(self, r_in, intersection_record, scatter_record):
        
        target_direction = intersection_record.normal + random_in_unit_sphere()
        scattered = Ray(intersection_record.position, target_direction)
        scatter_record.attenuation = self.albedo
        scatter_record.is_specular = False
        scatter_record.pdf_ptr = None
        scatter_record.specular_ray = scattered

        return True, scatter_record
    
    def __repr__(self) -> str:
        return f"Albedo: {self.albedo}"

class Metal(Material):
    def __init__(self, albedo, fuzz: float):
        self.albedo = albedo
        self.fuzz = min(fuzz, 1.0)

    def reflect(self, v, n):
        return v - (n * 2 * dot(v, n))

    def scatter(self, r_in, intersection_record, scatter_record):
        reflected = self.reflect(unit_vector(r_in.direction()), intersection_record.normal)
        scattered = Ray(intersection_record.position, reflected + random_in_unit_sphere() * self.fuzz)
        scatter_record.attenuation = self.albedo
        scatter_record.is_specular = True
        scatter_record.pdf_ptr = 0
        scatter_record.specular_ray = scattered

        return dot(intersection_record.normal, scattered.direction()) > 0, scatter_record
    
    def __repr__(self) -> str:
        return f"Albedo: {self.albedo} Fuzz: {self.fuzz}"


class Dielectric:
    def __init__(self, albedo=Vec(1.0, 1.0, 1.0),ref_idx=1.0):
        self.ref_idx = ref_idx
        self.albedo = albedo

    def reflect(self, v, n):
        return v - (n * 2 * dot(v, n))
    
    def refract(self, v, n, ni_over_nt):
        refracted = Vec(0.0, 0.0, 0.0)
        uv = unit_vector(v)
        dt = dot(uv, n)
        discrim = 1.0 - ni_over_nt**2 * (1 - dt**2)
        if discrim > 0:
            refracted = ni_over_nt * (uv - n * dt) - n * math.sqrt(discrim)
            return True, refracted
        else:
            return False, Vec(0.0,0.0,0.0)

    def schlick(self, cosine, ref_idx):
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0**2
        return r0 + (1 - r0) * ((1 - cosine)**5)
    
    def scatter(self, r_in, intersection_record, scatter_record):
        scatter_record.pdf_ptr = None
        scatter_record.attenuation = self.albedo
        scatter_record.is_specular = True
        
        outward_normal = None
        reflected = self.reflect(r_in.direction(), intersection_record.normal)

        if dot(r_in.direction(), intersection_record.normal) <= 0:
            outward_normal = intersection_record.normal
            ni_over_nt = 1.0 / self.ref_idx
            cosine = -dot(r_in.direction(), intersection_record.normal) / (r_in.direction().length())
            
        else:
            outward_normal = -intersection_record.normal
            ni_over_nt = self.ref_idx
            cosine = self.ref_idx * dot(r_in.direction(), intersection_record.normal) / (r_in.direction().length())
           

        refract_flag, refracted = self.refract(r_in.direction(), outward_normal, ni_over_nt)
        if refract_flag:
            reflect_prob = self.schlick(cosine, self.ref_idx)
        else:
            reflect_prob = 1.0

        if random.uniform(0,1) < reflect_prob:
            scatter_record.specular_ray = Ray(intersection_record.position, reflected)
        else:
            scatter_record.specular_ray = Ray(intersection_record.position, refracted)

        return True, scatter_record
