from modules import \
    basic_classes, \
    basic_globals, \
    gamemaker_functions as gmf

import pygame
import os


class Block(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spd = 1.5
        self.dead = False
        self.size = kwargs.get('size', 40)
        self.width = self.size
        self.height = self.size
        self.tag = kwargs.get('tag', 'DEFAULT')  # tag types { BLOCK, SPIKE, START, END }
        self.death_count_down = 0

        if self.tag == 'tp':
            self.colored_sides = []  # 0 == 'right', 1 == 'bottom', 2 == 'left', 3 == 'top'
            self.portal_sprites_blue = []
            self.portal_sprites_yellow = []
            for i in range(4):
                blue_surf = pygame.Surface((self.width, self.height))
                blue_surf.fill(basic_globals.BG_COLOR)
                blue_img = pygame.image.load(os.path.join('resources/portal_sprites', f'blue{i}.png'))
                blue_surf.blit(blue_img, (0, 0))

                yellow_surf = blue_surf.copy()
                yellow_surf.fill(basic_globals.BG_COLOR)
                yellow_img = pygame.image.load(os.path.join('resources/portal_sprites', f'yellow{i}.png'))
                yellow_surf.blit(yellow_img, (0, 0))
                self.portal_sprites_blue.append(blue_img)
                self.portal_sprites_yellow.append(yellow_img)

    def rem(self, delay=0):
        if not self.dead:
            self.dead = True
            self.death_count_down = delay

    def update(self, keys):
        super().update(keys)

        if self.tag[:9] == 'wagon':
            self.hsp = self.spd * self.parent.delta_time

            for tile in self.parent.game_tiles + [self.parent.player, self.parent.player.gun]:
                if tile == self:
                    continue

                if tile.tag[:9] == 'odbijanie' or tile.tag == 'player' or tile.tag == 'gun':
                    if gmf.place_meeting(self.x + self.hsp, self.y, tile, self):
                        while not gmf.place_meeting(self.x + gmf.sign(self.hsp), self.y, tile, self):
                            self.x += gmf.sign(self.hsp)
                        self.hsp = 0
                        self.spd = -self.spd

                if tile.tag[:9] == 'odbijanie' or tile.tag == 'player' or tile.tag == 'gun':
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

    def make_portal(self, side, color):
        if self.tag == 'tp':
            if len(self.colored_sides) == 2:
                # remove one portal and add a new one
                self.colored_sides.pop(0)
            self.colored_sides.append((side, color))

    def remove_portal(self, color):
        if self.tag == 'tp':
            for side in self.colored_sides:
                if side[1] == color:
                    self.colored_sides.remove(side)

    def has_portal_on_side(self, side):
        for sd, color in self.colored_sides:
            if sd == side:
                return True
        return False

    def draw(self, surface):
        super().draw(surface)

        if self.tag == 'tp':
            for side, color in self.colored_sides:
                index = 0
                if side == 'right':
                    index = 0
                elif side == 'bottom':
                    index = 1
                elif side == 'left':
                    index = 2
                elif side == 'top':
                    index = 3

                if color == 'blue':
                    surface.blit(self.portal_sprites_blue[index], (self.x, self.y))
                else:
                    surface.blit(self.portal_sprites_yellow[index], (self.x, self.y))

        # # Top
        # pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, 3))
        # # Bottom
        # pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y + self.height - 3, self.width, 3))
        # # Right
        # pygame.draw.rect(surface, (255, 0, 0), (self.x+self.width-3, self.y, 3, self.height))
        # # Left
        # pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 3, self.height))
