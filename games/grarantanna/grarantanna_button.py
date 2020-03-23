import pygame
from modules import basic_classes
from modules import basic_globals
from modules.gamemaker_functions import *
from modules import gamemaker_functions as gmf
import os


class Button(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = kwargs.get('text', '')
        self.width = kwargs.get('width', 150)
        self.height = kwargs.get('height', 50)
        self.color1 = kwargs.get('color1', (255, 255, 255))
        self.color2 = kwargs.get('color2', (200, 200, 200))
        self.color3 = kwargs.get('color3', (150, 150, 150))
        self.font_color = kwargs.get('font_color', (50, 50, 50))
        self.target = kwargs.get('target', None)
        self.font = pygame.font.SysFont(kwargs.get('font_name', ''), kwargs.get('font_size', 36))
        s1 = pygame.Surface((self.width, self.height))
        s2 = s1.copy()
        s3 = s1.copy()
        s1.fill(self.color1)
        s2.fill(self.color2)
        s3.fill(self.color3)
        self.sprites = [s1, s2, s3]

        self.pressed_before = False
        self.pressed = False

    def update(self, keys):
        self.sprite_index = 0
        mouse_press = self.parent.mouse.get_pressed()[0]
        mouse_x, mouse_y = self.parent.mouse.get_pos()
        self.pressed_before = self.pressed
        self.pressed = False
        if gmf.point_in_rectangle(mouse_x, mouse_y, self.x, self.y, self.width, self.height):
            self.sprite_index = 1
            if mouse_press and self.target is not None:
                if not self.pressed_before:
                    self.target()
                self.sprite_index = 2
                self.pressed = True

    def draw(self, surface):
        super().draw(surface)
        rendered = self.font.render(self.text, True, self.font_color)
        pos = self.x + self.width//2 - rendered.get_width()//2, self.y + self.height//2 - rendered.get_height()//2
        surface.blit(rendered, pos)

