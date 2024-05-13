from abc import ABC, abstractmethod
import math
from studio import dot

class IntersectionRecord:
    def __init__(self):
        self.t: float = 0.0
        self.position = None
        self.normal = None
        self.mat_ptr = None
    
    def __repr__(self) -> str:
        return f"t: {self.t}, position: {self.position}, normal: {self.normal}, material: {self.mat_ptr}"

# an object in the scene that ray can intersect.
class Intersection(ABC):
    @abstractmethod
    def intersect(self, r, t_min, t_max, rec):
        pass


class AssetLists(Intersection):
    def __init__(self, object_list=None):
        if object_list is None:
            self.object_list = []  # Initialize an empty list if no list is provided
        elif isinstance(object_list, list):
            self.object_list = object_list  # Use the provided list if it's already a list
        else:
            raise TypeError("object_list must be a list of Intersection objects or None")

    def add(self, obj):
        if not isinstance(obj, Intersection):
            raise TypeError("All items added must be instances of Intersection or its subclasses")
        self.object_list.append(obj)
    
    def intersect(self, r, t_min, t_max, rec):
        hit_anything = False
        closest_so_far = t_max
        temp_rec = IntersectionRecord()

        for i in range(len(self.object_list)):
            intersection_flag, rec = self.object_list[i].intersect(r, t_min, closest_so_far, temp_rec)
            if intersection_flag:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.t = temp_rec.t
                rec.position = temp_rec.position
                rec.normal = temp_rec.normal
                rec.mat_ptr = temp_rec.mat_ptr

        return hit_anything, rec


class Sphere(Intersection):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.mat_ptr = material

    def intersect(self, r, t_min, t_max, rec):
        # Vector from ray origin to sphere center
        oc = r.origin() - self.center
        a = dot(r.direction(), r.direction())
        b = dot(r.origin()-self.center , r.direction())
        c = dot(oc, oc) - self.radius*self.radius
        discriminant = (b*b - a*c)

        if discriminant > 0:
            sqrt_discriminant = math.sqrt(discriminant)
            # Find the nearest root that lies in the acceptable range
            temp = (-b - sqrt_discriminant) / (a)
            if t_min < temp < t_max:
                rec.t = temp
                rec.position = r.point_at_parameter(rec.t)
                rec.normal = (rec.position - self.center) / self.radius
                rec.mat_ptr = self.mat_ptr
                
                return True, rec

            temp = (-b + sqrt_discriminant) / (a)
            if t_min < temp < t_max:
                rec.t = temp
                rec.position = r.point_at_parameter(rec.t)
                rec.normal = (rec.position - self.center) / self.radius
                rec.mat_ptr = self.mat_ptr

                return True, rec

        
        return False, rec

    def __repr__(self) -> str:
        return f"Center: {self.center}, Radius: {self.radius}, Material: {self.material}"
