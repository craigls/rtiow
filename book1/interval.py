class Interval:
    min_value: float
    max_value: float

    def __init__(
        self, min_value: float = float("inf"), max_value: float = float("-inf")
    ):
        self.min_value = min_value
        self.max_value = max_value

    def contains(self, x: float) -> bool:
        return self.min_value <= x and x <= self.max_value

    def surrounds(self, x: float) -> bool:
        return self.min_value < x and x < self.max_value

    def clamp(self, x: float) -> float:
        if x < self.min_value:
            return self.min_value
        if x > self.max_value:
            return self.max_value
        return x


empty = Interval(float("inf"), float("-inf"))
universe = Interval(float("-inf"), float("inf"))
