import pygame
import random
from modules import basic_classes


class Fruit(basic_classes.DrawableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = kwargs.get('size', 50)
        sprite1 = pygame.Surface((self.size, self.size))
        sprite1.fill((200, 200, 50))
        self.sprites = [sprite1]

    def kill(self):
        self.x = random.randrange(self.parent.WIDTH//self.size) * self.size
        self.y = random.randrange(self.parent.HEIGHT//self.size) * self.size
