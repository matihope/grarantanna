from modules import \
    basic_classes, \
    basic_globals

import pygame
from threading import Thread


class Block(basic_classes.DrawableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = kwargs.get('size', 40)
        self.tag = kwargs.get('tag', 'DEFAULT')  # tag types { BLOCK, SPIKE, START, END }
        self.dead = False

    def remove(self):
        if not self.dead:
            self.dead = True
            s = Thread(target=self.__remove)
            s.start()

    def __remove(self):
        pygame.time.delay(200)
        self.parent.game_tiles.remove(self)
        self.parent.remove_obj(self)
