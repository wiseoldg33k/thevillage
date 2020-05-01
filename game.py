import os
import random
from collections import deque

import arcade
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1920
SCREEN_TITLE = "The Village"

VILLAGER_SPRITE_SCALING = 0.8
BUILDING_SPRITE_SCALING = 0.5
RESOURCE_SPRITE_SCALING = 0.8

GRID_SIZE = 64


def pixels_to_grid(x, y, max_y, grid_size):
    return x // grid_size, (max_y - y) // grid_size


def grid_to_pixels(x, y, max_y, grid_size):
    return x * grid_size, max_y - (y * grid_size)


class Villager(arcade.Sprite):
    def __init__(self, game, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game
        self.name = name
        self.current_path = deque([])

    def compute_path(self, obj):
        grid = Grid(matrix=self.game.matrix)

        grid_obj_pos = pixels_to_grid(
            obj.center_x, obj.center_y, max_y=SCREEN_HEIGHT, grid_size=GRID_SIZE
        )
        grid_self_pos = pixels_to_grid(
            self.center_x, self.center_y, max_y=SCREEN_HEIGHT, grid_size=GRID_SIZE
        )

        start = grid.node(*grid_self_pos)
        end = grid.node(*grid_obj_pos)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)

        path = deque(path)
        self.current_path = path
        return path

    def update(self):
        if self.current_path:
            path = self.current_path
        else:
            if self.game.resources:
                target = random.choice(self.game.resources)
                path = self.compute_path(target)

        if path:
            next_move = path.popleft()
            self.center_x, self.center_y = grid_to_pixels(
                *next_move, max_y=SCREEN_HEIGHT, grid_size=GRID_SIZE
            )


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
        self.pause = False
        self.show_pathfinding_grid = False

        matrix = []
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            row = []
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                row.append(1)
            matrix.insert(0, row)
        self.matrix = matrix

        self.villagers = arcade.SpriteList()
        self.buildings = arcade.SpriteList()
        self.resources = arcade.SpriteList()

    def setup(self, rate=1 / 60):
        # Set the background color
        arcade.set_background_color(arcade.color.DIRT)
        self.pause = False
        self.set_update_rate(rate=rate)

    def draw_pathfinding_canvas(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.CYAN, 1)

        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            arcade.draw_line(0, y, SCREEN_WIDTH, y, arcade.color.CYAN, 1)

    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        if self.show_pathfinding_grid:
            self.draw_pathfinding_canvas()

        self.buildings.draw()
        self.resources.draw()

        # keep villagers on top of everything please
        self.villagers.draw()

    def on_update(self, delta_time):
        if not self.pause:
            self.villagers.update()

    def on_key_release(self, key, modifier):
        if key == arcade.key.SPACE:
            self.pause = not self.pause
        if key == arcade.key.P:
            self.show_pathfinding_grid = not self.show_pathfinding_grid

    def add_villager(self, name, imagename):
        v = Villager(
            filename=os.path.join("assets", "villagers", imagename),
            scale=VILLAGER_SPRITE_SCALING,
            game=self,
            name=name,
        )
        v.center_x, v.center_y = self.town_hall_location
        self.villagers.append(v)

    def add_town_hall(self, x_placement, y_placement, imagename):
        b = Building(
            os.path.join("assets", "terrain", "Structure", imagename),
            scale=BUILDING_SPRITE_SCALING,
        )
        b.center_x = (int(x_placement * SCREEN_WIDTH) // GRID_SIZE) * GRID_SIZE
        b.center_y = (int(y_placement * SCREEN_HEIGHT) // GRID_SIZE) * GRID_SIZE
        self.buildings.append(b)

        self.town_hall_location = (b.center_x, b.center_y)

    def add_resource(self, x_placement, y_placement, imagename):
        res = Resource(
            os.path.join("assets", "terrain", "Environment", imagename),
            scale=RESOURCE_SPRITE_SCALING,
        )
        res.center_x = (int(x_placement * SCREEN_WIDTH) // GRID_SIZE) * GRID_SIZE
        res.center_y = (int(y_placement * SCREEN_HEIGHT) // GRID_SIZE) * GRID_SIZE
        self.resources.append(res)


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup(1 / 6)

    game.add_town_hall(0.5, 0.5, "medievalStructure_09.png")

    game.add_resource(0.2, 0.2, "medievalEnvironment_19.png")
    game.add_resource(0.8, 0.8, "medievalEnvironment_19.png")
    game.add_resource(0.1, 0.9, "medievalEnvironment_19.png")

    game.add_villager("Alice", "female_idle.png")
    game.add_villager("Rob", "zombie_idle.png")

    arcade.run()


if __name__ == "__main__":
    main()
