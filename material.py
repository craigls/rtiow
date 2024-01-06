from abc import ABC, abstractmethod
from ray import Ray
from hittable import HitRecord
from color import Color
from vec3 import random_unit_vector, reflect, unit_vector, Vec3


class Material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered) -> bool:
        pass


class Lambertian(Material):
    albedo: Color

    def __init__(self, a: Color) -> None:
        self.albedo = a

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> bool:
        scatter_dir = rec.normal + random_unit_vector()
        # Correct scatter if close to zero
        if scatter_dir.near_zero():
            scatter_dir = rec.normal

        temp_r = Ray(rec.p, scatter_dir)
        scattered.direction = temp_r.direction
        scattered.origin = temp_r.origin
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z

        return True


class Metal(Material):
    albedo: Color

    def __init__(self, a: Color) -> None:
        self.albedo = a

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> bool:
        reflected: Vec3 = reflect(unit_vector(r_in.direction), rec.normal)
        temp_r = Ray(rec.p, reflected)
        scattered.origin = temp_r.origin
        scattered.direction = temp_r.direction
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True
