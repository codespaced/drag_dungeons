import esper
from bearlibterminal import terminal

import component as c
import const

from map_objects.enums import TileType


class RenderProcessor(esper.Processor):
    def __init__(self):
        super(RenderProcessor, self).__init__()

        self.screen_width = const.SCREEN_WIDTH
        self.screen_height = const.SCREEN_HEIGHT
        self.map_width = const.MAP_WIDTH
        self.map_height = const.MAP_HEIGHT

    def process(self, **kwargs):
        self.render_all()
        self.render_map(kwargs.get("game_map"))
        self.refresh_terminal()
        self.clear_all()

    def render_map(self, game_map):
        if game_map:
            for point, tile in game_map:
                color = terminal.color_from_name("white")
                ch = "X"
                if tile.label == TileType.EMPTY:
                    color = terminal.color_from_name("black")
                    ch = "-"
                elif tile.label == TileType.FLOOR:
                    color = terminal.color_from_name("grey")
                    ch = "."
                elif tile.label == TileType.WALL:
                    color = terminal.color_from_name("black")
                    ch = "#"
                elif tile.label == TileType.CORRIDOR:
                    color = terminal.color_from_name("dark_grey")
                    ch = "+"
                terminal.layer(0)
                terminal.bkcolor(color)
                terminal.put(point.x, point.y, " ")

    def render_all(self):
        generator = self.world.get_components(c.Renderable, c.Position)

        for ent, (rend, pos) in generator:
            color = terminal.color_from_argb(255, r=rend.fg[0], g=rend.fg[1], b=rend.fg[2])
            terminal.color(color)
            terminal.put(x=int(pos.x), y=int(pos.y), c=rend.ch)

    def refresh_terminal(self):
        terminal.refresh()

    def clear_all(self):
        terminal.clear()
