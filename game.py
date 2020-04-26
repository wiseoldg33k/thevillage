import arcade
import os

import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Village"

VILLAGER_SPRITE_SCALING = 0.5
BUILDING_SPRITE_SCALING = 0.6
RESOURCE_SPRITE_SCALING = 0.8


class Villager(arcade.Sprite):
    def update(self):
        self.center_x += random.randint(-5, 5)
        self.center_y += random.randint(-5, 5)


class Building(arcade.Sprite):
    pass


class Resource(arcade.Sprite):
    pass


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.town_hall_location = (0, 0)

        self.villagers = arcade.SpriteList()
        self.buildings = arcade.SpriteList()
        self.resources = arcade.SpriteList()

    def setup(self, rate=1 / 60):

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        self.set_update_rate(rate=rate)

    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        self.buildings.draw()
        self.resources.draw()

        # keep villagers on top of everything please
        self.villagers.draw()

    def on_update(self, delta_time):
        self.villagers.update()

    def add_villager(self, name, imagename):
        v = Villager(
            os.path.join("assets", "villagers", imagename),
            scale=VILLAGER_SPRITE_SCALING,
        )
        v.name = name
        v.center_x, v.center_y = self.town_hall_location
        self.villagers.append(v)

    def add_town_hall(self, x_placement, y_placement, imagename):
        b = Building(
            os.path.join("assets", "terrain", "Structure", imagename),
            scale=BUILDING_SPRITE_SCALING,
        )
        b.center_x = int(x_placement * SCREEN_WIDTH)
        b.center_y = int(y_placement * SCREEN_HEIGHT)
        self.buildings.append(b)

        self.town_hall_location = (b.center_x, b.center_y)

    def add_resource(self, x_placement, y_placement, imagename):
        res = Resource(
            os.path.join("assets", "terrain", "Environment", imagename),
            scale=RESOURCE_SPRITE_SCALING,
        )
        res.center_x = int(x_placement * SCREEN_WIDTH)
        res.center_y = int(y_placement * SCREEN_HEIGHT)
        self.resources.append(res)


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup(1 / 12)

    game.add_town_hall(0.5, 0.5, "medievalStructure_09.png")

    game.add_resource(0.2, 0.2, "medievalEnvironment_19.png")

    game.add_villager("Alice", "female_idle.png")
    game.add_villager("Rob", "zombie_idle.png")

    arcade.run()


if __name__ == "__main__":
    main()
