import pygame
from modules import basic_classes
from modules import basic_globals
from modules.gamemaker_functions import *
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
        self.flying_speed = -3

        self.gun = Gun(owner=self, x=self.x, y=self.y)
        
    def update(self, keys):
        super().update(keys)

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
                    self.hsp = 0
                    self.is_flying = False
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
                        # if keys[pygame.K_SPACE]:
                        #     vsp = 0.1

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


class Gun(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = kwargs.get('owner', None)
        self.color = (50, 200, 60)
        self.size = 6
        self.default_distance = 0.5

        self.hsp = 0
        self.vsp = 0

        self.remaining_reload = 0
        self.mouse_pressed_before = False
        self.mouse_press = False

        self.bullet = None

    def update(self, keys):
        super().update(keys)
        m_x, m_y = self.parent.mouse.get_pos()
        d = point_direction(self.x, self.y, m_x, m_y)
        self.hsp = ((self.owner.x+self.owner.size/2) - self.x) / 10 * self.parent.delta_time
        self.vsp = ((self.owner.y+self.owner.size/2) - self.y) / 10 * self.parent.delta_time
        self.hsp += length_dir_x(self.default_distance, d)
        self.vsp += -length_dir_y(self.default_distance, d)

        if self.bullet is not None:
            if self.bullet.outside_the_game:
                self.bullet = None
                self.parent.remove_obj(self.bullet)
            elif self.bullet.touched:
                self.bullet = None
                self.parent.remove_obj(self.bullet)

        # Shooting
        self.mouse_pressed_before = self.mouse_press
        self.mouse_press = self.parent.mouse.get_pressed()[0] or self.parent.mouse.get_pressed()[2]
        if self.mouse_press and not self.mouse_pressed_before and self.bullet is None and \
                not self.owner.drawing_death_animation:
            self.hsp = -length_dir_x(20, d)
            self.vsp = length_dir_y(20, d)
            x = self.x + self.size // 2
            y = self.y + self.size // 2
            d = point_direction(x, y, m_x, m_y)
            self.bullet = Bullet(direction=d, speed=5, x=x, y=y)
            self.parent.add_updatable(self.bullet)

        for block in self.parent.game_tiles:
            if self.hsp == 0 and self.vsp == 0:
                break
            if block.tag == 'start'or block.tag == 'czesc':
                continue

            if place_meeting(self.x + self.hsp, self.y, block, self):
                while not place_meeting(self.x + self.hsp, self.y, block, self):
                    self.hsp -= sign(self.hsp)
                self.hsp = 0

            if place_meeting(self.x, self.y + self.vsp, block, self):
                while not place_meeting(self.x, self.y + self.vsp, block, self):
                    self.vsp -= sign(self.vsp)
                self.vsp = 0

        if not self.owner.drawing_death_animation:
            self.x += self.hsp
            self.y += self.vsp

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class Bullet(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = kwargs.get('speed', 1)
        self.direction = kwargs.get('direction', 1)

        self.size = kwargs.get('size', 10)

        surf = pygame.Surface((self.size, self.size))
        surf.fill((255, 0, 0))

        self.sprites = [surf]

        self.hsp = length_dir_x(self.speed, self.direction)
        self.vsp = -length_dir_y(self.speed, self.direction)

        self.touched = False
        self.touched_block_id = None
        self.touched_side = ''  # left, right, top, bottom
        self.outside_the_game = False

    def update(self, keys):

        if not self.touched:
            self.hsp -= length_dir_x(0.1, 90) * self.parent.delta_time
            self.vsp -= -length_dir_y(0.1, 90) * self.parent.delta_time

        for block in self.parent.game_tiles:
            if block.tag == 'start':
                continue

            if place_meeting(self.x + self.hsp, self.y, block, self):
                self.touched_block_id = block
                self.touched = True
                self.hsp = 0
                self.vsp = 0
                break

            if place_meeting(self.x, self.y + self.vsp, block, self):
                self.touched_block_id = block
                self.touched = True
                self.vsp = 0
                self.hsp = 0
                break

        self.x += self.hsp
        self.y += self.vsp

        if 0 <= self.x <= self.parent.WIDTH or 0 <= self.y <= self.parent.HEIGHT:
            self.outside_the_game = True
