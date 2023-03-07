from random import randint
import pygame
import time
from files.game import Game
from files.ball import *
from files.sounds import SoundManager

fps = 0
pygame.init()

pygame.display.set_caption("Kerloc'h VS TP47")
screen = pygame.display.set_mode((720, 480))

running = True
# importer l'arriere plan
background = pygame.image.load("files/images/background.png")

# importer l'arriere plan du menu
background_menu = pygame.image.load("files/images/menu.png")

# importation de bouton jouer
play_button = pygame.image.load("files/images/bouton_jouer.png")
play_button_rect = play_button.get_rect()
play_button_rect.x = 160
play_button_rect.y = 400

# importation des boutons de difficultés
difficulty_button = pygame.image.load("files/images/bouton_facile.png")
difficulty_button_rect = difficulty_button.get_rect()
difficulty_button_rect.x = 160
difficulty_button_rect.y = 300
# charger le son
sound_manager = SoundManager()
# charger le jeu
game = Game(sound_manager)
while running:
    t0 = time.time()
    # verifier si le jeu est lancé
    if game.game_is_in_progress:
        game.update_game(screen, background, fps)
    else:
        screen.blit(background_menu, (0, 0))
        screen.blit(play_button, (play_button_rect.x, play_button_rect.y))
        screen.blit(difficulty_button, (difficulty_button_rect.x, difficulty_button_rect.y))

    # actualiser le jeu
    pygame.display.flip()

    for event in pygame.event.get():
        # L'utilisateur quitte le jeu
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # detecter si le joueur enclenche une touche au clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            # detecte pour lancer la balle
            if event.key == pygame.K_a:
                game.player.shoot_ball()
            if event.key == pygame.K_F3:
                if game.donnee:
                    game.donnee = False
                else:
                    game.donnee = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos_x = pygame.mouse.get_pos()[0]
            mouse_pos_y = pygame.mouse.get_pos()[1]
            if play_button_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                game.game_is_in_progress = True
                game.restart()
            elif difficulty_button_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                if game.difficulty == 0:
                    difficulty_button = pygame.image.load("files/images/bouton_normal.png")
                    game.difficulty = 1
                elif game.difficulty == 1:
                    difficulty_button = pygame.image.load("files/images/bouton_difficile.png")
                    game.difficulty = 2
                elif game.difficulty == 2:
                    difficulty_button = pygame.image.load("files/images/bouton_extreme.png")
                    game.difficulty = 3
                elif game.difficulty == 3:
                    difficulty_button = pygame.image.load("files/images/bouton_facile.png")
                    game.difficulty = 0
    # gestion des fps
    tf = time.time() - t0
    try:
        fps = 1/tf
    except:
        fps = 0.00005
    while fps >= 40:
        time.sleep(0.00005)
        tf = time.time() - t0
        fps = 1 / tf

