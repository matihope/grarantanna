import pygame
from modules import basic_classes
from modules import basic_globals
from modules.gamemaker_functions import *
from games.grarantanna import grarantanna_bullet


class Gun(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = kwargs.get('owner', None)
        self.color = (50, 200, 60)
        self.size = 6
        self.default_distance = 0.5

        self.hsp = 0
        self.vsp = 0

        self.mouse_pressed_before = False
        self.remaining_reload = 0
        self.bullet = None
        self.tag = 'gun'

    def update(self, keys):
        super().update(keys)
        m_x, m_y = self.parent.mouse.get_pos()
        d = point_direction(self.x, self.y, m_x, m_y)
        self.hsp = ((self.owner.x+self.owner.size/2) - self.x) / 10 * self.parent.delta_time
        self.vsp = ((self.owner.y+self.owner.size/2) - self.y) / 10 * self.parent.delta_time
        self.hsp += length_dir_x(self.default_distance, d)
        self.vsp += -length_dir_y(self.default_distance, d)

        if self.bullet is not None:
            if self.bullet.outside_the_game or self.bullet.touched:
                if self.bullet.touched:
                    self.bullet.touched_block.make_portal(self.bullet.touched_side, self.bullet.portal_color)
                # Removing
                self.parent.remove_obj(self.bullet)
                self.bullet = None

        # Shooting
        mouse_press = self.parent.mouse.get_pressed()
        if (mouse_press[0] or mouse_press[2]) and not self.mouse_pressed_before and self.bullet is None and \
                not self.owner.drawing_death_animation:
            self.hsp = -length_dir_x(20, d)
            self.vsp = length_dir_y(20, d)
            x = self.x + self.size // 2
            y = self.y + self.size // 2
            d = point_direction(x, y, m_x, m_y)
            portal_color = 'blue' if mouse_press[0] else 'yellow'
            self.remove_portal_from_blocks(color=portal_color)
            self.bullet = grarantanna_bullet.Bullet(direction=d, speed=5, x=x, y=y-3, portal_color=portal_color)
            self.parent.add_updatable(self.bullet, draw_order=2)
        self.mouse_pressed_before = mouse_press[0] or mouse_press[2]

        for block in self.parent.game_tiles:
            if self.hsp == 0 and self.vsp == 0:
                break
            if block.tag == 'start'or block.tag == 'czesc':
                continue

            if place_meeting(self.x + self.hsp, self.y, block, self):
                while place_meeting(self.x + self.hsp, self.y, block, self):
                    self.hsp -= sign(self.hsp)/10

            if place_meeting(self.x, self.y + self.vsp, block, self):
                while place_meeting(self.x, self.y + self.vsp, block, self):
                    self.vsp -= sign(self.vsp)/10

        if not self.owner.drawing_death_animation:
            self.x += self.hsp
            self.y += self.vsp

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    def remove_portal_from_blocks(self, color):
        [block.remove_portal(color) for block in self.parent.game_tiles if block.tag == 'tp']
