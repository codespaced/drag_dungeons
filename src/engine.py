import esper

from bearlibterminal import terminal
from dataclasses import dataclass

import const as c
from input_handler import handle_input


#################################
# Components                    #
#################################
@dataclass()
class Position:
    x: int
    y: int


@dataclass()
class Renderable:
    ch: str = "@"
    fg: tuple = (255, 255, 255)
    bg: tuple = (0, 0, 0)
    layer: int = 0
    comp: int = terminal.TK_OFF  # TK_OFF == 0


@dataclass()
class Velocity:
    dx: int = 0
    dy: int = 0


@dataclass()
class TakesInput:
    pass


#################################
# Processors                    #
#################################
class MovementProcessor(esper.Processor):
    def __init__(self):
        super(MovementProcessor, self).__init__()

    def process(self, *args, **kwargs):
        action = kwargs.get("action")
        move = action.get("move")
        if move:
            for ent, (ti, vel, pos) in self.world.get_components(TakesInput, Velocity, Position):
                pos.x += vel.dx
                pos.y += vel.dy


class InputProcessor(esper.Processor):
    def __init__(self):
        super(InputProcessor, self).__init__()

    def process(self, *args, **kwargs):
        action = handle_input()

        Game.action = action

        move = Game.action.get("move")
        game_exit = Game.action.get("exit")

        if move:
            for ent, (ti, vel) in self.world.get_components(TakesInput, Velocity):
                dx, dy = move
                vel.dx = dx
                vel.dy = dy

        if game_exit:
            Game.game_exit = True


class RenderProcessor(esper.Processor):
    def __init__(self):
        super(RenderProcessor, self).__init__()

    def process(self, *args, **kwargs):
        self.render_all()
        self.refresh_terminal()
        self.clear_all()

    def render_all(self):
        generator = self.world.get_components(Renderable, Position)
        for ent, (ren, pos) in generator:
            terminal.color(terminal.color_from_argb(255, r=ren.fg[0], g=ren.fg[1], b=ren.fg[2]))
            terminal.put(x=int(pos.x), y=int(pos.y), c=ren.ch)

    def refresh_terminal(self):
        terminal.refresh()

    def clear_all(self):
        terminal.clear()


class Game:
    game_exit = False
    action = {}

    def __init__(self):
        self.world = esper.World()

    def on_start(self):
        processors = (
            MovementProcessor(),
            InputProcessor(),
            RenderProcessor()
        )

        for num, proc in enumerate(processors):
            self.world.add_processor(proc, priority=num)

    def on_enter(self):
        player = self.world.create_entity()
        self.world.add_component(player, Position(x=c.SCREEN_WIDTH/2, y=c.SCREEN_HEIGHT/2))
        self.world.add_component(player, Velocity())
        self.world.add_component(player, TakesInput())
        self.world.add_component(player, Renderable())

    def on_update(self):
        # print("on_update")
        self.world.process(action=self.action)


def main():
    game = Game()
    game.on_start()
    game.on_enter()

    while not game.game_exit:
        game.on_update()


if __name__ == "__main__":
    terminal.open()
    main()
    terminal.close()
