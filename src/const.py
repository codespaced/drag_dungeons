from bearlibterminal import terminal


TITLE = "Drag Dungeons"

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 43

FONT_PATH = "data/consolas10x10.png"

MAP_SETTINGS = {
    "map_height": 50,
    "map_width": 100,
    "tile_size": 10,
    "num_rooms": 100,
    "min_room_size": 4,
    "max_room_size": 15,
    "room_margin": 3,
}

COLORS = {
    "transparent",
    "none",
    "black",
    "white",
    "grey",
    "gray",
    "red",
    "flame",
    "orange",
    "amber",
    "yellow",
    "lime",
    "chartreuse",
    "green",
    "sea",
    "turquoise",
    "cyan",
    "sky",
    "azure",
    "blue",
    "han",
    "violet",
    "purple",
    "fuchsia",
    "magenta",
    "pink",
    "crimson",
    }


class Layers:
    BACKGROUND = 0
    MAP = 10
    PLAYER = 20
    LIGHT = 30
    TESTING = 50


class Tiles:
    UNSEEN = "\uE004"
    FLOOR = "\uE000"
    CORRIDOR = "\uE001"
    WALL = "\uE002"
    CONNECT = "\uE003"
    BLOCK = "\u2588"
