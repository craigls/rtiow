"""
Ray Tracing in one weekend - Book 1 code
"""
import sys
import math
from ray import Ray
from sphere import Sphere
from vec3 import Vec3, Point3, dot, cross, unit_vector
from color import Color, get_color
from hittable import HittableList, Hittable, HitRecord
from interval import Interval
from material import Lambertian, Metal, Dielectric
from camera import Camera
import utils
import sys


def ray_color(r: Ray, world: HittableList) -> Color:
    rec = HitRecord()

    if world.hit(r, Interval(0, float("inf")), rec):
        return 0.5 * (rec.normal + Color(1, 1, 1))

    unit_direction = unit_vector(r.direction)
    a = 0.5 * unit_direction.y + 1.0
    return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)


def main() -> None:
    world: HittableList = HittableList()
    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left = Dielectric(1.5)
    material_right = Metal(Color(0.8, 0.6, 0.2), 0.0)

    world.add(Sphere(Point3(0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Point3(0.0, 0.0, -1.0), 0.5, material_center))
    world.add(Sphere(Point3(-1.0, 0.0, -1.0), 0.4, material_left))
    world.add(Sphere(Point3(1.0, 0.0, -1.0), 0.5, material_right))

    cam: Camera = Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 10
    cam.max_depth = 10
    cam.setup()

    if len(sys.argv) < 2:
        print("Error: Pass output .ppm file as argument")
        raise SystemExit(1)

    with open(sys.argv[1], "w") as f:
        # ppm header
        f.write(f"P3\n{cam.image_width} {cam.image_height}\n255\n")
        for px in cam.render(world):
            f.write(f"{px[0]} {px[1]} {px[2]}\n")


if __name__ == "__main__":
    main()
