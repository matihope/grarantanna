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
        self.align_x = kwargs.get('align_x', 'center')
        self.align_y = kwargs.get('align_y', 'center')
        self.draw_x = self.x - self.width // 2  # Default align_x='center'
        self.draw_y = self.y - self.height // 2  # Default align_y='center'
        if self.align_x == 'left':
            self.draw_x = self.x
        elif self.align_x == 'right':
            self.draw_x = self.x - self.width
        if self.align_y == 'top':
            self.draw_y = self.y
        elif self.align_y == 'bottom':
            self.draw_y = self.y - self.height

        self.target = kwargs.get('target', None)
        self.bg_color = kwargs.get('bg_color', (50, 50, 50))
        self.font_name = kwargs.get('font_name', 'resources/Born2bSportyV2.ttf')
        self.font_size = kwargs.get('font_size', 32)
        self.font_color = kwargs.get('font_color', (227, 197, 56))
        self.font_grow_ratio = kwargs.get('font_grow_ratio', 1.2)
        s1 = pygame.Surface((self.width, self.height))
        s2 = s1.copy()
        s3 = s1.copy()
        s1.fill(self.bg_color)
        s2.fill(self.bg_color)
        s3.fill(self.bg_color)
        self.sprites = [s1, s2, s3]
        for i in range(len(self.sprites)):
            img = pygame.image.load(os.path.join(f'resources/button{kwargs.get("folder_index", 0)}', f'button{i}.png'))
            self.sprites[i].blit(img, ((self.width-img.get_width())/2, (self.height-img.get_height())/2))

        self.pressed_before = False
        self.pressed = False
        self.long_press = kwargs.get('long_press', False)

    def update(self, keys):
        self.sprite_index = 0
        mouse_press = self.parent.mouse.get_pressed()[0]
        mouse_x, mouse_y = self.parent.mouse.get_pos()
        self.pressed_before = self.pressed
        self.pressed = False
        if gmf.point_in_rectangle(mouse_x, mouse_y, self.draw_x, self.draw_y, self.width, self.height):
            self.sprite_index = 1
            if mouse_press and self.target is not None:
                self.sprite_index = 2
                self.pressed = True
            if self.pressed_before and not self.pressed:
                self.parent.game.channel.play(self.parent.game.sound_przyciski_menu)
                self.target()

    def draw(self, surface):
        if self.visible and len(self.sprites) > 0:
            # self.sprite_index += self.animation_speed
            self.sprite_index %= len(self.sprites)
            surface.blit(self.sprites[int(self.sprite_index)], (self.draw_x, self.draw_y))

        font = pygame.font.Font(self.font_name, self.font_size if self.sprite_index == 0 else int(self.font_size*self.font_grow_ratio))
        rendered = font.render(self.text, True, self.font_color)
        pos = self.draw_x + self.width//2 - rendered.get_width()//2, \
              self.draw_y + self.height//2 - rendered.get_height()//2
        surface.blit(rendered, pos)

