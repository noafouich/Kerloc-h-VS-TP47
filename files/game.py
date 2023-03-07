from random import randint
import math
import pygame
from files.player import Player
from files.boss import Boss


class Game:
    """
    classe du jeu
    """

    def __init__(self, sound_manager):
        self.difficulty = 0
        self.sound_manager = sound_manager
        # jeu en cours
        self.game_is_in_progress = False
        # générer le jeu
        self.player = Player(self)
        self.pressed = {}
        self.boss = Boss(self)
        self.temp = 0
        self.donnee = False
        self.temp_collide = 0

    def restart(self):
        self.player.health = self.player.max_health
        self.boss.health = self.boss.max_health
        self.boss.phase = 1
        self.boss.rect.x = 550
        self.boss.rect.y = 350
        self.player.rect.x = 100
        self.player.rect.y = 400

    def check_collision(self, sprite1, sprite2):
        return pygame.sprite.collide_mask(sprite1, sprite2)

    def check_collition_group(self, group1, group):
        return pygame.sprite.groupcollide(group1, group, True, True)

    def update_game(self, screen, background, fps):
        # afficher l'arrière plan
        screen.blit(background, (0, 0))
        # afficher les donnees :
        font = pygame.font.Font("files/other/police donnees.ttf", 16)
        if self.donnee:
            fps_text = font.render(f"FPS : {math.ceil(fps)}", True, (255, 0, 0))
            screen.blit(fps_text, (10, 10))
            co_y = font.render(f"coordonnée y : {self.player.rect.y}", True, (255, 0, 0))
            screen.blit(co_y, (10, 30))
            co_x = font.render(f"coordonnée x : {self.player.rect.x}", True, (255, 0, 0))
            screen.blit(co_x, (10, 50))
            health = font.render(f"health : {self.player.health} / {self.player.max_health}", True, (255, 0, 0))
            screen.blit(health, (10, 70))
            boss_health = font.render(f"boss health : {self.boss.health} / {self.boss.max_health}", True, (255, 0, 0))
            screen.blit(boss_health, (10, 90))
        # joueur mort ?
        if self.player.health <= 0:
            self.boss.rect.y = 15000
            self.player.rect.y = 10000
            for ball in self.player.all_ball:
                ball.remove()
            for ball_boss in self.boss.all_ball_boss:
                ball_boss.remove()
            self.temp += 1
            if self.temp == 1:
                self.sound_manager.play("perdu")
            if self.temp != 230:
                screen.blit(pygame.image.load("files/images/game_over.png"), (0, 0))
            elif self.temp == 230:
                self.temp = 0
                self.game_is_in_progress = False

        # mettre à jour la difficulté pour les statstiques
        self.boss.update_difficulty()
        self.player.update_difficulty()
        for ball_boss in self.boss.all_ball_boss:
            ball_boss.update_difficulty()

        # afficher le boss ou le faire mourrir
        if self.boss.health > 0:
            screen.blit(self.boss.image, self.boss.rect)
            self.boss.update_health_bar(screen)
        if self.boss.health <= 0:
            self.boss.boss_kill = 1
        if self.boss.health <= 0 and self.boss.boss_kill == 1:
            self.boss.rect.y = 10000
            self.player.rect.y = 10000
            for ball in self.player.all_ball:
                ball.remove()
            for ball_boss in self.boss.all_ball_boss:
                ball_boss.remove()
            self.temp += 1
            if self.temp == 1:
                self.sound_manager.play('gagne')
            if self.temp != 200:
                screen.blit(pygame.image.load("files/images/victoire.png"), (0, 0))
            elif self.temp == 200:
                self.temp = 0
                self.game_is_in_progress = False
        # collition et dégat joueur , boss
        if pygame.sprite.collide_mask(self.player, self.boss) and self.boss.phase != 4:
            if self.difficulty == 0:
                self.player.health -= 0.5
            elif self.difficulty == 1:
                self.player.health -= 1
            elif self.difficulty == 2:
                self.player.health -= 0.5
            else:
                self.player.health -= 1.5

        elif pygame.sprite.collide_mask(self.player,
                                        self.boss) and self.boss.phase == 4 and self.player.health < self.player.max_health:
            self.player.health += 1
        else:
            self.temp_collide = 0

        # collition ball et ball boss
        if self.difficulty == 0:
            self.check_collition_group(self.boss.all_ball_boss, self.player.all_ball)

        # joueur vivant
        if self.player.health > 0:
            screen.blit(self.player.image, self.player.rect)
            self.player.update_health_bar(screen)
        if self.player.health <= 0:
            self.player.boss_kill = 1
        if self.player.health <= 0 and self.player.boss_kill == 1:
            self.player.rect.y = 10000
        # afficher le joueur
        screen.blit(self.player.image, self.player.rect)

        # déplacer le joueur
        if self.pressed.get(
                pygame.K_RIGHT) and self.player.rect.x + self.player.velocity < 720 - self.player.rect.width:
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x - self.player.velocity > 0:
            self.player.move_left()

        # jump
        if self.pressed.get(pygame.K_SPACE) and self.player.jump_score == 0:
            self.player.jump_score = 1
        if self.player.jump_score == 1:
            self.player.jump_velocity -= 0.16
            self.player.move_up()
        if self.player.rect.y < 200:
            self.player.jump_score = 2
        if self.player.jump_score == 2:
            self.player.jump_velocity += 0.16
            self.player.move_down()
        if self.player.rect.y > 400:
            self.player.jump_score = 0
            self.player.jump_velocity = 7

        # recupére les balles du joueur
        for ball in self.player.all_ball:
            if self.check_collision(ball, self.boss):
                ball.remove()
            if self.check_collision(ball, self.boss) and self.boss.phase != 3 and self.boss.phase != 4:
                self.boss.health -= self.player.attack
            else:
                ball.move_right()
            if ball.rect.x >= 720:
                ball.remove()
        # recupére les balles du boss
        for ball_boss in self.boss.all_ball_boss:
            if self.check_collision(ball_boss, self.player):
                x = randint(0, 2)
                if x == 0:
                    self.sound_manager.play("aie")
                elif x == 1:
                    self.sound_manager.play("outch")
                else:
                    self.sound_manager.play("ouie")
                self.player.health -= self.boss.attack
                ball_boss.remove()
            else:
                ball_boss.move_left()
            if ball_boss.rect.x >= 720:
                ball_boss.remove()

        # affiche les balles
        self.player.all_ball.draw(screen)
        self.boss.all_ball_boss.draw(screen)

        # deplacement du boss phase 1
        if self.boss.phase == 1:
            if self.boss.phase11 == 0:
                self.boss.rect.x = 550
                self.boss.rect.y = 350
                self.boss.phase11 = 1
                self.boss.image = pygame.image.load("files/images/boss1.png")
            self.boss.boss_phase1()

        # deplacement du boss phase 2
        if self.boss.phase == 2:
            if self.boss.phase22 == 0:
                self.boss.rect.x = 550
                self.boss.rect.y = 350
                self.boss.phase22 = 1
                self.boss.image = pygame.image.load("files/images/boss5.png")
            self.boss.boss_phase2()

        # deplacement du boss phase 3
        R = 0
        if self.boss.phase == 3 and not self.player.health <= 0:
            if self.boss.tp_phase != 5:
                self.boss.image = pygame.image.load("files/images/boss4.png")
                self.boss.tp_phase2 += 1
                if self.boss.tp_phase2 == 70:
                    self.boss.rect.x = self.player.rect.x - 35
                    self.boss.rect.y = self.player.rect.y - 35
                    if self.check_collision(self.player, self.boss):
                        R += 1
                    if R == 1:
                        self.sound_manager.play("aaaaaah")
                    self.boss.tp_phase2 = 0
                    self.boss.tp_phase += 1
                    R = 0
            else:
                self.boss.tp_phase = 0
                self.boss.phase = 1

        # deplacement du boss phase 4
        if self.boss.phase == 4:
            if self.boss.tp_phase_heal != 4:
                self.boss.image = pygame.image.load("files/images/boss2.png")
                self.boss.tp_phase_heal2 += 1
                if self.boss.tp_phase_heal2 == 70:
                    self.boss.rect.x = randint(0, 660)
                    self.boss.rect.y = randint(200, 380)
                    self.boss.tp_phase_heal2 = 0
                    self.boss.tp_phase_heal += 1
            else:
                self.boss.phase = 2
                self.boss.tp_phase_heal = 0
