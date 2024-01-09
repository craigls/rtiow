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
import random


def ray_color(r: Ray, world: HittableList) -> Color:
    rec = HitRecord()

    if world.hit(r, Interval(0, float("inf")), rec):
        return 0.5 * (rec.normal + Color(1, 1, 1))

    unit_direction = unit_vector(r.direction)
    a = 0.5 * unit_direction.y + 1.0
    return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)


def main() -> None:
    world = HittableList()
    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Point3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            sphere_material: Lambertian | Metal | Dielectric
            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = Color.random(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4, 1, 0), 1.0, material3))

    cam = Camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.vfov = 20
    cam.lookfrom = Point3(13, 2, 3)
    cam.lookat = Point3(0, 0, 0)
    cam.vup = Vec3(0, 1, 0)
    cam.defocus_angle = 0.6
    cam.focus_dist = 10.0
    cam.image_width = 800

    # Adjust for higher image quality
    cam.samples_per_pixel = 100
    cam.max_depth = 50

    # Configure camera w/above parameters
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
