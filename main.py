from ursina import *
from rubiks_cube import RubiksCube
from input_handler import InputHandler

# class RubiksCube(Entity):
#     def __init__(self):
#         super().__init__()
#         self.create_cube_positions()

#     def create_cube_positions(self):
#         self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2)
#                      for z in range(-1, 2)}
#         self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2)
#                        for z in range(-1, 2)}
#         self.FACE = {Vec3(x, y, -1) for x in range(-1, 2)
#                      for y in range(-1, 2)}
#         self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
#         self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2)
#                       for z in range(-1, 2)}
#         self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
#         self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP

#     def create_rubiks_cube(self):
#         self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'
#         self.CUBES = [Entity(model=self.cube_model, texture=self.cube_texture,
#                              position=pos) for pos in self.SIDE_POSITIONS]
#         self.PARENT = Entity()
#         self.rotation_axes = {"LEFT": "x", "RIGHT": "x",
#                               'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
#         self.cubes_side_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM,
#                                      'RIGHT': self.RIGHT, 'FACE': self.FACE,
#                                      'BACK': self.BACK, 'TOP': self.TOP}
#         self.random_state()
#         # add sensor to cube
#         self.create_sensors()

#     def random_state(self, rotations=3):
#         [self.rotate_side_without_animation(random.choice(
#             list(self.rotation_axes))) for i in range(rotations)]

#     def rotate_side_without_animation(self, side_name):
#         cube_positions = self.cubes_side_positions[side_name]
#         rotation_axis = self.rotation_axes[side_name]
#         self.reparent_to_scene()
#         for cube in self.CUBES:
#             if cube.position in cube_positions:
#                 cube.parent = self.PARENT
#                 exec(f'self.PARENT.rotation_{rotation_axis} =  90')

#     def rotate_side(self, side_name, animation_time):
#         cube_positions = self.cubes_side_positions[side_name]
#         rotation_axis = self.rotation_axes[side_name]
#         self.reparent_to_scene()
#         for cube in self.CUBES:
#             if cube.position in cube_positions:
#                 cube.parent = self.PARENT
#                 eval(
#                     f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=animation_time)')

#     def reparent_to_scene(self):
#         for cube in self.CUBES:
#             if cube.parent == self.PARENT:
#                 world_pos, world_rot = round(
#                     cube.world_position, 1), cube.world_rotation
#                 cube.parent = scene
#                 cube.position, cube.rotation = world_pos, world_rot
#         self.PARENT.rotation = 0

#     def create_sensors(self):
#         def create_sensor(name, pos, scale):
#             return Entity(name=name, position=pos, model='cube', color=color.dark_gray, scale=scale,   collider='box', visible=False)

#         self.LEFT_sensor = create_sensor(
#             name='LEFT', pos=(-0.99, 0, 0), scale=(1.01, 3.01, 3.01))
#         self.FACE_sensor = create_sensor(
#             name='FACE', pos=(0, 0, -0.99), scale=(3.01, 3.01, 1.01))
#         self.BACK_sensor = create_sensor(
#             name='BACK', pos=(0, 0, 0.99), scale=(3.01, 3.01, 1.01))
#         self.RIGHT_sensor = create_sensor(
#             name='RIGHT', pos=(0.99, 0, 0), scale=(1.01, 3.01, 3.01))
#         self.TOP_sensor = create_sensor(
#             name='TOP', pos=(0, 1, 0), scale=(3.01, 1.01, 3.01))
#         self.BOTTOM_sensor = create_sensor(
#             name='BOTTOM', pos=(0, -1, 0), scale=(3.01, 1.01, 3.01))


# class InputHandler:
#     def __init__(self, rubiks_cube):
#         self.mouse_right_click = 'right mouse down'
#         self.mouse_middle_click = 'middle mouse down'
#         self.mouse_left_click = 'left mouse down'

#         self.animation_time = 0.5
#         self.action_trigger = True
#         self.action_mode = True

#         self.rubiks_cube = rubiks_cube

#         # display message
#         self.message = Text(origin=(0, 19), color=color.black)
#         self.toggle_game_mode()

#     def toggle_game_mode(self):
#         self.action_mode = not self.action_mode
#         msg = dedent(f"{'ACTION mode ON' if self.action_mode else 'VIEW mode ON'}"
#                      f"(to switch - press middle mouse button)").strip()
#         self.message.text = msg

#     def toggle_animation_trigger(self):
#         self.action_trigger = not self.action_trigger

#     def handleInputs(self, key):
#         if key in f'{self.mouse_left_click} {self.mouse_right_click}' and self.action_mode and self.action_trigger:
#             for hitinfo in mouse.collisions:
#                 collider_name = hitinfo.entity.name
#                 if (key == self.mouse_left_click and collider_name in 'LEFT RIGHT FACE BACK' or
#                    key == self.mouse_right_click and collider_name in 'TOP BOTTOM'):
#                     self.action_trigger = False
#                     self.rubiks_cube.rotate_side(side_name=collider_name, animation_time = self.animation_time)
#                     invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)
#                     break

#         if key == self.mouse_middle_click or key == 'v':
#             self.toggle_game_mode()


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
