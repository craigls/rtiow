import math
from hittable import Hittable, HitRecord
from vec3 import Vec3, Point3, dot
from ray import Ray
from interval import Interval
from material import Material


class Sphere(Hittable):
    center: Point3
    radius: float
    mat: Material

    def __init__(self, center: Point3, radius: float, mat: Material) -> None:
        self.center = center
        self.radius = radius
        self.mat = mat

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        oc = r.origin - self.center
        a = r.direction.length_squared()
        half_b = dot(oc, r.direction)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return False
        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (-half_b + sqrtd) / a
            if not ray_t.surrounds(root):
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.mat
        return True
