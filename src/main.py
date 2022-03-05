import pygame
import neat
import os
from game.game import Game
from ai.ai import AI
from config.globals import screen

pygame.init()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    conf_path = os.path.join(local_dir, "config/neat_config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, conf_path)

    ai = AI(config)
    ai.run()

    #game = Game()
    # game.run()
