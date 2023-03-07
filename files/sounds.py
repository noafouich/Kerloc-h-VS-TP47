import pygame


class SoundManager:
    def __init__(self):
        self.sounds = {
            "aaaaaah": pygame.mixer.Sound("files/sounds/Aaaaaah-_.ogg"),
            "aie": pygame.mixer.Sound("files/sounds/Aie-__1.ogg"),
            "Bonjour": pygame.mixer.Sound("files/sounds/Bonjour !.ogg"),
            "gagne": pygame.mixer.Sound("files/sounds/gagne.ogg"),
            "outch": pygame.mixer.Sound("files/sounds/outch !!.ogg"),
            "ouie": pygame.mixer.Sound("files/sounds/ouie.ogg"),
            "perdu": pygame.mixer.Sound("files/sounds/perdu.ogg")
        }
        self.music = {

        }

    def play(self, name):
        self.sounds[name].play()
