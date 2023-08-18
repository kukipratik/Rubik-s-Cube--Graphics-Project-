from ursina import *


class RubiksCube(Entity):
    def __init__(self):
        super().__init__()
        self.create_cube_positions()

    def create_rubiks_cube(self):
        self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'
        self.CUBES = [Entity(model=self.cube_model, texture=self.cube_texture,
                             position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {"LEFT": "x", "RIGHT": "x",
                              'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
        self.cubes_side_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM,
                                     'RIGHT': self.RIGHT, 'FACE': self.FACE,
                                     'BACK': self.BACK, 'TOP': self.TOP}
        self.random_state()
        # add sensor to cube
        self.create_sensors()

    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2)
                     for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2)
                       for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2)
                     for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2)
                      for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP
        # print("left face = ", self.LEFT)
        # print("top face = ", self.TOP)
        print("all face = ", self.SIDE_POSITIONS)

    def create_sensors(self):
        def create_sensor(name, pos, scale):
            return Entity(name=name, position=pos, model='cube', color=color.dark_gray, scale=scale,   collider='box', visible=False)

        self.LEFT_sensor = create_sensor(
            name='LEFT', pos=(-0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.FACE_sensor = create_sensor(
            name='FACE', pos=(0, 0, -0.99), scale=(3.01, 3.01, 1.01))
        self.BACK_sensor = create_sensor(
            name='BACK', pos=(0, 0, 0.99), scale=(3.01, 3.01, 1.01))
        self.RIGHT_sensor = create_sensor(
            name='RIGHT', pos=(0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.TOP_sensor = create_sensor(
            name='TOP', pos=(0, 1, 0), scale=(3.01, 1.01, 3.01))
        self.BOTTOM_sensor = create_sensor(
            name='BOTTOM', pos=(0, -1, 0), scale=(3.01, 1.01, 3.01))

    def random_state(self, rotations=3):
        [self.rotate_side_without_animation(random.choice(
            list(self.rotation_axes))) for i in range(rotations)]

    def rotate_side_without_animation(self, side_name):
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} =  90')

    # don't remove animation_time from props (it is being used actually)
    def rotate_side(self, side_name, animation_time, angle):
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(
                    f'self.PARENT.animate_rotation_{rotation_axis}({angle}, duration=animation_time)')

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(
                    cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0
