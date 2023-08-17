from ursina import *
from rubiks_cube import RubiksCube
from input_handler import InputHandler

class Game(Entity):
    def __init__(self):
        super().__init__()
        self.rubiks_cube = RubiksCube()
        self.input_handler = InputHandler(rubiks_cube=self.rubiks_cube)
        self.initialize_surroundings()
        self.load_game()

    def initialize_surroundings(self):
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(
            60, 60), rotation_x=90, y=-5, color=color.light_gray)  # plane
        Entity(model='sphere', scale=100,
               texture='textures/sky0', double_sided=True)  # sky
        camera = EditorCamera()
        camera.world_position = (0, 0, -5)

    def load_game(self):
        self.rubiks_cube.create_rubiks_cube()

    def input(self, key):
        self.input_handler.handleInputs(key)


if __name__ == '__main__':
    app = Ursina()
    window.fullscreen = False
    game = Game()
    app.run()
