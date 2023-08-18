from ursina import *
from rubiks_cube import RubiksCube
from input_handler import InputHandler
from ursina.shaders import lit_with_shadows_shader


class GameController(Entity):
    def __init__(self):
        super().__init__()
        self.app = Ursina()
        window.fullscreen = False
        self.day_time = True
        print("hello. I got called here")
    
    def toogle_day_time(self):
        self.day_time = not self.day_time
        self.app.restart()
    
    def get_day_time(self):
        return self.day_time

    def run(self):
        self.app.run()


class Game(GameController):
    def __init__(self):
        super().__init__()
        self.load_game()
        self.run()

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
    Game()
