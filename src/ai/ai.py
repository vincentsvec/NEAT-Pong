"""
Ai module
"""
import pygame
import neat
import pickle
from game.game import Game
from config.globals import screen, colors, generations
from components.paddle import Paddle
from components.ball import Ball


class AI():
    def __init__(self, config):
        self.config = config
        self.clock = pygame.time.Clock()
        self.dis = pygame.display.set_mode((screen["width"], screen["height"]))
        self.paddle1 = Paddle(self.dis, 1)
        self.paddle2 = Paddle(self.dis, 2)
        self.ball = Ball(self.dis, [self.paddle1, self.paddle2])
        self.score = [0, 0]

    def run(self):
        """
        Initialisation of the AI.
        """

        # uncomment next line to resume training from checkpoint
        #pop = neat.Checkpointer.restore_checkpoint("neat-checkpoint-12")

        # comment next line to train from checkpoint
        pop = neat.Population(self.config)
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
        pop.add_reporter(neat.Checkpointer(1))

        best_ai = pop.run(self.eval_genomes, generations)
        self.save_best(best_ai)

    def eval_genomes(self, genomes, _):
        """
        The fitness funtion of neat algorithm. Creates 2 genomes to train against each other.
        """

        for i, (genome_id, genome1) in enumerate(genomes):
            if i == len(genomes) - 1:
                break

            genome1.fitness = 0

            for genome_id2, genome2 in genomes[i + i:]:
                genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
                self.genome1 = genome1
                self.genome2 = genome2
                self.train()

    def train(self):
        """
        Training function of Ai. Initialisation of 2 networks. Init of game
        """

        self.network1 = neat.nn.FeedForwardNetwork.create(
            self.genome1, self.config)
        self.network2 = neat.nn.FeedForwardNetwork.create(
            self.genome2, self.config)

        self.game = Game(self)
        self.game.run()

    def get_decision(self):
        """
        Decides which action to take. Networks take 3 inputs and gives 3 outputs. 
        Stay, go up or go down. The decision with the highest value is picked.
        """

        # output of neat algorithm
        out1 = self.network1.activate((self.game.paddle1.posy, self.game.ball.posy, abs(
            self.game.paddle1.posx - self.game.ball.posx)))
        out2 = self.network2.activate((self.game.paddle2.posy, self.game.ball.posy, abs(
            self.game.paddle2.posx - self.game.ball.posx)))

        # decision of ai
        dec1 = out1.index(max(out1))
        dec2 = out2.index(max(out2))

        return [dec1, dec2]

    def enum_fitness(self, positive, paddle_hits_miss):
        """
        Adds or substracts fitness from genomes.
        If positive is True the fintess is added, else the fitness is substracted.
        """

        if positive:
            self.genome1.fitness += paddle_hits_miss[0]
            self.genome2.fitness += paddle_hits_miss[1]

        else:
            self.genome1.fitness -= paddle_hits_miss[0]
            self.genome2.fitness -= paddle_hits_miss[1]

    def test(self, genome):
        """
        Game loop for testing the best ai.
        Test takes the best genome and creates the network from it.
        """

        run = True
        game = Game(self)

        self.reset_train()

        network = neat.nn.FeedForwardNetwork.create(genome, self.config)

        while run:
            self.dis.fill(colors["black"])
            game.draw_arena(self.score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.paddle1.update(event)
            self.paddle2.update(event)

            # output and decision of network.
            out = network.activate((self.paddle2.posy, self.ball.posy, abs(
                self.paddle2.posx - self.ball.posx)))

            dec = out.index(max(out))
            self.paddle2.ai_move(dec)

            game_over, paddle_miss = self.ball.update()
            if game_over:
                if paddle_miss[0] == 1:
                    self.score[1] += 1
                else:
                    self.score[0] += 1

                self.test(genome)

            pygame.display.update()
            self.clock.tick(screen["test_fps"])

        pygame.quit()
        quit()

    def reset_train(self):
        self.paddle1 = Paddle(self.dis, 1)
        self.paddle2 = Paddle(self.dis, 2)
        self.ball = Ball(self.dis, [self.paddle1, self.paddle2])

    def save_best(self, best):
        with open("src/ai/best_ai.pickle", "wb") as f:
            pickle.dump(best, f)

    def load_best(self):
        with open("src/ai/best_ai.pickle", "rb") as f:
            best_ai = pickle.load(f)

            return best_ai

    def get_mode(self):
        """
        Display for getting one of 3 modes - train, test or standard game.
        """

        pygame.font.init()

        font = pygame.font.Font(None, 60)
        small_font = pygame.font.Font(None, 30)

        text1 = font.render('Pick a mode:', False, colors["white"])
        text2 = font.render('1 = train ai', False, colors["white"])
        text3 = font.render('2 = test ai', False, colors["white"])
        text4 = font.render('3 = standard game', False, colors["white"])
        text5 = small_font.render(
            'Default training generation is set to 50. Change in config/globals.py/generations', False, colors["white"])

        while True:
            self.dis.fill(colors["black"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1

                    if event.key == pygame.K_2:
                        return 2

                    if event.key == pygame.K_3:
                        return 3

            self.dis.blit(text1, [self.dis.get_width() /
                                  3, self.dis.get_height() / 3])
            self.dis.blit(text2, [self.dis.get_width() /
                                  3, self.dis.get_height() / 3 + 40])
            self.dis.blit(text3, [self.dis.get_width() /
                                  3, self.dis.get_height() / 3 + 80])
            self.dis.blit(text4, [self.dis.get_width() /
                                  3, self.dis.get_height() / 3 + 120])
            self.dis.blit(text5, [10, self.dis.get_height() / 3 + 200])

            pygame.display.update()

    def standard_game(self):
        """
        Init for standard game.
        """

        game = Game(self)
        game.player_game()
