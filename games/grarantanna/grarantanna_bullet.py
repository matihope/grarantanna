import pygame
from modules import basic_classes
from modules import basic_globals
from modules.gamemaker_functions import *


class Bullet(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = kwargs.get('speed', 1)
        self.direction = kwargs.get('direction', 1)
        self.portal_color = kwargs.get('portal_color', 'blue')

        self.size = kwargs.get('size', 6)

        surf = pygame.Surface((self.size, self.size))
        surf.fill((0, 178, 255) if self.portal_color == 'blue' else (249, 240, 7))

        self.sprites = [surf]

        self.hsp = length_dir_x(self.speed, self.direction)
        self.vsp = -length_dir_y(self.speed, self.direction)

        self.touched = False
        self.touched_block = None
        self.touched_side = ''  # left, right, top, bottom
        self.outside_the_game = False

    def update(self, keys):

        if not self.touched:
            self.hsp -= length_dir_x(0.25, 90)
            self.vsp -= -length_dir_y(0.25, 90)

        for block in self.parent.game_tiles:
            if block.tag == 'start' or block.tag == 'czesc':
                continue

            if place_meeting(self.x + self.hsp, self.y, block, self):
                self.touched_block = block
                self.touched = True
                self.touched_side = 'left' if sign(self.hsp) == 1 else 'right'
                self.hsp = 0
                self.vsp = 0
                break

            if place_meeting(self.x, self.y + self.vsp, block, self):
                self.touched_block = block
                self.touched = True
                self.touched_side = 'top' if sign(self.vsp) == 1 else 'bottom'
                self.vsp = 0
                self.hsp = 0
                break

        self.x += self.hsp
        self.y += self.vsp

        if not 0 <= self.x <= self.parent.WIDTH or not 0 <= self.y <= self.parent.HEIGHT:
            self.outside_the_game = True

    def draw(self, surface):
        surface.blit(self.sprites[self.sprite_index], (self.x, self.y))
