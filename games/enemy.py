import pygame
from modules import basic_classes
from modules import basic_globals


class Enemy(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sprite1 = pygame.Surface((50, 150))
        sprite1.fill(basic_globals.RED)
        self.sprites = [
            sprite1
        ]

        self.animation_speed = 1

    def update(self):
        super().update()
