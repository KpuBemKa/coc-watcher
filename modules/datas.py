from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    max_dX: int = 0
    max_dY: int = 0


@dataclass
class Color:
    b: int
    g: int
    r: int

    # Method to create a Color instance from a BGR tuple
    @classmethod
    def from_tuple(cls, bgr_tuple: tuple[int, int, int]) -> "Color":
        return cls(bgr_tuple[0], bgr_tuple[1], bgr_tuple[2])

    # Method to convert the Color instance to a BGR tuple
    def to_tuple(self) -> tuple[int, int, int]:
        return (self.b, self.g, self.r)

    def is_similar(self, other: "Color", tolerance=5) -> bool:
        def in_range(channel1, channel2, tolerance):
            """
            Checks if channel2 value falls in the [channel1 - tolerance; channel1 + tolerance] range
            """
            return (channel1 - tolerance) <= channel2 <= (channel1 + tolerance)

        return (
            in_range(self.b, other.b, tolerance)
            and in_range(self.g, other.g, tolerance)
            and in_range(self.r, other.r, tolerance)
        )
