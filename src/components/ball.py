"""
module for ball
"""
import pygame
import random
from config.globals import ball_conf


class Ball:
    def __init__(self, surface, paddles):
        self.dis = surface
        self.paddles = paddles
        self.radius = ball_conf["radius"]
        self.color = ball_conf["color"]
        self.speed = ball_conf["speed"]
        self.posx = self.dis.get_width() / 2
        self.posy = self.dis.get_height() / 2
        self.vectorX, self.vectorY = self.generate_vector()
        self.paddle_hits = [0, 0]
        self.paddle_miss = [0, 0]

    def update(self):
        """
        Updates all properties of ball. Returns True if game is over.
        """
        self.draw()
        collision, missed_paddle = self.check_collision()

        if collision:
            return True, missed_paddle

        self.move()

        return None, None

    def draw(self):
        """
        Draws the ball.
        """
        self.rect = pygame.draw.circle(self.dis, self.color, [
            self.posx, self.posy], self.radius, self.radius)

    def move(self):
        """
        Moves the ball by adding the vecors to positon of the ball.
        """
        self.posx += self.vectorX
        self.posy += self.vectorY

    def generate_vector(self):
        """
        Randomly generates initial vectors.
        """
        x = random.choice((-self.speed, self.speed))
        y = random.choice((-self.speed, self.speed))
        return x, y

    def check_collision(self):
        """
        Checks for different collisions. If ball hits the returns True if game is over.
        Returns which paddle missed the ball to evaluate genomes.
        """

        # ball hits the upper or bottom wall
        if self.posy <= 0 or self.posy >= self.dis.get_height():
            self.vectorY *= -1

        # ball hits the paddle
        for player, paddle in enumerate(self.paddles):
            if paddle.get_rect().colliderect(self.rect):
                self.vectorX *= -1
                self.paddle_hits[player] += 1

        # ball hits left or right wall
        if self.posx <= 0:
            self.paddle_miss[0] += 1
            return True, self.paddle_miss

        elif self.posx >= self.dis.get_width():
            self.paddle_miss[1] += 1
            return True, self.paddle_miss

        return None, None
