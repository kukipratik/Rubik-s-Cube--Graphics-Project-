from ursina import *
from rubiks_cube import RubiksCube
from input_handler import InputHandler
from ursina.shaders import *


class GameController:
    def __init__(self):
        self.app = Ursina()
        window.fullscreen = False
        self.day_time = True
        self.game = Game(self)
        self.app.run()

    def toggle_day_time(self):
        self.day_time = not self.day_time
        self.game.restart()
        self.app.restart()

    def get_day_time(self):
        return self.day_time


class Game(Entity):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.load_game()

    def load_game(self):
        self.rubiks_cube = RubiksCube()
        self.rubiks_cube.create_rubiks_cube()
        self.input_handler = InputHandler(rubiks_cube=self.rubiks_cube)
        if self.controller.get_day_time():
            self.initialize_surroundings_for_day_time()
        else:
            self.initialize_surroundings_for_night()

    def initialize_surroundings_for_night(self):
        print("nignt")
        self.camera = EditorCamera()
        self.camera.world_position = (0, 0, -5)
        self.light = DirectionalLight(parent=camera, y=-1, z=-3,
                                      shadows=True, rotation=(45, -45, 45))
        self.ground = Entity(model='quad', scale=60, texture='white_cube', texture_scale=(
            60, 60), rotation_x=90, y=-5, color=color.light_gray, shader=lit_with_shadows_shader)  # plane
        self.sky = Entity(model='sphere', scale=100,
                          texture='textures/sky0', double_sided=True)  # sky


    def initialize_surroundings_for_day_time(self):
        print("day")
        self.camera = EditorCamera()
        self.camera.world_position = (0, 0, -5)
        self.ground = Entity(model='quad', scale=60, texture='white_cube', texture_scale=(
            60, 60), rotation_x=90, y=-5, color=color.light_gray, shader=lit_with_shadows_shader)  # plane
        self.sky = Entity(model='sphere', scale=100,
                        texture='textures/sky0', double_sided=True)  # sky


    def destroy_all_entities(self):
        destroy(self.camera)
        if self.controller.get_day_time():
            destroy(self.light)
        destroy(self.ground)
        destroy(self.sky)
        destroy(self.input_handler.message)
        for cube in self.rubiks_cube.CUBES:
            destroy(cube)

    def restart(self):
        self.destroy_all_entities()
        self.rubiks_cube = None
        self.input_handler = None
        self.load_game()

    def input(self, key):
        self.input_handler.handleInputs(key)
        if key == 'r':
            self.controller.toggle_day_time()


if __name__ == '__main__':
    controller = GameController()
