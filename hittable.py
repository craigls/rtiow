from vec3 import Vec3, Point3, dot
from abc import ABC, abstractmethod
from ray import Ray
from typing import List, Any


class HitRecord:
    p: Point3
    normal: Vec3
    t: float
    front_face: bool

    def __init__(self) -> None:
        self.normal = Vec3()
        self.p = Point3()
        self.t = 0
        self.front_face = False

    def set_face_normal(self, r: Ray, outward_normal: Vec3) -> None:
        # Sets the hit record normal vector.
        # NOTE: the parameter `outward_normal` is assumed to have unit length.
        front_face = dot(r.direction, outward_normal) < 0
        self.normal = outward_normal if front_face else -outward_normal


class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, ray_tmin: float, ray_tmax: float, rec: HitRecord) -> bool:
        pass


class HittableList(Hittable):
    objects: List[Hittable] = []

    def hit(self, r: Ray, ray_tmin: float, ray_tmax: float, rec: HitRecord) -> bool:
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = ray_tmax

        for object in self.objects:
            if object.hit(r, ray_tmin, closest_so_far, rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec

        return hit_anything

    def add(self, h: Hittable):
        self.objects.append(h)

    def clear(self):
        self.objects = []
