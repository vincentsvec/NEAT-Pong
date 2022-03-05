import pygame
import os
from game.game import Game
from config.globals import screen

pygame.init()

if __name__ == "__main__":
    local_dir = os.pat.dirname(__file__)
    conf_path = os.path.join(local_dir, "config/neat_config.txt")

    game = Game()
    game.run()
