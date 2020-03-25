import pygame
from modules import basic_classes
from modules import basic_globals
from modules.gamemaker_functions import *
from modules import gamemaker_functions as gmf
import os

from games.grarantanna import grarantanna_button

class Slider(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = kwargs.get('text', '')
        self.width = kwargs.get('width', 400)
        self.height = kwargs.get('height', 140)
        self.x = kwargs.get('x', 100)
        self.y = kwargs.get('y', 100)

        self.value = kwargs.get('value', 10)
        self.value_max = kwargs.get('value_max', 50)
        self.slider_color = kwargs.get('slider_color', (255, 255, 255))

        self.target = kwargs.get('target', None)
        self.bg_color = kwargs.get('bg_color', (50, 50, 50))
        self.font_name = kwargs.get('font_name', '')
        self.font_size = kwargs.get('font_size', 40)
        self.font_color = kwargs.get('font_color', (227, 197, 56))
        self.font_grow_ratio = kwargs.get('font_grow_ratio', 1.2)

        self.s1 = pygame.Surface((self.width, self.height))
        self.s1.fill(self.bg_color)
        self.img1 = pygame.image.load(os.path.join(f'resources/slider{kwargs.get("folder_index", 0)}', f'slider0.png'))
        self.s1.blit(self.img1, (0, 45))

        self.s2_width = 75
        self.s2_height = 48

        self.s2_x = (self.width - self.s2_width) * self.value/self.value_max
        self.s2_y = 46
        self.s2 = pygame.Surface((self.s2_width, self.s2_height))
        self.s2.fill(basic_globals.BG_COLOR)
        img = pygame.image.load(os.path.join(f'resources/slider{kwargs.get("folder_index", 0)}', f'slider1.png'))
        self.s2.blit(img, (0, 0))

        self.pressed = True
        

    def draw(self, surface):
        self.s1.blit(self.img1, (0, 45))
        self.s1.blit(self.s2,(self.s2_x, self.s2_y))

        font = pygame.font.SysFont(self.font_name, self.font_size)
        rendered = font.render(self.text , True, self.font_color)
        pos = self.width//2 - rendered.get_width()//2, 0
        self.s1.blit(rendered, pos)
    
        s34 = pygame.Surface((self.width, 40))
        s34.fill(self.bg_color)
        font = pygame.font.SysFont(self.font_name, self.font_size)
        rendered = font.render(str(self.value) , True, self.font_color)
        pos = self.width//2 - rendered.get_width()//2, 100
        self.s1.blit(s34, (0, 100))
        self.s1.blit(rendered, pos)

        surface.blit(self.s1, (self.x - self.width//2, self.y))

    def update(self, keys):
        super().update(keys)
        self.s2_x = (self.width - self.s2_width) * self.value/self.value_max
        self.value = max(self.value, 0)
        self.value = min(self.value, self.value_max )
        mouse_x, mouse_y = self.parent.mouse.get_pos()

        if gmf.point_in_rectangle(mouse_x, mouse_y, self.x + self.s2_x - self.width//2, self.y + self.s2_y, self.s2_width, self.s2_height) and self.parent.mouse.get_pressed() == (1, 0, 0):
            self.pressed = True
        elif self.parent.mouse.get_pressed() != (1, 0, 0):  
            self.pressed = False

        if self.pressed:
            if gmf.point_in_rectangle(mouse_x, mouse_y, self.x + self.s2_x - self.width//2, self.y + self.s2_y, self.s2_width, self.s2_height) :
                self.value = (mouse_x - self.x + self.width//2) / self.width * self.value_max
                self.value = round(self.value)

            if mouse_y > self.y + self.s2_y and mouse_y < self.y + self.s2_y + self.s2_height:
                if (mouse_x - self.x + self.width//2) > self.width:
                    self.value = self.value_max
                if (mouse_x - self.x + self.width//2) < 0:
                    self.value = 0
