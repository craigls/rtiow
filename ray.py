from vec3 import Vec3, Point3


class Ray:
    origin: Point3
    direction: Vec3

    def __init__(
        self, origin: Point3 | None = None, direction: Vec3 | None = None
    ) -> None:
        self.origin = origin or Point3()
        self.direction = direction or Vec3()

    def at(self, t: float) -> Point3:
        return self.origin + self.direction * t
