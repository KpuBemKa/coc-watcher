from dataclasses import dataclass
from screeninfo import get_monitors


# @dataclass
class Position:
    def __init__(self, x: int, y: int, max_dX: int = 0, max_dY: int = 0):
        self.__x = x
        self.__y = y

        self.__max_dX = max_dX
        self.__max_dY = max_dY

        # top-left x position, top-left y position, width, height
        self.__bounding_box = (x - max_dX, y - max_dY, x + max_dX, y + max_dY)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def max_dX(self):
        return self.__max_dX

    @property
    def max_dY(self):
        return self.__max_dY

    def get_bounding_box(self):
        """Returns the X & Y coordinates of the top left corner of a box containing the positions described by this object

        Returns:
            tuple[int, int, int, int]: X coordinate of the top-left corner, Y coordinate of the top-left corner, box width, box height
        """
        return self.__bounding_box


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


def position_converter(source_res: tuple[int, int], position: Position):
    monitor = get_monitors()[0]
    width_ratio = monitor.width / source_res[0]
    height_ratio = monitor.height / source_res[1]

    return Position(
        int(position.x * width_ratio),
        int(position.y * height_ratio),
        int(position.max_dX * width_ratio),
        int(position.max_dY * height_ratio),
    )
