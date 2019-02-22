from map_objects.enums import TileType
from map_objects.point import Point


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
        passable: if the tile is passable
    """

    def __init__(self, x: int, y: int, *, label: TileType = TileType.EMPTY, passable: bool = False):
        self.position: Point = Point(x, y)
        self.label: TileType = label
        self.passable: bool = passable

    def __str__(self):
        return f"Tile{self.position} = {self.label}, {self.passable}"

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
        if label is TileType.EMPTY:
            return Tile.empty(point)
        elif label is TileType.FLOOR:
            return Tile.floor(point)
        elif label is TileType.WALL:
            return Tile.wall(point)
        elif label is TileType.DOOR:
            return Tile.door(point)
        elif label is TileType.CORRIDOR:
            return Tile.corridor(point)

        return Tile.error(point)

    @property
    def tile_color(self) -> tuple:
        return self.label()

    @classmethod
    def empty(cls, point=Point(-1, -1)):
        """
        creates an empty Tile that is not passable
        :param point: x- and y-coordinates for the tile, defaults to -1, -1 if no point is provided
        :type point: Point
        :return: returns a tile at x and y of point with the label "EMPTY" and not passable
        :rtype Tile
        """
        return Tile(point.x, point.y, label=TileType.EMPTY, passable=False)

    @classmethod
    def floor(cls, point):
        """
        creates a floor Tile that is passable
        :param point: x- and y-coordinates for the tile
        :type point: Point
        :return: returns a tile at x and y of point with the label "FLOOR" and passable
        :rtype: Tile
        """
        return Tile(point.x, point.y, label=TileType.FLOOR, passable=True)

    @classmethod
    def corridor(cls, point):
        """
        creates a corridor Tile that is passable
        :param point: x- and y-coordinates for the tile
        :type point: Point
        :return: returns a tile at x and y of point with the label "CORRIDOR" and passable
        :rtype: Tile
        """
        return Tile(point.x, point.y, label=TileType.CORRIDOR, passable=True)

    @classmethod
    def wall(cls, point):
        """
        creates a wall Tile that is not passable
        :param point: x- and y-coordinates for the tile
        :type point: Point
        :return: returns a tile at x and y of point with the label "WALL" and not passable
        :rtype: Tile
        """
        return Tile(point.x, point.y, label=TileType.WALL, passable=False)

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
        return Tile(point.x, point.y, label=TileType.RED)
