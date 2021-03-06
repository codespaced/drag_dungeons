import esper

from bearlibterminal import terminal

import component as c
import const
import processor as p

from map_objects.generator import DungeonGenerator


class Game:
    action = {}
    game_exit = False

    @classmethod
    def quit_game(cls):
        cls.game_exit = True

    def __init__(self):
        self.world = esper.World()
        self.dungeon_generator = DungeonGenerator(const.MAP_SETTINGS)

    def on_start(self):
        processors = (
            p.MovementProcessor(),
            p.InputProcessor(),
            p.RenderProcessor()
        )

        for num, proc in enumerate(processors):
            self.world.add_processor(proc, priority=num)

    def on_enter(self):
        player = self.world.create_entity()
        self.world.add_component(player, c.Position(x=const.SCREEN_WIDTH/2, y=const.SCREEN_HEIGHT/2))
        self.world.add_component(player, c.Velocity())
        self.world.add_component(player, c.TakesInput())
        self.world.add_component(player, c.Renderable())
        self.world.add_component(player, c.Event({}))

        self.dungeon_generator.initialize_map()
        self.dungeon_generator.place_random_rooms(
            min_room_size=const.MAP_SETTINGS["min_room_size"],
            max_room_size=const.MAP_SETTINGS["max_room_size"],
        )
        self.dungeon_generator.build_corridors()

    def on_update(self):
        # print("on_update")
        self.world.process(game_map=self.dungeon_generator.dungeon)
        generator = self.world.get_component(c.Event)
        for ent, event in generator:
            if event.action.get("exit"):
                self.quit_game()
            if event.action.get("remake"):
                self.remake_map()

    def remake_map(self):
        self.dungeon_generator.clear_map()
        self.dungeon_generator.initialize_map()
        self.dungeon_generator.place_random_rooms(
            min_room_size=const.MAP_SETTINGS["min_room_size"],
            max_room_size=const.MAP_SETTINGS["max_room_size"]
        )
        self.dungeon_generator.build_corridors()


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
