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
        self.teleported_player = None

        self.gun = grarantanna_gun.Gun(owner=self, x=self.x, y=self.y)
        
    def update(self, keys):
        super().update(keys)

        if keys[pygame.K_t]:
            self.x, self.y = self.parent.mouse.get_pos()

        # If player died
        if self.drawing_death_animation:
            self.vsp += self.grv * self.parent.delta_time
            self.y += self.vsp * self.parent.delta_time
            self.animation_speed = 1
            if self.y > self.parent.HEIGHT:
                self.reset_vars()
            return

        # Basic movement
        self.hsp = (int(keys[pygame.K_d]) - int(keys[pygame.K_a])) * self.spd
        self.vsp += self.grv * self.parent.delta_time

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

        hsp = self.hsp * self.parent.delta_time
        vsp = self.vsp * self.parent.delta_time

        self.animation_speed = 0.6 * self.parent.delta_time * sign(self.hsp)

        # Collision handling
        for block in self.parent.game_tiles:
            if block.tag == 'start' or block.tag == 'czesc':
                continue

            if self.vsp == 0 and self.hsp == 0:
                break

            else:  # For every other block
                if place_meeting(self.x + hsp, self.y, block, self):
                    while not place_meeting(self.x + sign(self.hsp), self.y, block, self):
                        self.x += sign(self.hsp)
                    self.is_flying = False
                    self.hsp = 0
                    hsp = 0

                if place_meeting(self.x, self.y + vsp, block, self):
                    while not place_meeting(self.x, self.y + sign(self.vsp), block, self):
                        self.y += sign(self.vsp)

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
                        if block.has_portal_on_side('left'):
                            print('Touching portal left')

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
                        if block.has_portal_on_side('right'):
                            print('Touching portal right')
                            #
                            # b = block.get_opposite()
                            # if b is not None:
                            #     if not self.teleporting:
                            #         self.teleported_x = b.x
                            #         self.teleported_y = b.y
                            #
                            #     if b.has_portal_on_side('bottom'):
                            #         self.teleported_hsp = self.vsp
                            #         self.teleported_vsp = self.hsp
                            #     elif b.has_portal_on_side('top'):
                            #         self.teleported_hsp = self.vsp
                            #         self.teleported_vsp = self.hsp
                            #     elif b.has_portal_on_side('right'):
                            #         self.teleported_hsp = -self.hsp
                            #         self.teleported_vsp = self.vsp
                            #     elif b.has_portal_on_side('left'):
                            #         self.teleported_hsp = self.hsp
                            #         self.teleported_vsp = self.vsp
                            # self.teleporting = True

                # Test for player's head
                if place_meeting(self.x, self.y - 1, block, self):
                    if block.tag == 'magnes_dol' or block.tag == 'magnes_wszystko':
                        self.vsp = 0
                        vsp = 0
                        # if keys[pygame.K_SPACE]:
                        #     vsp = 0.1

                    if block.tag == 'tp':
                        if block.has_portal_on_side('bottom'):
                            print('Touching portal bottom')

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
                        block.rem(delay=400)

                    if block.tag == 'znikajacy_kwadrat':
                        block.rem(delay=200)

                    if block.tag == 'leci_lewo':
                        self.is_flying = True
                        self.flying_speed = -abs(self.flying_speed)
                        self.x = block.x-self.size
                        self.y = block.y + block.size // 2 - self.size // 2

                    if block.tag == 'leci_prawo':
                        self.is_flying = True
                        self.flying_speed = abs(self.flying_speed)
                        self.x = block.x + block.size
                        self.y = block.y + block.size // 2 - self.size // 2

                    if block.tag == 'tp':
                        if place_meeting(self.x+self.size, self.y + 1, block, self) and \
                           place_meeting(self.x-self.size, self.y + 1, block, self):
                            if block.has_portal_on_side('top'):
                                print('Touching portal top')

                                b = block.get_opposite()
                                if b is not None and not self.teleporting:
                                    self.teleporting = True
                                    p = TeleportedPlayer(self, 'top', block, b)
                                    self.parent.add_updatable(p)

        if self.vsp > 0:
            # Falling
            self.on_ground = False
            self.on_boost = False

        self.x += hsp
        self.y += vsp

        # If on the edge of the screen
        if not 0 <= self.x <= self.parent.WIDTH or \
           not 0 <= self.y <= self.parent.HEIGHT:
            self.lose_hp()

    def lose_hp(self):
        # What happens when dies
        self.vsp = -7
        self.drawing_death_animation = True

    def reset_vars(self):
        self.x = self.start_x
        self.y = self.start_y
        self.vsp = 0
        self.hsp = 0
        self.gun.x = self.x
        self.gun.y = self.y
        self.spd = abs(self.spd)
        self.on_boost = False
        self.on_ground = False
        self.parent.reset_level()
        self.drawing_death_animation = False


class TeleportedPlayer(basic_classes.UpdatableObj):
    def __init__(self, player, original_side, original_block, opposite_block, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_player = player
        self.original_block = original_block
        self.original_side = original_side
        self.opposite_block = opposite_block

        self.sprites = self.original_player.sprites

        for side in ['right', 'left', 'bottom', 'top']:
            if self.opposite_block.has_portal_on_side(side):
                self.destinated_side = side
                break

        if self.destinated_side == 'right':
            offset_x = abs(self.original_player.x - self.original_block.x)
            offset_y = abs(self.original_player.y - self.original_block.y)
            self.x = -offset_x + self.opposite_block.x + self.opposite_block.width - self.original_player.width
            self.y = self.opposite_block.y + self.opposite_block.height - offset_y - self.original_player.height

        self.hsp = 0
        self.vsp = 0

    def update(self, keys):
        super().update(keys)

        self.sprite_index = self.original_player.sprite_index

        hsp = self.original_player.hsp
        vsp = self.original_player.vsp
        if self.original_side == 'right':
            if self.destinated_side == 'right':
                self.hsp = -hsp
                self.vsp = vsp
            elif self.destinated_side == 'top':
                self.vsp = hsp
                self.hsp = vsp
            elif self.destinated_side == 'bottom':
                self.vsp = -hsp
                self.hsp = -vsp
        elif self.original_side == 'left':
            if self.destinated_side == 'left':
                self.hsp = -hsp
                self.vsp = vsp
            elif self.destinated_side == 'top':
                self.hsp = -vsp
                self.vsp = -hsp
            elif self.destinated_side == 'bottom':
                self.hsp = -vsp
                self.vsp = hsp
        elif self.original_side == 'top':
            if self.destinated_side == 'top':
                self.hsp = hsp
                self.vsp = -vsp
            elif self.destinated_side == 'right':
                self.hsp = vsp
                self.vsp = -hsp
            elif self.destinated_side == 'left':
                self.hsp = -vsp
                self.vsp = vsp
        elif self.original_side == 'bottom':
            if self.destinated_side == 'bottom':
                self.hsp = hsp
                self.vsp = -vsp
            elif self.destinated_side == 'right':
                self.hsp = -vsp
                self.vsp = hsp
            elif self.destinated_side == 'left':
                self.hsp = vsp
                self.vsp = -hsp

        hsp = self.hsp * self.parent.delta_time
        vsp = self.vsp * self.parent.delta_time

        for block in self.parent.game_tiles:
            if block.tag == 'start' or block.tag == 'czesc' or block == self.original_block or block == self.opposite_block:
                continue

            if self.vsp == 0 and self.hsp == 0:
                break

            else:  # For every other block
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

        self.x += hsp
        self.y += vsp


