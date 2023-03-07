import pygame


class BallBoss(pygame.sprite.Sprite):

    def __init__(self, boss, game):
        super().__init__()
        self.game = game
        self.health = 200
        self.boss = boss
        self.max_health = 200
        self.velocity = 3
        self.image = pygame.image.load("files/images/ball1.png")
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = self.boss.rect.x
        self.rect.y = self.boss.rect.y + 50

    def update_difficulty(self):
        if self.game.difficulty == 0 or self.game.difficulty == 1:
            self.velocity = 3
        elif self.game.difficulty == 2:
            self.velocity = 4
        else:
            self.velocity = 5

    def remove(self):
        self.boss.all_ball_boss.remove(self)

    def move_left(self):
        self.rect.x -= self.velocity
