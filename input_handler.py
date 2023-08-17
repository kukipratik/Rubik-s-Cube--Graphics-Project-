from ursina import *

class InputHandler:
    def __init__(self, rubiks_cube):
        self.mouse_right_click = 'right mouse down'
        self.mouse_middle_click = 'middle mouse down'
        self.mouse_left_click = 'left mouse down'

        self.animation_time = 0.5
        self.action_trigger = True
        self.action_mode = True

        self.rubiks_cube = rubiks_cube

        # display message
        self.message = Text(origin=(0, 19), color=color.black)
        self.toggle_game_mode()

    def toggle_game_mode(self):
        self.action_mode = not self.action_mode
        msg = dedent(f"{'ACTION mode ON' if self.action_mode else 'VIEW mode ON'}"
                     f"(to switch - press middle mouse button)").strip()
        self.message.text = msg

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger

    def handleInputs(self, key):
        if key in f'{self.mouse_left_click} {self.mouse_right_click}' and self.action_mode and self.action_trigger:
            for hitinfo in mouse.collisions:
                collider_name = hitinfo.entity.name
                if (key == self.mouse_left_click and collider_name in 'LEFT RIGHT FACE BACK' or
                   key == self.mouse_right_click and collider_name in 'TOP BOTTOM'):
                    self.action_trigger = False
                    self.rubiks_cube.rotate_side(side_name=collider_name, animation_time = self.animation_time)
                    invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)
                    break

        if key == self.mouse_middle_click or key == 'v':
            self.toggle_game_mode()
