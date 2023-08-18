from ursina import *
from rubiks_cube import RubiksCube
from input_handler import InputHandler
from ursina.shaders import lit_with_shadows_shader


class Game(Entity):
    def __init__(self):
        super().__init__()
        self.load_game()

    def load_game(self):
        self.rubiks_cube = RubiksCube()
        self.rubiks_cube.create_rubiks_cube()
        self.input_handler = InputHandler(rubiks_cube=self.rubiks_cube)
        self.initialize_surroundings()

    def initialize_surroundings(self):
        camera = EditorCamera()
        camera.world_position = (0, 0, -5)
        DirectionalLight(parent=camera, y=-1, z=-3,
                         shadows=True, rotation=(45, -45, 45))
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(
            60, 60), rotation_x=90, y=-5, color=color.light_gray, shader=lit_with_shadows_shader)  # plane
        Entity(model='sphere', scale=100,
               texture='textures/sky0', double_sided=True)  # sky

    def input(self, key):
        self.input_handler.handleInputs(key)


if __name__ == '__main__':
    app = Ursina()
    window.fullscreen = False
    game = Game()
    app.run()
