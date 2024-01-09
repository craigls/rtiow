from abc import ABC, abstractmethod
from ray import Ray
from hittable import HitRecord
from color import Color
from vec3 import random_unit_vector, reflect, refract, unit_vector, dot, Vec3
import math
import random


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

        scattered.direction = scatter_dir
        scattered.origin = rec.p
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z

        return True


class Metal(Material):
    albedo: Color
    fuzz: float

    def __init__(self, a: Color, f: float) -> None:
        self.albedo = a
        self.fuzz = f if f < 1 else 1

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> bool:
        reflected: Vec3 = reflect(unit_vector(r_in.direction), rec.normal)
        scattered.direction = reflected + self.fuzz * random_unit_vector()
        scattered.origin = rec.p
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return dot(scattered.direction, rec.normal) > 0


class Dielectric(Material):
    index_of_refraction: float

    def __init__(self, index_of_refraction: float) -> None:
        self.ir = index_of_refraction

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> bool:
        attenuation.x = 1.0
        attenuation.y = 1.0
        attenuation.z = 1.0

        refraction_ratio = (1.0 / self.ir) if rec.front_face else self.ir
        unit_direction = unit_vector(r_in.direction)

        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = math.sqrt(max(0.0, 1.0 - cos_theta * cos_theta))

        cannot_refract = refraction_ratio * sin_theta > 1.0
        if cannot_refract or reflectance(cos_theta, refraction_ratio) > random.random():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, refraction_ratio)

        scattered.direction = direction
        scattered.origin = rec.p
        return True


def reflectance(cosine: float, ref_idx: float) -> float:
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0) * math.pow((1 - cosine), 5)
