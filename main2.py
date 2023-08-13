from ursina import *

class Game():
    def __init__(self):
        super().__init__()
        app = Ursina()
        window.fullscreen = True
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100,
               texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.load_game()
        app.run()
        
    def load_game(self):
        Entity(model= self.model, texture= self.texture)

    def input(self, key):
        super().input(key)

if __name__ == '__main__':
    game = Game()
    game.run()
