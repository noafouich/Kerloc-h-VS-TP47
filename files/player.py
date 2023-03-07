import pygame
from files.ball import Ball


class Player(pygame.sprite.Sprite):
    """
    classe du joueur
    """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 200
        self.max_health = 200
        self.attack = 20
        self.velocity = 5
        self.jump_velocity = 7
        self.image = pygame.image.load("files/images/kerl.png")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400
        self.jump_score = 0
        self.all_ball = pygame.sprite.Group()
        self.orgine_image = self.image
        self.angle = 0

    def update_difficulty(self):
        if self.game.difficulty == 0:
            self.attack = 20
        elif self.game.difficulty == 1:
            self.attack = 15
        elif self.game.difficulty == 2:
            self.attack = 10
        else:
            self.attack = 5

    def shoot_ball(self):
        self.all_ball.add(Ball(self.game))

    def rotate_right(self):
        self.angle -= 12
        self.image = pygame.transform.rotozoom(self.orgine_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate_left(self):
        self.angle += 12
        self.image = pygame.transform.rotozoom(self.orgine_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_right(self):
        self.rect.x += self.velocity
        self.rotate_right()

    def move_left(self):
        self.rect.x -= self.velocity
        self.rotate_left()

    def move_up(self):
        self.rect.y -= self.jump_velocity

    def move_down(self):
        self.rect.y += self.jump_velocity

    def update_health_bar(self, surface):
        # couleur :
        max_bar_color = (97, 148, 73)
        bar_color = (80, 243, 3)
        # position x y et largeur , hauteur
        bar_position = [self.rect.x - 8, self.rect.y - 15, self.health / 4, 10]
        max_bar_position = [self.rect.x - 8, self.rect.y - 15, self.max_health / 4, 10]
        # dessiner la barre
        pygame.draw.rect(surface, max_bar_color, max_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)
