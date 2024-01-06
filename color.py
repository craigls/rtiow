from vec3 import Vec3
from typing import TypeAlias
from interval import Interval
from typing import Tuple

Color: TypeAlias = Vec3


def get_color(color: Color, samples_per_pixel) -> Tuple[float, float, float]:
    intensity = Interval(0.000, 0.999)
    scale = 1.0 / samples_per_pixel
    r = color.x * scale
    g = color.y * scale
    b = color.z * scale

    return (
        int(255 * intensity.clamp(r)),
        int(255 * intensity.clamp(g)),
        int(255 * intensity.clamp(b)),
    )
