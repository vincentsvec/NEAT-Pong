"""
module for paddle
"""
import pygame
from config.globals import paddle_conf


class Paddle:
    def __init__(self, surface, player):
        self.dis = surface
        self.player = player
        self.width = paddle_conf["width"]
        self.height = paddle_conf["height"]
        self.color = paddle_conf["color"]
        self.speed = paddle_conf["speed"]
        self.posx = 10 if player == 1 else self.dis.get_width() - self.width - 10
        self.posy = self.dis.get_height() / 2 - self.height / 2

    def update(self, event):
        """
        Updates all properties of paddle.
        """
        self.draw()
        self.move(event)

    def draw(self):
        """
        Draws the paddle.
        """
        self.rect = pygame.draw.rect(self.dis, self.color, [
            self.posx, self.posy, self.width, self.height])

    def move(self, event):
        """
        Moves the paddles independently, recognisng which paddle to move by player variable.
        """

        keys = pygame.key.get_pressed()

        if self.player == 1:
            if keys[pygame.K_UP] and self.posy > 0:
                self.posy -= self.speed

            if keys[pygame.K_DOWN] and self.posy < self.dis.get_height() - self.height:
                self.posy += self.speed

        elif self.player == 2:
            if keys[pygame.K_w] and self.posy > 0:
                self.posy -= self.speed

            if keys[pygame.K_s] and self.posy < self.dis.get_height() - self.height:
                self.posy += self.speed

    def get_rect(self):
        """
        Returns pygame rectangle object.
        """
        return self.rect

    def ai_move(self, decision):
        """
        Moves paddle according to ai decision.
        """

        if decision == 1 and self.posy > 0:
            self.posy -= self.speed

        elif decision == 2 and self.posy < self.dis.get_height() - self.height:
            self.posy += self.speed
