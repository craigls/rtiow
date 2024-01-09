from ray import Ray
from hittable import Hittable, HitRecord
from color import Color, get_color
from vec3 import unit_vector, random_in_unit_disk, cross, Vec3, Point3
from interval import Interval
from typing import Generator, Tuple
import math
import random
from utils import degrees_to_radians


class Camera:
    image_width: int = 100
    image_height: int
    aspect_ratio: float = 1.0
    view_height: float
    view_width: float
    center: Point3
    view_u: Vec3
    view_v: Vec3
    px_delta_u: Vec3
    px_delta_v: Vec3
    view_upper_left: Vec3
    px00_loc: Vec3
    max_depth: int = 50
    samples_per_pixel: int = 100
    vfov: float = 90
    lookfrom: Point3 = Point3(0, 0, -1)
    lookat: Point3 = Point3(0, 0, 0)
    vup: Vec3 = Vec3(0, 1, 0)
    u: Vec3
    v: Vec3
    w: Vec3
    defocus_angle: float = 0
    focus_dist: float = 10
    defocus_disk_v: Vec3
    defocus_disk_u: Vec3

    def setup(self) -> None:
        # Force image height to be at least 1
        self.image_height = int(self.image_width / self.aspect_ratio) or 1

        # Determine viewport dimensions
        theta = degrees_to_radians(self.vfov)
        h = math.tan(theta / 2)

        self.view_height = 2 * h * self.focus_dist
        self.view_width = self.view_height * (self.image_width / self.image_height)
        self.center = self.lookfrom

        # Calculate u, v, w unit basis vectors for the camera coordinate frame
        self.w = unit_vector(self.lookfrom - self.lookat)
        self.u = unit_vector(cross(self.vup, self.w))
        self.v = cross(self.w, self.u)

        # Calculate vectors accross horizontal and down the vertical edges
        self.view_u = self.view_width * self.u
        self.view_v = self.view_height * -self.v

        # Horizontal and vertical delta vectors between pixels
        self.px_delta_u = self.view_u / self.image_width
        self.px_delta_v = self.view_v / self.image_height

        # Upper left pixel
        self.view_upper_left = (
            self.center - (self.focus_dist * self.w) - self.view_u / 2 - self.view_v / 2
        )

        self.px00_loc = self.view_upper_left + 0.5 * (self.px_delta_u + self.px_delta_v)

        # Camera defocus disk basis vectors
        defocus_radius = self.focus_dist * math.tan(
            degrees_to_radians(self.defocus_angle / 2)
        )
        self.defocus_disk_u = self.u * defocus_radius
        self.defocus_disk_v = self.v * defocus_radius

    def pixel_sample_square(self) -> Vec3:
        px = -0.5 + random.random()
        py = -0.5 + random.random()
        return (px * self.px_delta_u) + (py * self.px_delta_u)

    def get_ray(self, i: int, j: int) -> Ray:
        px_center = self.px00_loc + (i * self.px_delta_u) + (j * self.px_delta_v)
        px_sample = px_center + self.pixel_sample_square()
        ray_origin = (
            self.defocus_disk_sample() if self.defocus_angle > 0 else self.center
        )
        ray_direction = px_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    def render(
        self, world: Hittable
    ) -> Generator[Tuple[float, float, float], None, None]:
        for j in range(self.image_height):
            print(f"Scanlines remaining: {(self.image_height - 1) - j} ", end="\r")
            for i in range(self.image_width):
                px_color = Color(0, 0, 0)
                # Apply anti-aliasing
                for _ in range(self.samples_per_pixel):
                    r = self.get_ray(i, j)
                    px_color += self.ray_color(r, self.max_depth, world)
                yield get_color(px_color, self.samples_per_pixel)

    def ray_color(self, r: Ray, depth: int, world: Hittable) -> Color:
        if depth <= 0:
            return Color(0, 0, 0)
        rec = HitRecord()

        if world.hit(r, Interval(0.001, float("inf")), rec):
            scattered = Ray()
            attenuation = Color()
            if rec.mat.scatter(r, rec, attenuation, scattered):
                return attenuation * self.ray_color(scattered, depth - 1, world)
            return Color(0, 0, 0)

        unit_direction = unit_vector(r.direction)
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)

    def defocus_disk_sample(self) -> Point3:
        p = random_in_unit_disk()
        return self.center + (p.x * self.defocus_disk_u) + (p.y * self.defocus_disk_v)
