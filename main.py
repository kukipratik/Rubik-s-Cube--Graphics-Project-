from ursina import *
from game import Game
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


if __name__ == '__main__':
    controller = GameController()
