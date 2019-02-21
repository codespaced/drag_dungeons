import esper
from bearlibterminal import terminal

import component as c
import const


class RenderProcessor(esper.Processor):
    def __init__(self):
        super(RenderProcessor, self).__init__()

        self.screen_width = const.SCREEN_WIDTH
        self.screen_height = const.SCREEN_HEIGHT
        self.map_width = const.MAP_WIDTH
        self.map_height = const.MAP_HEIGHT

    def process(self, **kwargs):
        self.render_all()
        self.refresh_terminal()
        self.clear_all()

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
