from vec3 import Vec3
from typing import TypeAlias
from interval import Interval
from typing import Tuple
import math

Color: TypeAlias = Vec3


def linear_to_gamma(n: float):
    return math.sqrt(n)


def get_color(color: Color, samples_per_pixel) -> Tuple[float, float, float]:
    intensity = Interval(0.000, 0.999)
    scale = 1.0 / samples_per_pixel
    r = linear_to_gamma(color.x * scale)
    g = linear_to_gamma(color.y * scale)
    b = linear_to_gamma(color.z * scale)

    return (
        int(255 * intensity.clamp(r)),
        int(255 * intensity.clamp(g)),
        int(255 * intensity.clamp(b)),
    )
