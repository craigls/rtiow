from vec3 import Vec3, Point3, dot
from abc import ABC, abstractmethod
from ray import Ray
from interval import Interval
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
    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        pass


class HittableList(Hittable):
    objects: List[Hittable]
    temp_rec: HitRecord

    def __init__(self) -> None:
        self.objects = []
        self.temp_rec = HitRecord()

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = ray_t.max_value

        for object in self.objects:
            if object.hit(r, Interval(ray_t.min_value, closest_so_far), temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.front_face = temp_rec.front_face

        return hit_anything

    def add(self, h: Hittable):
        self.objects.append(h)

    def clear(self):
        self.objects = []
