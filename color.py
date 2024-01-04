from vec3 import Vec3
from typing import TypeAlias


Color: TypeAlias = Vec3


def get_color(color: Color) -> str:
    return "{r} {g} {b}\n".format(
        r=int(255.999 * color.x),
        g=int(255.999 * color.y),
        b=int(255.999 * color.z),
    )
