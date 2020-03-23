from modules import \
    basic_classes, \
    basic_globals, \
    gamemaker_functions as gmf

import pygame


class Block(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spd = 1
        self.dead = False
        self.size = kwargs.get('size', 40)
        self.tag = kwargs.get('tag', 'DEFAULT')  # tag types { BLOCK, SPIKE, START, END }
        self.death_count_down = 0

    def rem(self, delay=0):
        if not self.dead:
            self.dead = True
            self.death_count_down = delay

    def update(self, keys):
        super().update(keys)

        if self.tag[:9] == 'wagon':
            self.hsp = self.spd * self.parent.delta_time

            for tile in self.parent.game_tiles + [self.parent.player]:
                if tile == self:
                    continue

                if tile.tag[:9] == 'odbijanie' or tile.tag == 'player':
                    if gmf.place_meeting(self.x + self.hsp, self.y, tile, self):
                        while not gmf.place_meeting(self.x + gmf.sign(self.hsp), self.y, tile, self):
                            self.x += gmf.sign(self.hsp)
                        self.hsp = 0
                        self.spd = -self.spd

            self.x += self.hsp

        self.death_count_down = max(0, self.death_count_down-12*self.parent.delta_time)
        if self.dead and self.death_count_down == 0:
            self.parent.remove_obj(self)
            self.parent.game_tiles.remove(self)
