import pygame
from modules import basic_classes
from modules import basic_globals
from modules.gamemaker_functions import *

import os


class Player(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_x = self.x
        self.start_y = self.y
        surf = pygame.Surface((20, 20))
        surf.fill(basic_globals.BG_COLOR)
        pygame.draw.circle(surf, (200, 200, 200), (10, 10), 10)
        # surf.blit(pygame.image.load(os.path.join('resources', 'pilkaB.png')), (0, 0))
        self.sprites = [surf]
        self.size = kwargs.get('size', 20)
        self.spd = 2.2

        self.grv = 0.4
        self.hsp = 0
        self.vsp = 0
        self.on_ground = False
        self.on_boost = False
        self.jump = -7
        self.power_jump = -11.3
        
    def update(self, keys):
        super().update(keys)

        self.hsp = (int(keys[pygame.K_d]) - int(keys[pygame.K_a])) * self.spd

        self.vsp += self.grv * self.parent.delta_time
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vsp = self.jump if not self.on_boost else self.power_jump
            self.on_ground = False
            self.on_boost = False

        hsp = self.hsp * self.parent.delta_time
        vsp = self.vsp * self.parent.delta_time

        # Collision handling
        for block in self.parent.game_tiles:

            if block.tag == 'trojkat' or block.tag == 'kwadrat' or block.tag[:6] == 'magnes':
                if place_meeting(self.x + hsp, self.y, block, self):
                    while not place_meeting(self.x + sign(self.hsp), self.y, block, self):
                        self.x += sign(self.hsp)
                    self.hsp = 0
                    hsp = 0

                if place_meeting(self.x, self.y + vsp, block, self):
                    while not place_meeting(self.x, self.y + sign(self.vsp), block, self):
                        self.y += sign(self.vsp)
                    self.vsp = 0
                    vsp = 0
                
                # Test for the right side of the player
                if place_meeting(self.x + 1, self.y, block, self):
                    if block.tag == 'magnes_lewo' or block.tag == 'magnes_wszystko':
                        self.hsp = 0

                # Test for the left side of the player
                if place_meeting(self.x - 1, self.y, block, self):
                    if block.tag == 'magnes_prawo' or block.tag == 'magnes_wszystko':
                        self.hsp = 0

                # Test for player's head
                if place_meeting(self.x, self.y - 1, block, self):
                    if block.tag == 'magnes_dol' or block.tag == 'magnes_wszystko':
                        self.vsp = 0

                # Test for player's feet
                if place_meeting(self.x, self.y + 1, block, self):
                    if block.tag == 'magnes_gora' or block.tag == 'magnes_wszystko':
                        self.vsp = 0

                    if block.tag == 'trojkat':
                        self.on_boost = True
                    self.on_ground = True

            elif block.tag == 'kolce':
                if place_meeting(self.x + hsp, self.y, block, self) or \
                        place_meeting(self.x, self.y + vsp, block, self):
                    self.x = self.start_x
                    self.y = self.start_y
                    self.vsp = 0
                    self.hsp = 0
                    hsp = 0
                    vsp = 0
                    self.on_boost = False
                    self.on_ground = False
                    # self.parent.run = False

            if self.hsp == 0 and self.vsp == 0:
                # If player is stopped
                break

        if self.vsp > 0:
            # Falling
            self.on_ground = False
            self.on_boost = False

        self.x += hsp
        self.y += vsp
