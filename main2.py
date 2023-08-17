from ursina import *


class Game(Entity):
    def __init__(self):
        super().__init__()
        app = Ursina()
        window.fullscreen = False
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100,
               texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()
        app.run()

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
        self.message = Text(origin=(0,19), color=color.black)
        self.toggle_game_mode()
    
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
        # if key == 'a':
        #     self.rotate_side('LEFT')
        # if key == 's':
        #     self.rotate_side('BOTTOM')
        keys = dict(zip('asdwqe', 'LEFT BOTTOM RIGHT TOP FACE BACK'.split()))
        if key in keys and self.action_trigger:
            self.rotate_side(keys[key])

        if key == "left mouse down":
            print("clicked left")

        if key == "middle mouse down":
            print("middle mouse left")
            self.toggle_game_mode()
        #     self.rot += 90
        #     self.PARENT.animate_rotation_x(self.rot, duration=0.5)


if __name__ == '__main__':
    game = Game()
    # game.run()
