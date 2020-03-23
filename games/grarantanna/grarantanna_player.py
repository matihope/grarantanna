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
        self.size = kwargs.get('size', 20)
        surf = pygame.Surface((20, 20))
        surf.fill(basic_globals.BG_COLOR)
        pygame.draw.circle(surf, (200, 200, 200), (10, 10), self.size//2)
        # surf.blit(pygame.image.load(os.path.join('resources', 'pilkaB.png')), (0, 0))
        self.sprites = [surf]
        self.spd = 2.2

        self.grv = 0.4
        self.hsp = 0
        self.vsp = 0
        self.on_ground = False
        self.on_boost = False
        self.jump = -7
        self.power_jump = -11.3

        self.gun = Gun(owner=self, x=self.x, y=self.y)
        
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
            if block.tag == 'start':
                continue

            if self.vsp == 0 and self.hsp == 0:
                break

            elif block.tag == 'kolce':
                if place_meeting(self.x + hsp, self.y, block, self) or \
                        place_meeting(self.x, self.y + vsp, block, self):
                    self.lose_hp()
                    # self.parent.run = False

            else:  # For every other blockaa
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
                        hsp = 0

                # Test for the left side of the player
                if place_meeting(self.x - 1, self.y, block, self):
                    if block.tag == 'magnes_prawo' or block.tag == 'magnes_wszystko':
                        self.hsp = 0
                        hsp = 0

                # Test for player's head
                if place_meeting(self.x, self.y - 1, block, self):
                    if block.tag == 'magnes_dol' or block.tag == 'magnes_wszystko':
                        self.vsp = 0
                        vsp = 0

                # Test for player's feet
                if place_meeting(self.x, self.y + 1, block, self):
                    if block.tag == 'magnes_gora' or block.tag == 'magnes_wszystko':
                        self.vsp = 0
                        vsp = 0

                    if block.tag == 'trojkat_gora':
                        self.on_boost = True
                    self.on_ground = True

                    if block.tag == 'zamiana':
                        block.tag = 'kwadrat'
                        self.spd *= -1

                    if block.tag == 'znikajacy_kwadrat':
                        block.remove()

        if self.vsp > 0:
            # Falling
            self.on_ground = False
            self.on_boost = False

        self.x += hsp
        self.y += vsp

        if not 0 <= self.x <= self.parent.WIDTH or \
           not 0 <= self.y <= self.parent.HEIGHT:
            self.lose_hp()

    def lose_hp(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vsp = 0
        self.hsp = 0
        self.gun.x = self.x
        self.gun.y = self.y
        self.on_boost = False
        self.on_ground = False


class Gun(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = kwargs.get('owner', None)
        self.color = (50, 200, 60)
        self.size = 4
        self.default_distance = 0.5

        self.hsp = 0
        self.vsp = 0

    def update(self, keys):
        super().update(keys)
        m_x, m_y = self.parent.mouse.get_pos()
        d = point_direction(self.x, self.y, m_x, m_y)
        self.hsp = ((self.owner.x+self.owner.size/2) - self.x) / 10 * self.parent.delta_time
        self.vsp = ((self.owner.y+self.owner.size/2) - self.y) / 10 * self.parent.delta_time
        self.hsp += length_dir_x(self.default_distance, d)
        self.vsp += -length_dir_y(self.default_distance, d)

        if self.parent.mouse.get_pressed()[0]:
            # Shot
            self.hsp = -length_dir_x(5, d)
            self.vsp = length_dir_y(5, d)

        for block in self.parent.game_tiles:
            if self.hsp == 0 and self.vsp == 0:
                break
            if block.tag == 'start':
                continue

            if place_meeting(self.x + self.hsp, self.y, block, self):
                while not place_meeting(self.x + self.hsp, self.y, block, self):
                    self.hsp -= sign(self.hsp)
                self.hsp = 0

            if place_meeting(self.x, self.y + self.vsp, block, self):
                while not place_meeting(self.x, self.y + self.vsp, block, self):
                    self.vsp -= sign(self.vsp)
                self.vsp = 0

        self.x += self.hsp
        self.y += self.vsp

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)



