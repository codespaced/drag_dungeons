from typing import Tuple

import numpy

from map_objects.enums import TileType
from map_objects.point import Point
from map_objects.tile import Tile


class Dungeon:
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width
        self.rooms = []

        self.grid_shape: Tuple[int, int] = (height, width)
        self.tile_grid = numpy.full(shape=self.grid_shape, fill_value=Tile.empty())
        self.region_grid = numpy.full(shape=self.grid_shape, fill_value=-1, dtype=numpy.int)
        self.fov_grid = numpy.zeros(shape=self.grid_shape)

    @property
    def rows(self):
        return range(self.height)

    @property
    def columns(self):
        return range(self.width)

    def __iter__(self):
        for row in self.rows:
            for col in self.columns:
                yield Point(col, row), self.tile_grid[row, col]

    def clear_dungeon(self):
        """
        Clears the dungeon data by filling the tile grid with empty tiles and region grid with -1
        """
        self.tile_grid = numpy.full(shape=self.grid_shape, fill_value=Tile.empty())
        self.region_grid = numpy.full(shape=self.grid_shape, fill_value=-1, dtype=int)

    def tile(self, point: Point) -> Tile:
        tile = Tile.empty()
        if not self.in_bounds(point):
            tile = Tile.empty(point)
        try:
            tile = self.tile_grid[point.y, point.x]
        except IndexError:
            print("index out of range")
        return tile

    def set_tile(self, point: Point, label: TileType):
        self.tile_grid[point.y, point.x] = Tile.from_label(point, label)

    def region(self, point: Point) -> int:
        return self.region_grid[point.y, point.x]

    def set_region(self, point: Point, region: int):
        self.region_grid[point.y, point.x] = region

    def in_bounds(self, pos: Point) -> bool:
        """
        Checks if position is within the boundaries of the dungeon
        :param pos: position to check
        :type pos: Point
        :return: True is pos is within boundaries of the dungeon
        :rtype: bool
        """
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height
