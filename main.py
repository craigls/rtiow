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
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    cam: Camera = Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.setup()

    with open(sys.argv[1], "w") as f:
        # ppm header
        f.write(f"P3\n{cam.image_width} {cam.image_height}\n255\n")
        for px in cam.render(world):
            f.write(f"{px[0]} {px[1]} {px[2]}\n")


if __name__ == "__main__":
    main()
