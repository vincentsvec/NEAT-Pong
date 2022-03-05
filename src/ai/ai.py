"""
Ai module
"""
import neat
from game.game import Game
import pickle


class AI():
    def __init__(self, config):
        self.config = config

    def run(self):
        # uncomment next line to resume training from checkpoint
        pop = neat.Checkpointer.restore_checkpoint("neat-checkpoint-12")

        #pop = neat.Population(self.config)
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
        pop.add_reporter(neat.Checkpointer(1))

        winner = pop.run(self.eval_genomes, 50)

    def eval_genomes(self, genomes, _):
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
        self.network1 = neat.nn.FeedForwardNetwork.create(
            self.genome1, self.config)
        self.network2 = neat.nn.FeedForwardNetwork.create(
            self.genome2, self.config)

        self.game = Game(self)
        self.game.run()

    def get_decision(self):
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
        if positive:
            self.genome1.fitness += paddle_hits_miss[0]
            self.genome2.fitness += paddle_hits_miss[1]

        else:
            self.genome1.fitness -= paddle_hits_miss[0]
            self.genome2.fitness -= paddle_hits_miss[1]

        print(self.genome1.fitness, self.genome2.fitness)
