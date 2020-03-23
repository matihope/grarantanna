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

    def rem(self, delay=0):
        if not self.dead:
            self.dead = True
            s = Thread(target=self.__remove_delay, args=(delay,))
            s.start()

    def __remove_delay(self, delay):
        pygame.time.delay(delay)
        self.parent.game_tiles.remove(self)
        self.parent.remove_obj(self)
