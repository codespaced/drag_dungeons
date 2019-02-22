from enum import Enum

from map_objects.point import Point


class CallableEnum(Enum):
    def __call__(self):
        return self.value


class Direction(CallableEnum):
    NW = Point(-1, 1)
    N = Point(0, 1)
    NE = Point(1, 1)
    W = Point(-1, 0)
    E = Point(1, 0)
    SW = Point(-1, -1)
    S = Point(0, -1)
    SE = Point(1, -1)

    @classmethod
    def cardinal(cls):
        """
        Yields Point for the cardinal directions (N, E, S, W)
        :return: generator object of Point for each cardinal directions
        """
        for direction in [cls.N, cls.E, cls.S, cls.W]:
            yield direction.value

    @classmethod
    def every(cls):
        for direction in cls:
            yield direction.value

    @staticmethod
    def self():
        return Point(0, 0)


class TileType(CallableEnum):
    WALL = (1, 1, 1, 1)
    FLOOR = (.5, .5, .5, 1)
    DOOR = (1, .5, .5, 1)
    CORRIDOR = (.7, .2, .7, 1)
    EMPTY = (.39, .8, .39, 1)
    BLUE = (0, 0, 1, 1)
    RED = (1, 0, 0, 1)
    YELLOW = (1, 1, 0, 1)

    def __str__(self):
        return str(self.name)
