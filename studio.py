import math
import random

class Vec:
    def __init__(self, e0=0.0, e1=0.0, e2=0.0):
        self.e = [e0, e1, e2]

    @property
    def x(self):
        return self.e[0]
    @property
    def y(self):
        return self.e[1]
    @property
    def z(self):
        return self.e[2]
    @property
    def r(self):
        return self.e[0]
    @property
    def g(self):
        return self.e[1]
    @property
    def b(self):
        return self.e[2]

    def __pos__(self):
        return self

    def __neg__(self):
        return Vec(-self.e[0], -self.e[1], -self.e[2])

    def __getitem__(self, index):
        return self.e[index]

    def __setitem__(self, index, value):
        self.e[index] = value

    def __add__(self, other):
        if isinstance(other, Vec):
            return Vec(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec):
            return Vec(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])
        return NotImplemented

    def __iadd__(self, other):
        self.e[0] += other.e[0]
        self.e[1] += other.e[1]
        self.e[2] += other.e[2]
        return self

    def __isub__(self, other):
        self.e[0] -= other.e[0]
        self.e[1] -= other.e[1]
        self.e[2] -= other.e[2]
        return self

    def __imul__(self, other):
        if isinstance(other, Vec):
            self.e[0] *= other.e[0]
            self.e[1] *= other.e[1]
            self.e[2] *= other.e[2]
        else:
            self.e[0] *= other
            self.e[1] *= other
            self.e[2] *= other
        return self
    

    def __mul__(self, other):
        if isinstance(other, Vec):
            return Vec(self.e[0] * other.e[0], self.e[1] * other.e[1], self.e[2] * other.e[2])
        elif isinstance(other, (int, float)):  # Scalar multiplication
            return Vec(self.e[0] * other, self.e[1] * other, self.e[2] * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Vec):
            return Vec(self.e[0] / other.e[0], self.e[1] / other.e[1], self.e[2] / other.e[2])
        elif isinstance(other, (int, float)):  # Scalar division
            if other == 0:
                return Vec(self.e[0], self.e[1], self.e[2])
            inv = 1.0 / other
            return Vec(self.e[0] * inv, self.e[1] * inv, self.e[2] * inv)
        return NotImplemented

    def length(self):
        return math.sqrt(self.e[0] ** 2 + self.e[1] ** 2 + self.e[2] ** 2)

    def squared_length(self):
        return self.e[0] ** 2 + self.e[1] ** 2 + self.e[2] ** 2

    def make_unit_vector(self):
        k = 1.0 / self.length()
        self.e[0] *= k
        self.e[1] *= k
        self.e[2] *= k

    def __str__(self):
        return f"{self.e[0]} {self.e[1]} {self.e[2]}"


def dot(v1, v2):
    return v1.e[0] * v2.e[0] + v1.e[1] * v2.e[1] + v1.e[2] * v2.e[2]

def cross(v1, v2):
    return Vec(v1.e[1] * v2.e[2] - v1.e[2] * v2.e[1],
                    -(v1.e[0] * v2.e[2] - v1.e[2] * v2.e[0]),
                    v1.e[0] * v2.e[1] - v1.e[1] * v2.e[0])

def unit_vector(v):
        return v / v.length()

def random_in_unit_sphere():
    while True:
        p = (Vec(random.uniform(0, 10)/float(10), random.uniform(0, 10)/float(10), random.uniform(0, 10)/float(10)) * 2) - Vec(1, 1, 1)
        if dot(p, p) < 1:
            return p

class Ray:
    def __init__(self, origin=None, direction=None):
        if origin is None:
            origin = Vec(0, 0, 0)
        if direction is None:
            direction = Vec(0, 0, 0)
        self.A = origin
        self.B = direction

    def origin(self):
        return self.A

    def direction(self):
        return self.B

    def point_at_parameter(self, t):
        return self.A + t * self.B 
    
    def __repr__(self) -> str:
        return f"Origin: {self.A}, Direction: {self.B}"


class Camera:
    def __init__(self, origin=None, lower_left_corner=None, horizontal=None, vertical = None):
        if origin is None:
            origin = Vec(0.0, 0.0, 0.0)
        if lower_left_corner is None:
            lower_left_corner = Vec(-2.0, -1.0, -1.0)
        if horizontal is None:  
            horizontal = Vec(4.0, 0.0, 0.0)
        if vertical is None:
            vertical = Vec(0.0, 2.0, 0.0)
        
        self.lower_left_corner = lower_left_corner #reference point
        self.horizontal = horizontal #postive x direction
        self.vertical =  vertical#positive y direction
        self.origin = origin #camera position

    def get_ray_at_point(self, u, v):
        direction = self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin
        return Ray(self.origin, direction)

