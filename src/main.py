import pygame
import neat
import os
from game.game import Game
from ai.ai import AI
import pickle

pygame.init()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    conf_path = os.path.join(local_dir, "config/neat_config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, conf_path)

    ai = AI(config)
    mode = ai.get_mode()

    if mode == 1:
        ai.run()
    elif mode == 2:
        best_ai = ai.load_best()
        ai.test(best_ai)
    else:
        ai.standard_game()
