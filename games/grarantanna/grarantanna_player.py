import pygame
from modules import basic_classes
from modules import basic_globals
from modules import gamemaker_functions as gmf

import os


class Player(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_x = self.x
        self.start_y = self.y
        x = pygame.Surface((20, 20))
        x.fill(basic_globals.BG_COLOR)
        x.blit(pygame.image.load(os.path.join('resources', 'pilkaB.png')), (0, 0))
        self.sprites = [x]
        self.size = kwargs.get('size', 20)
        self.spd = 2.25

        self.grv = 0.4
        self.hsp = 0
        self.vsp = 0
        self.on_ground = False
        self.on_boost = False
        self.jump = -7
        self.power_jump = -11.2

    def update(self, keys):
        super().update(keys)

        self.hsp = (int(keys[pygame.K_d]) - int(keys[pygame.K_a])) * self.spd

        self.vsp += self.grv
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vsp = self.jump if not self.on_boost else self.power_jump
            self.on_ground = False
            self.on_boost = False

        # Collision handling
        for block in self.parent.game_tiles:
            if self.hsp == 0 and self.vsp == 0:
                break

            if block.tag == 'trojkat' or block.tag == 'kwadrat':
                if gmf.place_meeting(self.x + self.hsp, self.y, block, self):
                    while not gmf.place_meeting(self.x + gmf.sign(self.hsp), self.y, block, self):
                        self.x += gmf.sign(self.hsp)
                    self.hsp = 0

                if gmf.place_meeting(self.x, self.y + self.vsp, block, self):
                    while not gmf.place_meeting(self.x, self.y + gmf.sign(self.vsp), block, self):
                        self.y += gmf.sign(self.vsp)
                    self.vsp = 0
                    if gmf.place_meeting(self.x, self.y + 1, block, self):
                        if block.tag == 'trojkat':
                            self.on_boost = True
                        self.on_ground = True

            elif block.tag == 'kolce':
                if gmf.place_meeting(self.x + self.hsp, self.y, block, self) or \
                        gmf.place_meeting(self.x, self.y + self.vsp, block, self):
                    self.x = self.start_x
                    self.y = self.start_y
                    self.vsp = 0
                    self.hsp = 0
                    self.on_boost = False
                    self.on_ground = False

        if self.vsp > 0:
            # Falling
            self.on_ground = False
            self.on_boost = False

        self.x += self.hsp
        self.y += self.vsp
