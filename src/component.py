from bearlibterminal import terminal
from dataclasses import dataclass


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


@dataclass()
class Event:
    action: dict
