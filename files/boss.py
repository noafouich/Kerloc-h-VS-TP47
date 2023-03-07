import pygame
from files.ball_boss import BallBoss
from random import *


class Boss(pygame.sprite.Sprite):
    """
    classe du boss
    """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.boss_kill = 0
        self.health = 1000
        self.max_health = 1000
        self.attack = 20
        self.velocity = 1
        self.image = pygame.image.load("files/images/boss1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 550
        self.rect.y = 350
        self.all_ball_boss = pygame.sprite.Group()
        # variable de temporisation
        self.phase = 1
        self.phase1 = 0
        self.phase11 = 0
        self.phase111 = 0
        self.phase2 = 0
        self.phase22 = 0
        self.phase222 = 0
        self.tp_phase = 0
        self.tp_phase2 = 0
        self.tp_phase_heal = 0
        self.tp_phase_heal2 = 0

    def update_health_bar(self, surface):
        # couleur :
        bar_color = (255, 0, 0)
        max_bar_color = (255, 255, 0)
        # position x y et largeur , hauteur
        bar_position = [self.rect.x, self.rect.y + 10, self.health / 10, 10]
        max_bar_position = [self.rect.x, self.rect.y + 10, self.max_health / 10, 10]
        # dessiner la barre
        pygame.draw.rect(surface, max_bar_color, max_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)

    def update_difficulty(self):
        if self.game.difficulty == 0 or self.game.difficulty == 1:
            self.attack = 20
        elif self.game.difficulty == 2:
            self.attack = 27
        else:
            self.attack = 40
        if self.game.difficulty == 0:
            self.velocity = 1
        elif self.game.difficulty == 1:
            self.velocity = 1.5
        elif self.game.difficulty == 2:
            self.velocity = 2.5
        else:
            self.velocity = 4

    def shoot_ball(self):
        ballboss = BallBoss(self, self.game)
        self.all_ball_boss.add(ballboss)

    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def move_up(self):
        self.rect.y -= self.velocity

    def move_down(self):
        self.rect.y += self.velocity

    def boss_phase1(self):
        if self.phase111 != 2:
            if self.phase1 == 0:
                self.move_up()
            if self.rect.y <= 100 and self.phase1 == 0:
                self.phase1 = 1
            if self.phase1 == 1:
                self.move_down()
            if self.rect.y >= 350 and self.phase1 == 1:
                self.phase1 = 0
                self.phase111 += 1
        else:
            self.phase1 = 0
            self.phase11 = 0
            self.phase111 = 0
            if self.game.difficulty == 0:
                self.phase = 1
            elif self.game.difficulty == 1 or self.game.difficulty == 2:
                self.phase = 2
            else:
                self.phase = 4

        # tir de boss phase1
        random_shoot = randint(1, 35)
        if random_shoot == 1:
            self.shoot_ball()

    def boss_phase2(self):
        if self.phase222 != 2:
            if self.phase2 == 0:
                self.move_up()
                self.move_left()
            if self.rect.x <= 200 and self.phase2 == 0:
                self.phase2 = 1
            if self.phase2 == 1:
                self.move_down()
                self.move_right()
            if self.rect.x >= 550 and self.phase2 == 1:
                self.phase2 = 0
                self.phase222 += 1
        else:
            self.phase2 = 0
            self.phase22 = 0
            self.phase222 = 0
            if self.game.difficulty == 1:
                self.phase = 1
            elif self.game.difficulty == 2:
                self.phase = 3
            else:
                self.phase = 3

        # tir de boss phase2
        random_shoot = randint(1, 35)
        if random_shoot == 1:
            self.shoot_ball()

    def boss_move(self):
        if self.rect.x == 720:
            x = randint(2, 4)
        elif self.rect.y == 480:
            x = randint(1, 3)
        else:
            x = x = randint(1, 4)
        if x == 1:
            self.move_right()
        elif x == 4:
            self.move_left()
        elif x == 3:
            self.move_up()
        elif x == 2:
            self.move_down()