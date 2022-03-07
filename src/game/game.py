"""
Main game module
"""
import pygame
from config.globals import screen, colors
from components.paddle import Paddle
from components.ball import Ball
import neat


class Game:
    def __init__(self, ai):
        self.ai = ai
        self.dis = pygame.display.set_mode((screen["width"], screen["height"]))
        self.clock = pygame.time.Clock()
        self.paddle1 = Paddle(self.dis, 1)
        self.paddle2 = Paddle(self.dis, 2)
        self.ball = Ball(self.dis, [self.paddle1, self.paddle2])
        self.score = [0, 0]

    def draw_arena(self, score):
        """
        Draws the arena elements
        """
        # draws score
        pygame.font.init()
        font = pygame.font.Font(None, 60)

        score1 = font.render(str(score[0]), False, colors["grey"])
        score2 = font.render(str(score[1]), False, colors["grey"])

        self.dis.blit(score1, [self.dis.get_width() / 4, 20])
        self.dis.blit(score2, [(self.dis.get_width() / 4) * 3, 20])

        # draws the middle line
        for line in range(10):
            pygame.draw.rect(self.dis, colors["grey"], [
                             self.dis.get_width() / 2 - 5, 10 + 50 * line, 10, self.dis.get_height() / 20])

    def run(self):
        """
        Main game loop with ai training.
        """

        run = True
        event = None

        while run:
            self.dis.fill(colors["black"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.paddle1.update(event)
            self.paddle2.update(event)

            # If game is over ball.update() returns True
            game_over, paddle_miss = self.ball.update()
            if game_over:
                self.ai.enum_fitness(False, paddle_miss)
                self.reset()
                run = False

            # find the decision of ai and move the paddle
            decisions = self.ai.get_decision()
            self.paddle1.ai_move(decisions[0])
            self.paddle2.ai_move(decisions[1])

            # if paddle misses the ball it is no longer valid

            if self.ball.paddle_hits[0] >= 1 or self.ball.paddle_hits[1] >= 1 or self.ball.paddle_hits[0] >= 40:
                self.ai.enum_fitness(True, self.ball.paddle_hits)
                run = False

            pygame.display.update()
            self.clock.tick(screen["train_fps"])

    def reset(self):
        """
        Game status reset.
        """

        self.paddle1 = Paddle(self.dis, 1)
        self.paddle2 = Paddle(self.dis, 2)
        self.ball = Ball(self.dis, [self.paddle1, self.paddle2])

    def player_game(self):
        """
        Standard game loop.
        """
        run = True
        event = None

        while run:
            self.dis.fill(colors["black"])
            self.draw_arena(self.score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.paddle1.update(event)
            self.paddle2.update(event)

            game_over, paddle_miss = self.ball.update()
            if game_over:
                if paddle_miss[0] == 1:
                    self.score[1] += 1
                else:
                    self.score[0] += 1

                self.reset()
                self.player_game()

            pygame.display.update()
            self.clock.tick(screen["test_fps"])

        pygame.quit()
        quit()
