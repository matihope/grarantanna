from modules import \
    basic_classes, \
    basic_globals

import pygame


class Block(basic_classes.DrawableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprites = [kwargs.get('texture', None)]
        # x = pygame.Surface((40, 40))
        # x.fill((255, 255, 20))
        # self.sprites = [x]
        self.size = kwargs.get('size', 40)
        self.tag = kwargs.get('tag', 'DEFAULT')  # tag types { BLOCK, SPIKE, START, END }
