import pygame
from modules import basic_classes
from modules import basic_globals
from modules.gamemaker_functions import *
from games.grarantanna import grarantanna_gun
import os


class Player(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = 'player'

        # Starting vars
        self.start_x = self.x
        self.start_y = self.y
        for sprite in range(12):
            surf = pygame.Surface((self.size, self.size))
            surf.fill(basic_globals.BG_COLOR)
            surf.blit(pygame.image.load(os.path.join('resources/plyta', f'plyta{sprite+1}.png')), (0, 0))
            self.sprites.append(surf)
        self.spd = 2.2

        self.grv = 0.4
        self.hsp = 0
        self.vsp = 0
        self.on_ground = False
        self.on_boost = False
        self.jump = -7
        self.power_jump = -11.3
        self.drawing_death_animation = False

        self.is_flying = False
        self.flying_speed = 3
        self.is_kicked_sideways = False
        self.kick_sideways_speed = 3
        self.teleporting = False
        self.teleporting_prev = False
        self.teleport_up_speed = -5
        self.moving_from_prev = 1

        self.collected_strings = []
        self.collected_strings_string = ''
        self.collect_indicator_offset_x = 25

        self.gun = grarantanna_gun.Gun(owner=self, x=self.x+3, y=self.y+3)

    def update(self, keys):
        super().update(keys)

        self.teleporting_prev = self.teleporting
        self.teleporting = False

        # Delete that
        if keys[pygame.K_t]:
            self.x, self.y = self.parent.mouse.get_pos()
            self.hsp, self.vsp = 0, 0

        # If player died
        if self.drawing_death_animation:
            self.vsp += self.grv
            self.y += self.vsp
            self.animation_speed = 1
            if self.y > self.parent.HEIGHT:
                self.reset_vars()
                self.parent.reset_level()
            return

        # Basic movement
        self.hsp = (int(keys[pygame.K_d]) - int(keys[pygame.K_a])) * self.spd * self.moving_from_prev
        if self.hsp == 0:
            self.moving_from_prev = 1
        self.vsp += self.grv

        # If player is flying
        if self.is_flying:
            self.hsp = self.flying_speed
            self.vsp = 0
            self.is_kicked_sideways = False
        elif self.is_kicked_sideways:
            self.hsp = self.kick_sideways_speed

        # Jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            if not self.is_flying:
                self.vsp = self.jump if not self.on_boost else self.power_jump
            self.is_flying = False
            self.on_ground = False
            self.on_boost = False

        if self.vsp < -15:
            self.vsp = -15
        elif self.vsp > 15:
            self.vsp = 15

        hsp = self.hsp
        vsp = self.vsp

        self.animation_speed = 0.6 * sign(self.hsp)

        # Collision handling
        for block in self.parent.game_tiles:
            if block.tag == 'start':
                continue

            if self.vsp == 0 and self.hsp == 0:
                break

            else:  # For every other block
                if block.tag != 'czesc':
                    if place_meeting(self.x + hsp, self.y, block, self):
                        while not place_meeting(self.x + sign(self.hsp), self.y, block, self):
                            self.x += sign(self.hsp)
                            if not 0 <= self.x <= self.parent.WIDTH:
                                break
                        self.is_flying = False
                        self.hsp = 0
                        hsp = 0

                    if place_meeting(self.x, self.y + vsp, block, self):
                        while not place_meeting(self.x, self.y + sign(self.vsp), block, self):
                            self.y += sign(self.vsp)
                            if not 0 <= self.y <= self.parent.HEIGHT:
                                break

                        self.vsp = 0
                        vsp = 0
                        self.is_kicked_sideways = False

                # Test for the right side of the player
                if place_meeting(self.x + 1, self.y, block, self):
                    if block.tag == 'magnes_lewo' or block.tag == 'magnes_wszystko':
                        self.hsp = 0
                        hsp = 0

                    if block.tag == 'zabija_lewo':
                        self.lose_hp()

                    if block.tag == 'trojkat_lewo':
                        self.is_kicked_sideways = True
                        self.kick_sideways_speed = -abs(self.kick_sideways_speed)

                    if block.tag == 'tp':
                        if place_meeting(self.x + 1, self.y - self.size, block, self) and \
                                place_meeting(self.x + 1, self.y + self.size, block, self):
                            if block.has_portal_on_side('left'):
                                self.teleporting = True
                                b = block.get_opposite()
                                if b is not None and not self.teleporting_prev:
                                    self.teleporting_prev = True
                                    self.tp_self(b, block, 'left')

                    if block.tag == 'czesc':
                        self.collected_strings.append(block.text)
                        block.letter_collect()
                        continue

                # Test for the left side of the player
                if place_meeting(self.x - 1, self.y, block, self):
                    if block.tag == 'magnes_prawo' or block.tag == 'magnes_wszystko':
                        self.hsp = 0
                        hsp = 0

                    if block.tag == 'zabija_prawo':
                        self.lose_hp()

                    if block.tag == 'trojkat_prawo':
                        self.is_kicked_sideways = True
                        self.kick_sideways_speed = abs(self.kick_sideways_speed)

                    if block.tag == 'tp':
                        if place_meeting(self.x - 1, self.y - self.size, block, self) and \
                                place_meeting(self.x - 1, self.y + self.size, block, self):
                            if block.has_portal_on_side('right'):
                                self.teleporting = True
                                b = block.get_opposite()
                                if b is not None and not self.teleporting_prev:
                                    self.teleporting_prev = True
                                    self.tp_self(b, block, 'right')

                    if block.tag == 'czesc':
                        self.collected_strings.append(block.text)
                        block.letter_collect()
                        continue

                # Test for player's head
                if place_meeting(self.x, self.y - 1, block, self):
                    if block.tag == 'magnes_dol' or block.tag == 'magnes_wszystko':
                        self.vsp = 0
                        vsp = 0
                        # if keys[pygame.K_SPACE]:
                        #     vsp = 0.1

                    if block.tag == 'tp':
                        if place_meeting(self.x+self.size, self.y - 1, block, self) and \
                                place_meeting(self.x-self.size, self.y - 1, block, self):
                            if block.has_portal_on_side('bottom'):
                                self.teleporting = True
                                b = block.get_opposite()
                                if b is not None and not self.teleporting_prev:
                                    self.teleporting_prev = True
                                    self.tp_self(b, block, 'bottom')

                    if block.tag == 'czesc':
                        self.collected_strings.append(block.text)
                        block.letter_collect()
                        continue

                # Test for player's feet
                if place_meeting(self.x, self.y + 1, block, self):
                    self.on_ground = True
                    if block.tag == 'magnes_gora' or block.tag == 'magnes_wszystko':
                        self.vsp = 0
                        vsp = 0

                    if block.tag == 'kolce':
                        self.lose_hp()

                    elif block.tag == 'trojkat_gora':
                        self.on_boost = True

                    elif block.tag == 'zamiana':
                        block.tag = 'kwadrat'
                        self.spd *= -1
                        block.rem(delay=500)

                    if block.tag == 'znikajacy_kwadrat':
                        block.rem(delay=200)

                    if block.tag == 'leci_lewo':
                        self.is_flying = True
                        self.flying_speed = -abs(self.flying_speed)
                        self.x = block.x-self.size
                        self.y = block.y + block.size // 2 - self.size // 2
                        self.gun.x = self.x + self.gun.size//2
                        self.gun.y = self.y + self.gun.size//2

                    if block.tag == 'leci_prawo':
                        self.is_flying = True
                        self.flying_speed = abs(self.flying_speed)
                        self.x = block.x + block.size
                        self.y = block.y + block.size // 2 - self.size // 2

                    if block.tag == 'tp':
                        if place_meeting(self.x+self.size, self.y + 1, block, self) and \
                                place_meeting(self.x-self.size, self.y + 1, block, self):
                            if block.has_portal_on_side('top'):

                                self.teleporting = True
                                b = block.get_opposite()
                                if b is not None and not self.teleporting_prev:
                                    self.on_ground = False
                                    self.teleporting_prev = True
                                    self.tp_self(b, block, 'top')

                        if block.tag == 'czesc':
                            self.collected_strings.append(block.text)
                            block.letter_collect()
                            continue

        if self.vsp > 0:
            # Falling
            self.on_ground = False
            self.on_boost = False

        self.x += hsp
        self.y += vsp

        print(self.collected_strings)

        # If on the edge of the screen
        if not 0 <= self.x <= self.parent.WIDTH or \
                not 0 <= self.y <= self.parent.HEIGHT:
            self.lose_hp()

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

        self.moving_from_prev = 1
        if (current == 'right' and dest == 'right') or (current == 'left' and dest == 'left'):
            self.moving_from_prev = -1

        self.gun.x = self.x + self.gun.size//2
        self.gun.y = self.y + self.gun.size//2

    def reset_vars(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vsp = 0
        self.hsp = 0

        self.gun.x = self.x + self.gun.size//2
        self.gun.y = self.y + self.gun.size//2

        self.spd = abs(self.spd)
        self.on_boost = False
        self.on_ground = False
        self.drawing_death_animation = False

    def lose_hp(self):
        # What happens when dies
        self.vsp = -7
        self.drawing_death_animation = True
