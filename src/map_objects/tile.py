from dataclasses import dataclass
from enum import Enum
from typing import Dict

from map_objects.point import Point


class TileType(Enum):
    EMPTY = -1
    WALL = 0
    FLOOR = 1
    CORRIDOR = 2
    DOOR = 3

    CONNECTION = 100

    ERROR = 999

    def __str__(self):
        return str(self.name)


@dataclass()
class Tile:
    """
    An object to represent a single tile in the map's grid

    Args:
        x- and y-coordinate for the tile
        label for the tile
        passable or not

    Attributes:
        position: the Point in the grid
        label: label of the tile
        blocked:
        blocks_sight:
        passable: if the tile is passable
    """

    def __init__(
        self,
        x: int,
        y: int,
        *,
        label: TileType = TileType.EMPTY,
        blocked: bool = True,
        blocks_sight: bool = True,
        passable: bool = False,
    ):
        self.position: Point = Point(x, y)
        self.label: TileType = label
        self.blocked: bool = blocked
        self.blocks_sight: bool = blocks_sight
        self.passable: bool = passable

    def __str__(self):
        return f"{self.label.name} {self.position}"

    def __repr__(self):
        return f"({self.__class__.__name__}) x={self.x}, y={self.y}, label={self.label}, passable={self.passable}"

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    @staticmethod
    def from_label(point: Point, label: TileType):
        """
        creates a Tile from the label provided
        :param point: x- and y-coordinates for the tile
        :type point: Point
        :param label: label for the type of tile to be created
        :type label: TileType
        :return: returns a tile at x and y of point with the label provided
        :rtype: Tile
        """
        labels = {
            TileType.EMPTY: Tile.empty(point),
            TileType.FLOOR: Tile.floor(point),
            TileType.WALL: Tile.wall(point),
            TileType.CORRIDOR: Tile.corridor(point),
            TileType.DOOR: Tile.door(point)
        }

        tile = labels.get(label, Tile.error(point))

        if tile.label == TileType.ERROR:
            print(f"Tile.from_label returned Tile.error. point={point}, label={label}")

        return tile

    @classmethod
    def empty(cls, point=Point(-1, -1)):
        """
        creates an empty Tile that is not passable
        :param point: x- and y-coordinates for the tile, defaults to -1, -1 if no point is provided
        :type point: Point
        :return: returns a tile at x and y of point with the label "EMPTY" and not passable
        :rtype Tile
        """
        return Tile(point.x, point.y, label=TileType.EMPTY)

    @classmethod
    def floor(cls, point):
        """
        creates a floor Tile that is passable
        :param point: x- and y-coordinates for the tile
        :type point: Point
        :return: returns a tile at x and y of point with the label "FLOOR" and passable
        :rtype: Tile
        """
        return Tile(point.x, point.y, label=TileType.FLOOR, blocked=False, blocks_sight=False)

    @classmethod
    def corridor(cls, point):
        """
        creates a corridor Tile that is passable
        :param point: x- and y-coordinates for the tile
        :type point: Point
        :return: returns a tile at x and y of point with the label "CORRIDOR" and passable
        :rtype: Tile
        """
        return Tile(point.x, point.y, label=TileType.CORRIDOR, blocked=False, blocks_sight=False)

    @classmethod
    def wall(cls, point):
        """
        creates a wall Tile that is not passable
        :param point: x- and y-coordinates for the tile
        :type point: Point
        :return: returns a tile at x and y of point with the label "WALL" and not passable
        :rtype: Tile
        """
        return Tile(point.x, point.y, label=TileType.WALL, blocked=True, blocks_sight=True)

    @classmethod
    def door(cls, point):
        """
        creates a door Tile that is not passable
        :param point: x- and y-coordinates for the tile
        :type point: Point
        :return: returns a tile at x and y of point with the label "DOOR" and not passable
        :rtype Tile
        """
        return Tile(point.x, point.y, label=TileType.DOOR, passable=False)

    @classmethod
    def error(cls, point):
        return Tile(point.x, point.y, label=TileType.ERROR)

    @classmethod
    def from_grid(cls, point: Point, grids: Dict[str, int]):
        tile = Tile(
            x=point.x,
            y=point.y,
            label=TileType(grids["label"]),
            blocked=grids.get("blocked", True),
            blocks_sight=grids.get("blocks_sight", True),
        )

        return tile
