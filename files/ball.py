import pygame
import math

class Ball(pygame.sprite.Sprite):
    """
    classe des balles
    """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.velocity = 13
        self.image = pygame.image.load("files/images/tp.png")
        self.rect = self.image.get_rect()
        self.rect.x = game.player.rect.x + 30
        self.rect.y = game.player.rect.y

    def remove(self):
        self.game.player.all_ball.remove(self)

    def move_right(self):
        self.rect.x += self.velocity
