import pygame
from modules import basic_classes
from modules import basic_globals


class SnakePlayer(basic_classes.UpdatableObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.size = kwargs.get('size', 50)
        sprite1 = pygame.Surface((self.size, self.size))
        sprite1.fill(basic_globals.RED)
        sprite2 = pygame.Surface((self.size, self.size))
        sprite2.fill(basic_globals.BLUE)
        self.sprites = [sprite1, sprite2]
        self.animation_speed = 1/60

        self.dir = 'STOP'
        self.vel = self.size
        self.body = [(self.x-self.size, self.y), (self.x-self.size*2, self.y)]
        self.body_color = (150, 40, 40)
        self.updates_per_second = 5
        self.update_limiter = 0

    def update(self, keys):
        super().update(keys)

        if keys[pygame.K_a]:
            self.dir = 'LEFT'
        if keys[pygame.K_d]:
            self.dir = 'RIGHT'
        if keys[pygame.K_w]:
            self.dir = 'UP'
        if keys[pygame.K_s]:
            self.dir = 'DOWN'

        self.update_limiter += self.updates_per_second/self.parent.FPS
        if self.update_limiter >= 1:

            self.update_limiter = 0
            if self.dir != 'STOP':
                self.body.pop(0)
                self.body.append((self.x, self.y))

            if self.dir == 'RIGHT':
                self.x += self.vel
            elif self.dir == 'LEFT':
                self.x -= self.vel
            elif self.dir == 'UP':
                self.y -= self.vel
            elif self.dir == 'DOWN':
                self.y += self.vel

            self.x %= self.parent.WIDTH
            self.y %= self.parent.HEIGHT

        for x, y in self.body:
            if x == self.x and y == self.y:
                self.parent.run = False

    def draw(self, surface):
        super().draw(surface)
        for x, y in self.body:
            pygame.draw.rect(surface, self.body_color, (x, y, self.size, self.size))

    def grow(self):
        self.body.append((self.body[-1]))
