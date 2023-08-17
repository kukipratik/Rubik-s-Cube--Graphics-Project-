from ursina import *

class InputHandler:
    def __init__(self, game):
        self.game = game

    def input(self, key):
        print("got here")
        mouse_right_click = 'right mouse down'
        mouse_middle_click = 'middle mouse down'
        mouse_left_click = 'left mouse down'
        
        if key in f'{mouse_left_click} {mouse_right_click}' and self.game.action_mode and self.game.action_trigger:
            for hitinfo in mouse.collisions:
                collider_name = hitinfo.entity.name
                if (key == mouse_left_click and collider_name in 'LEFT RIGHT FACE BACK' or
                    key == mouse_right_click and collider_name in 'TOP BOTTOM'):
                    self.game.rotate_side(collider_name)
                    break

        if key == mouse_middle_click or key == 'v':
            self.game.toggle_game_mode()

class Game(Entity):
    def __init__(self):
        super().__init__()
        # app = Ursina()
        window.fullscreen = False
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100,
               texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()
        self.input_handler = InputHandler(self)
        # app.run()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.cube_model, texture=self.cube_texture,
                             position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {"LEFT": "x", "RIGHT": "x",
                              'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
        self.cubes_side_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM,
                                     'RIGHT': self.RIGHT, 'FACE': self.FACE,
                                     'BACK': self.BACK, 'TOP': self.TOP}
        self.animation_time = 0.5
        self.action_trigger = True
        self.action_mode = True
        self.message = Text(origin=(0, 19), color=color.black)
        self.toggle_game_mode()
        self.create_sensors()
        self.random_state()

    def random_state(self, rotations = 3):
        [self.rotate_side_without_animation(random.choice(list(self.rotation_axes))) for i in range(rotations)]

    def rotate_side_without_animation(self, side_name):
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent= self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} =  90')

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

    def toggle_game_mode(self):
        self.action_mode = not self.action_mode
        msg = dedent(f"{'ACTION mode ON' if self.action_mode else 'VIEW mode ON'}"
                     f"(to switch - press middle mouse button)").strip()
        self.message.text = msg

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(
                    f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(
                    cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

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

    def input(self, key):
        self.input_handler.input(key)

if __name__ == '__main__':
    app = Ursina()
    game = Game()
    app.run()
