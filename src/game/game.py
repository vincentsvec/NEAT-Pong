"""
Main game module
"""
import pygame
from config.globals import screen, colors
from components.paddle import Paddle
from components.ball import Ball


class Game:
    def __init__(self):
        self.dis = pygame.display.set_mode((screen["width"], screen["height"]))
        self.clock = pygame.time.Clock()
        self.paddle1 = Paddle(self.dis, 1)
        self.paddle2 = Paddle(self.dis, 2)
        self.ball = Ball(self.dis, [self.paddle1, self.paddle2])

    def run(self):
        run = True
        event = None

        while run:
            self.dis.fill(colors["black"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.paddle1.update(event)
            self.paddle2.update(event)

            # If game is over ball.update() returns True
            if self.ball.update():
                self.reset()
                self.run()

            pygame.display.update()
            self.clock.tick(screen["fps"])

        pygame.quit()
        quit()

    def reset(self):
        self.paddle1 = Paddle(self.dis, 1)
        self.paddle2 = Paddle(self.dis, 2)
        self.ball = Ball(self.dis, [self.paddle1, self.paddle2])
