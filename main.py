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
import utils


def ray_color(r: Ray, world: Hittable) -> Color:
    rec = HitRecord()
    if world.hit(r, 0, math.inf, rec):
        return 0.5 * (rec.normal + Color(1, 1, 1))

    unit_direction = unit_vector(r.direction)
    a = 0.5 * unit_direction.y + 1.0
    return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)


def main() -> None:
    aspect_ratio = 16 / 9.0
    image_width = 400

    # Force image height to be at least 1
    image_height = int(400 / aspect_ratio) or 1

    # World
    world = HittableList()
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    # Camera
    focal_length = 1.0
    view_height = 2.0
    view_width = view_height * (image_width / image_height)
    camera_center = Point3(0, 0, 0)

    view_u = Vec3(view_width, 0, 0)
    view_v = Vec3(0, -view_height, 0)

    px_delta_u = view_u / image_width
    px_delta_v = view_v / image_height

    view_upper_left = camera_center - Vec3(0, 0, focal_length) - view_u / 2 - view_v / 2
    px00_loc = view_upper_left + 0.5 * (px_delta_u + px_delta_v)

    with open(sys.argv[1], "w") as f:
        # ppm header
        f.write(f"P3\n{image_width} {image_height}\n255\n")

        for j in range(image_height):
            print(f"Scanlines remaining: {(image_height - 1) - j}", end="\r")
            for i in range(image_width):
                px_center = px00_loc + (i * px_delta_u) + (j * px_delta_v)
                ray_direction = px_center - camera_center
                r = Ray(camera_center, ray_direction)
                px_color = ray_color(r, world)

                f.write(get_color(px_color))


if __name__ == "__main__":
    main()
