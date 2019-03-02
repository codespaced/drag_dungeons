from bearlibterminal import terminal

from map_objects.dungeon import Dungeon
from map_objects.enums import Direction
from map_objects.generator import DungeonGenerator
import random
import const as c
from map_objects.tile import TileType
from map_objects.point import Point
import numpy as np
import time


WHITE = terminal.color_from_name("white")
BLUE = terminal.color_from_name("blue")
YELLOW = terminal.color_from_name("yellow")
RED = terminal.color_from_name("red")

MAP_SETTINGS = {
    "map_height": 21,
    "map_width": 31,
    "tile_size": 10,
    "num_rooms": 100,
    "min_room_size": 3,
    "max_room_size": 7,
    "room_margin": 1,
}


def display_map(dungeon, testing_grid):
    for point, tile in dungeon.tile_map:
        terminal.color(terminal.color_from_name("white"))
        ch = c.Tiles.UNSEEN
        if tile.label == TileType.WALL:
            ch = c.Tiles.WALL
        elif tile.label == TileType.FLOOR:
            ch = c.Tiles.FLOOR
        elif tile.label == TileType.CORRIDOR:
            ch = c.Tiles.CORRIDOR

        terminal.layer(c.Layers.MAP)
        terminal.put(point.x, point.y, ch)

        if testing_grid[point.x, point.y]:
            terminal.layer(c.Layers.TESTING)
            terminal.color(terminal.color_from_name("YELLOW"))
            terminal.put(point.x, point.y, "\u2588")
            time.sleep(.1)


    terminal.refresh()
    terminal.clear()


def can_place(point, direction, dungeon_map: Dungeon=None, testing_grid=None):
    directions = []
    if direction == Point(0, 0):
        directions = Direction.every()

    for d in directions:
        neighbor = point + d
        if dungeon_map.label(neighbor) != 0:
            return False

    return False


def main():
    # seed map
    map_seed = "TEST_MAP"
    random.seed(map_seed)

    # create dungeon generator
    d_map = DungeonGenerator(MAP_SETTINGS)
    d_map.clear_map()

    # place rooms by hand
    d_map.place_room(11, 1, 8, 3, 1)
    d_map.place_room(25, 2, 3, 5, 1)
    d_map.place_room(3, 3, 3, 5, 1)
    d_map.place_room(18, 8, 5, 3, 1)
    d_map.place_room(25, 8, 5, 7, 1)
    d_map.place_room(5, 11, 5, 3, 1)
    d_map.place_room(11, 13, 5, 7, 1)
    d_map.place_room(21, 14, 3, 5, 1)

    testing_grid = d_map.dungeon.label_grid.copy()
    testing_grid.fill(0)
    display_map(d_map, testing_grid)

    for y in range(1, d_map.height - 1):
        for x in range(1, d_map.width - 1):
            testing_grid.fill(0)
            start_point = Point(x, y)
            points_to_check = []
            can_carve = False

            terminal.layer(c.Layers.TESTING)
            terminal.color(BLUE)
            terminal.put(start_point.x, start_point.y, c.Tiles.BLOCK)
            terminal.color(WHITE)

            if d_map.dungeon.label(start_point) != TileType.WALL.value:
                # terminal.layer(c.Layers.TESTING)
                # terminal.color(RED)
                # terminal.put(start_point.x, start_point.y, c.Tiles.BLOCK)
                print(f"start point {start_point} is not wall")
                continue

            for direction in Direction.every():
                testing_grid[start_point.x + direction.x, start_point.y + direction.y] = 1
                if d_map.dungeon.label(start_point + direction) != TileType.WALL.value:
                    continue


        display_map(d_map, testing_grid)


if __name__ == "__main__":
    terminal.open()
    main()
    terminal.close()
