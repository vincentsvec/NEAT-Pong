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

    def run(self):
        run = True
        event = None
        paddle_miss = [0, 0]

        while run:
            self.dis.fill(colors["black"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.paddle1.update(event)
            self.paddle2.update(event)

            # If game is over ball.update() returns True
            game_over, missed_paddle = self.ball.update()
            if game_over:
                if missed_paddle == "right":
                    paddle_miss[1] += 0.2
                elif missed_paddle == "left":
                    paddle_miss[0] += 0.2

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
            self.clock.tick(screen["fps"])

    def reset(self):
        self.paddle1 = Paddle(self.dis, 1)
        self.paddle2 = Paddle(self.dis, 2)
        self.ball = Ball(self.dis, [self.paddle1, self.paddle2])
