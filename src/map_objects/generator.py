import numpy as np
import random

from collections import OrderedDict, namedtuple
from dataclasses import dataclass
from typing import List
from loguru import logger

from map_objects.dungeon import Dungeon
from map_objects.enums import Direction
from map_objects.point import Point
from map_objects.tile import Tile, TileType


class Room:
    """
    Args:
        x- and y-coordinate of the top left corner of the room
        width and height of the room

    Attributes:
        x, y: top left coordinate in the 2d array
        width: number of tiles the room spans
        height: number of tiles the room spans
        region: number corresponding to region, used for connecting locations
        connections: list of regions room is connected to
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.region: int = None
        self.connections: list = []

    def __iter__(self):
        for i in range(self.height):
            for j in range(self.width):
                yield Point(x=self.x + j, y=self.y + i)

    @property
    def top_left(self) -> Point:
        return Point(self.x, self.y)

    @property
    def top_right(self) -> Point:
        return Point(self.x + self.width - 1, self.y)

    @property
    def bottom_left(self) -> Point:
        return Point(self.x, self.y + self.height - 1)

    @property
    def bottom_right(self) -> Point:
        return Point(self.x + self.width - 1, self.y + self.height - 1)

    @property
    def right(self) -> int:
        return self.x + self.width - 1

    @property
    def bottom(self) -> int:
        return self.y + self.height - 1


class DungeonGenerator:
    def __init__(self, map_settings: dict):

        self.dungeon = Dungeon(map_settings["map_height"], map_settings["map_width"])

        self.current_region: int = -1

        self.rooms: list = []
        self.corridors: list = []
        self.regions = OrderedDict({"count": 0})

        self.map_settings = OrderedDict(map_settings)
        self.winding_percent: int = 20

        self.seed = None

    def __iter__(self):
        # TODO: replace by property self.tile_map
        for x, y, grids in self.dungeon.tile_map:
            yield x, y, Tile.from_grid(Point(x, y), grids)

    @property
    def tile_map(self):
        for point, grids in self.dungeon:
            yield point, Tile.from_grid(point, grids)

    @property
    def max_rooms(self):
        return self.map_settings["num_rooms"]

    def new_region(self) -> int:
        """
        increases current_region by 1 and then returns current_region
        """
        self.current_region += 1
        return self.current_region

    # TODO: remove if not needed
    # def display(self):
    #     """
    #     iterator that begins at bottom left of the dungeon to display properly
    #     :rtype: List[int, int, Tile]
    #     """
    #     for i in range(self.height - 1, 0, -1):
    #         for j in range(self.width):
    #             # yield i, j - 1, self.grid[i][j - 1]
    #             yield j, i, self.dungeon.tile(Point(j, i))

    def initialize_map(self):
        for y in self.dungeon.rows:
            for x in self.dungeon.columns:
                self.dungeon.place(Point(x, y), Tile.wall(Point(x, y)), region=-1)

    # TODO: refactor self.tile to take Point
    def tile(self, x: int, y: int) -> Tile:
        """

        :param x: x-coordinate of tile
        :type x: int
        :param y: y-coordinate of tile
        :type y: int
        :return: Tile at coordinate (x, y)
        :rtype: Tile
        """

        grids = self.dungeon.grids(Point(x, y))
        tile = Tile.from_grid(Point(x, y), grids)

        return tile

    # TODO: replace start_x and start_y with Point variable
    def place_room(
        self,
        start_x: int,
        start_y: int,
        room_width: int,
        room_height: int,
        margin: int,
        ignore_overlap: bool = False,
    ):
        """

        :param start_x: 
        :type start_x: int
        :param start_y: 
        :type start_y: int
        :param room_width: 
        :type room_width: int
        :param room_height: 
        :type room_height: int
        :param margin: 
        :type margin: int
        :param ignore_overlap: 
        :type ignore_overlap: bool
        """
        room = Room(start_x, start_y, room_width, room_height)
        if self.room_fits(room, margin) or ignore_overlap:
            region = self.new_region()
            room.region = region
            for point in room:

                tile = Tile.floor(point)
                self.dungeon.place(point, tile, region)

            self.rooms.append(room)

    def place_random_rooms(
        self,
        min_room_size: int,
        max_room_size: int,
        room_step: int = 2,
        margin: int = None,
        attempts: int = 1000,
    ):
        """

        :param min_room_size: minimum number of tiles
        :type min_room_size: int
        :param max_room_size: 
        :type max_room_size: int
        :param room_step: 
        :type room_step: int
        :param margin: 
        :type margin: int
        :param attempts: number of times 
        :type attempts: int
        """
        if margin is None:
            margin = self.map_settings["room_margin"]
        for _ in range(attempts):
            if len(self.rooms) >= self.max_rooms:
                break
            room_width = random.randrange(min_room_size, max_room_size, room_step)
            room_height = random.randrange(min_room_size, max_room_size, room_step)
            start_point = self.random_point()
            self.place_room(
                start_point.x, start_point.y, room_width, room_height, margin
            )

    def room_fits(self, room: Room, margin: int) -> bool:
        """

        :param room: 
        :type room: Room
        :param margin: 
        :type margin: int
        :return: 
        :rtype: bool
        """
        mar_room = Room(
            (room.x - margin),
            (room.y - margin),
            (room.width + margin * 2),
            (room.height + margin * 2),
        )

        if (
            mar_room.x + mar_room.width < self.width
            and mar_room.y + mar_room.height < self.height
            and mar_room.x >= 0
            and mar_room.y >= 0
        ):
            for x, y in mar_room:
                tile = self.tile(x, y)
                if tile.label is not TileType.WALL:
                    return False

            return True
        return False

    def grow_maze(self, start: Point, label: TileType = None):
        """

        :param start:
        :type start: Point
        :param label:
        :type label: map_objects.tile.TileType
        """

        if label is None:
            label = TileType.CORRIDOR
        tiles = []  # tiles to check
        last_direction = Point(0, 0)

        region = self.new_region()
        self.place_tile(start, region=region, label=label)

        tiles.append(start)
        while len(tiles) > 0:
            tile = tiles.pop(-1)  # grab last tile

            # see which neighboring tiles can be carved
            open_tiles = []
            for d in Direction.cardinal():
                if self.can_place(tile, d):
                    # print("True")
                    open_tiles.append(d)
                # else:
                # print("False")

            if len(open_tiles) > 0:

                if (
                    last_direction in open_tiles
                    and random.randint(1, 101) > self.winding_percent
                ):
                    current_direction = last_direction
                else:
                    # TODO: refactor for random.choice()
                    current_direction = open_tiles[
                        random.randint(0, len(open_tiles) - 1)
                    ]

                self.place_tile(tile + current_direction, region=region, label=label)
                self.corridors.append(tile + current_direction)
                self.place_tile(tile + current_direction * 2, region=region, label=label)
                self.corridors.append(tile + current_direction * 2)

                tiles.append(tile + current_direction * 2)
                last_direction = current_direction
            else:
                # end current path
                last_direction = None

    def find_neighbors(self, point: Point, neighbors: Direction = None):
        """

        used by find_direct_neighbors
        :param point:
        :type point: Point
        :param neighbors: direction for neighbors to check, defaults to None
        :type neighbors: Direction
        :return yields new point in direction(s) chosen
        """
        if neighbors is None:
            neighbors = Direction.every()
        for direction in neighbors:
            new_point = point + direction
            if not self.dungeon.in_bounds(new_point):
                continue
            yield new_point

    def find_direct_neighbors(self, point: Point):
        """
        used by possible_moves
        :param point:
        :type point:
        :return:
        :rtype:
        """
        return self.find_neighbors(point, neighbors=Direction.cardinal())

    def clear_map(self):
        """
        Clears map by setting rooms to an empty list and calling dungeon.clear_dungeon()
        """
        self.rooms = []

        self.dungeon.clear_dungeon()

    def can_carve(self, pos: Point, direction: Point) -> bool:

        if pos is None:
            print("pos in can_carve() sent as None")
            return False

        xs = (1, 0, -1) if direction.x == 0 else (1 * direction.x, 2 * direction.x)
        ys = (1, 0, -1) if direction.y == 0 else (1 * direction.y, 2 * direction.y)

        for x in xs:
            for y in ys:
                if self.width <= pos.x + x or self.height <= pos.y + y:
                    return False
                tile = self.tile(pos.x + x, pos.y + y)
                if tile.label != TileType.WALL:
                    return False
        return True

    def carve(self, point: Point, region: int, label: TileType = TileType.FLOOR):

        tile = Tile.from_label(point, label)
        self.dungeon.place(point, tile, region)

    def build_corridors(self, start_point: Point = None):
        cells = []
        if start_point is None:
            start_point = Point(
                x=random.randint(1, self.width - 2),
                y=random.randint(1, self.height - 2),
            )
            # TODO: refactor can_carve
        attempts = 0
        while not self.can_carve(start_point, Direction.self()):
            attempts += 1
            start_point = Point(
                x=random.randint(1, self.width - 2),
                y=random.randint(1, self.height - 2),
            )
            # TODO: need to remove this hard stop once everything is combined
            if attempts > 100:
                break

        self.carve(point=start_point, region=self.new_region(), label=TileType.CORRIDOR)
        # add point to corridor list
        self.corridors.append(start_point)
        # add point to open cell list
        cells.append(start_point)

        while cells:
            middle = len(cells) // 2
            start_point = cells[-1]
            possible_moves = self.possible_moves(start_point)
            if possible_moves:
                point = random.choice(possible_moves)
                self.carve(
                    point=point, region=self.current_region, label=TileType.CORRIDOR
                )
                self.corridors.append(point)
                cells.append(point)
            else:
                cells.remove(start_point)

    def possible_moves(self, pos: Point) -> List[Point]:
        """
        searches for directions that a corridor can expand
        used by build_corridors()
        :param pos: index of tile in grid to find possible moves
        :type pos: Point
        :return: list of potential points the path could move
        :rtype: List[Point]
        """
        # logger.debug(f"inside possible_moves {pos}")
        available_squares = []
        for direction in Direction.cardinal():
            # logger.debug(f"direction = {direction}")
            neighbor = pos + direction
            # logger.debug(f"neighbor = {neighbor}")
            if (
                neighbor.x < 1
                or self.width - 2 < neighbor.x
                or neighbor.y < 1
                or self.height - 2 < neighbor.y
            ):
                # logger.debug(f"{neighbor} not in bounds")
                continue
            if self.can_carve(pos, direction):
                # logger.debug(f"can_carve returned True pos={pos}, direction={direction}")
                available_squares.append(neighbor)
        # logger.debug(f"available squares:")
        # for square in available_squares:
        # logger.debug(f"square={square}")
        # logger.add("debug.log")
        return available_squares

    @property
    def width(self) -> int:
        return self.map_settings["map_width"]

    @property
    def height(self) -> int:
        return self.map_settings["map_height"]

    def random_point(self) -> Point:
        return Point(
            x=random.randint(0, self.dungeon.width),
            y=random.randint(0, self.dungeon.height),
        )

    def build_dungeon(self):
        self.initialize_map()
        self.place_random_rooms(
            min_room_size=self.map_settings["min_room_size"],
            max_room_size=self.map_settings["max_room_size"],
        )

        # start_point = self.find_empty_space(3)
        # while start_point != Point(-1, -1):
        #     self.build_corridors(start_point)
        #     start_point = self.find_empty_space(3)

        for y in range(1, self.height, 2):
            for x in range(1, self.width, 2):
                point = Point(x, y)
                if self.dungeon.label(point) != TileType.WALL.value:
                    continue
                self.grow_maze(point)

    def find_empty_space(self, distance: int) -> Point:
        for x in range(distance, self.width - distance):
            for y in range(distance, self.height - distance):
                touching = 0
                for xi in range(-distance, distance):
                    for yi in range(-distance, distance):
                        if self.dungeon.label(Point(x + xi, y + yi)):
                            touching += 1
                if touching == 0:
                    print(f"returning {Point(x, y)}")
                    return Point(x, y)
        print("returning no point")
        return Point(-1, -1)

    def build_maze(self, label: TileType = None):
        """
        build maze using modified growing tree algorithm
        :param label:
        :type label:
        :return: None
        """
        if label is None:
            label = TileType.CORRIDOR

        tiles = []  # tiles to check

        for y in range(1, self.height, 2):
            for x in range(1, self.width, 2):
                point = Point(x, y)
                if self.dungeon.label(point) != TileType.WALL.value:
                    continue

                #############################
                # maze algorithm
                #############################

                self.place_maze(point)

    def place_maze(self, start_point: Point, label: TileType = TileType.CORRIDOR):
        points_to_check = []  # tiles to check
        last_direction = Point(0, 0)
        region = None

        # place corridor tile at starting point
        if self.can_place(start_point, Point(0, 0)):
            region = self.new_region()
            self.place_tile(start_point, label, region)
            points_to_check.append(start_point)

        while len(points_to_check) > 0:
            current_point = points_to_check.pop(-1)  # grab last point added

            # search neighbors for points that can be carved
            open_points = []
            for d in Direction.cardinal():
                if self.can_place(current_point, d):
                    open_points.append(d)


    def place_tile(self, point: Point, label: TileType, region: int):
        tile = Tile.from_label(point, label)
        assert self.current_region == region

    def can_place(self, point: Point, direction: Point) -> bool:
        x, y = point

        SliceBounds = namedtuple("SliceBounds", ["x1", "x2", "y1", "y2"])

        bounds = {
            Point(0, 0): SliceBounds(x1=point.x - 1, x2=point.x + 1, y1=point.y - 1, y2=point.y + 1),
            Point(0, 1): SliceBounds(x1=point.x - 1, x2=point.x + 1, y1=point.y + 1, y2=point.y + 2),
            Point(1, 0): SliceBounds(x1=point.x + 1, x2=point.x + 2, y1=point.y - 1, y2=point.y + 1),
            Point(-1, 0): SliceBounds(x1=point.x - 2, x2=point.x - 1, y1=point.y - 1, y2=point.y + 1),
            Point(0, -1): SliceBounds(x1=point.x - 1, x2=point.x + 1, y1=point.y - 2, y2=point.y - 1),
        }

        slices = {
            Point(0, 0): np.s_[x-1:x+1, y-1:y+1],
            Point(0, 1): np.s_[x-1:x+1, y+1:y+2],
            Point(0, -1): np.s_[x-1:x+1, y-2:y-1],
            Point(1, 0): np.s_[x+1:x+2, y-1:y+1],
            Point(-1, 0): np.s_[x-2:x-1, y-1:y+1]
        }

        x1, x2, y1, y2 = bounds[direction]

        if x1 < 0 or y1 < 0 or x2 > self.width or y2 > self.height:
            return False

        try:
            grid_slice = self.dungeon.label_grid[x1:x2, y1:y2]
            if grid_slice.max() != 0:
                return False
            else:
                return True
        except IndexError:
            return False
        except ValueError:
            return False
