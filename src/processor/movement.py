import esper

import component as c


class MovementProcessor(esper.Processor):
    def __init__(self):
        super(MovementProcessor, self).__init__()

    def process(self, **kwargs):
        for ent, (event, vel, pos) in self.world.get_components(c.Event, c.Velocity, c.Position):
            if event.action.get("move"):
                pos.x += vel.dx
                pos.y += vel.dy
