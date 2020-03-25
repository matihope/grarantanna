from modules import \
    basic_classes, \
    basic_globals

from modules.gamemaker_functions import *

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

        if self.tag == 'traktor':
            self.teleporting = False
            self.teleporting_prev = False
            self.vsp = 0
            self.hsp = 0
            self.size = 38
            self.width = 38
            self.height = 38
            self.grv = 0.4
            self.y += 2
            self.teleport_up_speed = -5

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

        if self.tag == 'czesc':
            self.text = ''
            self.font_size = 36
            self.font_color = (227, 197, 56)
            self.font = pygame.font.Font('resources/Born2bSportyV2.ttf', self.font_size)

    def letter_collect(self):
        self.rem()
        self.parent.channel.play(self.parent.sound_zdobycie_punktu)
        print('Player collected letter')

    def rem(self, delay=0):
        if not self.dead:
            self.dead = True
            self.death_count_down = delay

    def update(self, keys):
        super().update(keys)

        if self.tag[:9] == 'wagon':
            self.hsp = self.spd

            for tile in self.parent.game_tiles + [self.parent.player, self.parent.player.gun]:
                if tile == self:
                    continue

                if tile.tag[:9] == 'odbijanie' or tile.tag == 'player' or tile.tag == 'gun':
                    if place_meeting(self.x + self.hsp, self.y, tile, self):
                        while not place_meeting(self.x + sign(self.hsp), self.y, tile, self):
                            self.x += sign(self.hsp)
                        self.hsp = 0
                        self.spd = -self.spd

            self.x += self.hsp

        elif self.tag == 'traktor':
            self.hsp = self.spd
            self.vsp += self.grv

            self.teleporting_prev = self.teleporting
            self.teleporting = False

            for block in self.parent.game_tiles + [self.parent.player]:
                if block == self or block.tag == 'czesc' or block.tag == 'start':
                    continue

                if block.tag != 'player':
                    if place_meeting(self.x + self.hsp, self.y, block, self):
                        while not place_meeting(self.x + sign(self.hsp), self.y, block, self):
                            self.x += sign(self.hsp)
                        self.hsp = 0
                        self.spd = -self.spd

                    if place_meeting(self.x, self.y + self.vsp, block, self):
                        while not place_meeting(self.x, self.y + sign(self.vsp), block, self):
                            self.y += sign(self.vsp)
                        self.vsp = 0

                # Test for the right side of the block
                if place_meeting(self.x + 1, self.y, block, self):
                    if block.tag == 'player':
                        block.lose_hp()

                    if block.tag == 'tp':
                        if place_meeting(self.x + 1, self.y - self.size, block, self) and \
                                place_meeting(self.x + 1, self.y + self.size, block, self):
                            if block.has_portal_on_side('left'):
                                self.teleporting = True
                                b = block.get_opposite()
                                if b is not None and not self.teleporting_prev:
                                    self.teleporting_prev = True
                                    self.tp_self(b, block, 'left')

                # Test for the left side of the block
                if place_meeting(self.x - 1, self.y, block, self):
                    if block.tag == 'player':
                        block.lose_hp()
                    if block.tag == 'tp':
                        if place_meeting(self.x - 1, self.y - self.size, block, self) and \
                                place_meeting(self.x - 1, self.y + self.size, block, self):
                            if block.has_portal_on_side('right'):
                                self.teleporting = True
                                b = block.get_opposite()
                                if b is not None and not self.teleporting_prev:
                                    self.teleporting_prev = True
                                    self.tp_self(b, block, 'right')

                # Test for block's head
                if place_meeting(self.x, self.y - 1, block, self):
                    if block.tag == 'player' and not block.drawing_death_animation:
                        self.rem(100)
                        self.parent.channel.play(self.parent.sound_zabicie_traktora)
                        self.spd = 0
                    if block.tag == 'tp':
                        if place_meeting(self.x+self.size, self.y - 1, block, self) and \
                                place_meeting(self.x-self.size, self.y - 1, block, self):
                            if block.has_portal_on_side('bottom'):
                                self.teleporting = True
                                b = block.get_opposite()
                                if b is not None and not self.teleporting_prev:
                                    self.teleporting_prev = True
                                    self.tp_self(b, block, 'bottom')

                # Test for block's feet
                if place_meeting(self.x, self.y + 1, block, self):
                    if block.tag == 'tp':
                        if place_meeting(self.x+self.size, self.y + 1, block, self) and \
                                place_meeting(self.x-self.size, self.y + 1, block, self):
                            if block.has_portal_on_side('top'):

                                self.teleporting = True
                                b = block.get_opposite()
                                if b is not None and not self.teleporting_prev:
                                    self.teleporting_prev = True
                                    self.tp_self(b, block, 'top')

            self.x += self.hsp
            self.y += self.vsp
            if not 0 <= self.x <= self.parent.WIDTH or not 0 <= self.y <= self.parent.HEIGHT:
                self.rem()

        self.death_count_down = max(0, self.death_count_down-9)
        if self.dead and self.death_count_down == 0:
            self.parent.remove_obj(self)
            self.parent.game_tiles.remove(self)

    def get_opposite(self):
        if len(self.colored_sides) > 0:
            opposite_block = [blk for blk in self.parent.game_tiles if blk.tag == 'tp' and len(blk.colored_sides) > 0]
            if len(self.colored_sides) < 2:
                opposite_block.remove(self)

            if len(opposite_block) > 0:
                return opposite_block[0]
        return None

    def make_portal(self, side, color):
        if self.tag == 'tp':
            for s in self.colored_sides:
                if s[0] == side:
                    self.colored_sides.remove(s)

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

    def tp_self(self, block, block_original, current):
        dest = 'right'

        sides = ['right', 'left', 'bottom', 'top']
        if block == block_original:
            sides = [s for s in sides if s != current]

        for side in sides:
            if block.has_portal_on_side(side):
                dest = side
                break

        if dest == 'top':
            self.vsp = min(self.vsp, self.teleport_up_speed)

        if dest == 'right':
            self.x = block.x + block.width + 5
            self.y = block.y + block.height // 2 - self.height // 2
        elif dest == 'left':
            self.x = block.x - self.width - 5
            self.y = block.y + block.height // 2 - self.height // 2
        elif dest == 'top':
            self.x = block.x + block.width // 2 - self.width // 2
            self.y = block.y - self.height - 5
        elif dest == 'bottom':
            self.x = block.x + block.width // 2 - self.width // 2
            self.y = block.y + block.height + 5

        if (current == 'right' and dest == 'left') or (current == 'left' and dest == 'right'):
            self.spd = -self.spd

    def draw(self, surface):
        if self.tag == 'traktor':
            if self.visible and len(self.sprites) > 0:
                index = min(int(self.sprite_index), len(self.sprites) - 1)
                surface.blit(pygame.transform.flip(self.sprites[index], True if sign(self.hsp) == -1 else False, False),
                             (self.x, self.y-1))
                self.sprite_index += self.animation_speed
                self.sprite_index %= len(self.sprites)
        else:
            super().draw(surface)

        if self.tag == 'czesc':
            text = self.font.render(self.text, True, self.font_color)
            x = self.x + self.width//2 - text.get_width()/2
            y = self.y + self.height//2 - text.get_height()/2
            surface.blit(text, (x, y))

        elif self.tag == 'tp':
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
