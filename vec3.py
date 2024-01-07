from __future__ import annotations
from typing import Self, TypeAlias, Any
import random
import math


class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, v: Any) -> bool:
        if isinstance(v, Vec3):
            return self.x == v.x and self.y == v.y and self.z == v.z
        return False

    def __ge__(self, v: Self | float) -> bool:
        if isinstance(v, Vec3):
            return self.x >= v.x and self.y >= v.y and self.z >= v.z
        return self.x >= v and self.y >= v and self.z >= v

    def __gt__(self, v: Self | float) -> bool:
        if isinstance(v, Vec3):
            return self.x > v.x and self.y > v.y and self.z > v.z
        return self.x > v and self.y > v and self.z > v

    def __le__(self, v: Self | float) -> bool:
        if isinstance(v, Vec3):
            return self.x <= v.x and self.y <= v.y and self.z <= v.z
        return self.x <= v and self.y <= v and self.z <= v

    def __lt__(self, v: Self | float) -> bool:
        if isinstance(v, Vec3):
            return self.x < v.x and self.y < v.y and self.z < v.z
        return self.x < v and self.y < v and self.z < v

    def __add__(self, v: Self | float) -> Vec3:
        if isinstance(v, Vec3):
            return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)
        elif isinstance(v, float | int):
            return Vec3(self.x + v, self.y + v, self.z + v)
        raise NotImplementedError

    def __radd__(self, v):
        return Vec3(v + self.x, v + self.y, v + self.z)

    def __sub__(self, v: Self | float) -> Vec3:
        if isinstance(v, Vec3):
            return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)
        elif isinstance(v, float | int):
            return Vec3(self.x - v, self.y - v, self.z - v)
        raise NotImplementedError

    def __rsub__(self, v: float) -> Vec3:
        return Vec3(v - self.x, v - self.y - v, v - self.z)

    def __mul__(self, v: Self | float) -> Vec3:
        if isinstance(v, Vec3):
            return Vec3(self.x * v.x, self.y * v.y, self.z * v.z)
        if isinstance(v, float | int):
            return Vec3(self.x * v, self.y * v, self.z * v)
        raise NotImplementedError

    def __rmul__(self, v: float) -> Vec3:
        return Vec3(self.x * v, self.y * v, self.z * v)

    def __truediv__(self, v: Self | float) -> Vec3:
        if isinstance(v, Vec3):
            return Vec3(self.x * (1 / v.x), self.y * (1 / v.y), self.z * (1 / v.z))
        elif isinstance(v, float | int):
            return Vec3(self.x * (1 / v), self.y * (1 / v), self.z * (1 / v))

    def __rtruediv__(self, v: float):
        return Vec3(self.x * (1 / v), self.y * (1 / v), self.z * (1 / v))

    def __neg__(self) -> Vec3:
        return Vec3(-self.x, -self.y, -self.z)

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def near_zero(self) -> bool:
        s = 1e-8
        return math.fabs(self.x) < s and math.fabs(self.y) < s and math.fabs(self.z) < s


def unit_vector(v) -> Vec3:
    return v / v.length()


def random_vector(min_value: float = 0, max_value: float = 1) -> Vec3:
    return Vec3(
        random.uniform(min_value, max_value),
        random.uniform(min_value, max_value),
        random.uniform(min_value, max_value),
    )


def random_in_unit_sphere() -> Vec3:
    while True:
        p = random_vector(-1, 1)
        if p.length_squared() < 1:
            return p


def random_unit_vector() -> Vec3:
    return unit_vector(random_in_unit_sphere())


def random_on_hemisphere(normal: Vec3) -> Vec3:
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere
    return -on_unit_sphere


def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2 * dot(v, n) * n


def refract(uv: Vec3, n: Vec3, etai_over_etat: float) -> Vec3:
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(math.fabs(1.0 - r_out_perp.length_squared())) * n
    return r_out_perp + r_out_parallel


def dot(a: Vec3, b: Vec3) -> float:
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a: Vec3, b: Vec3) -> Vec3:
    return Vec3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)


Point3: TypeAlias = Vec3
