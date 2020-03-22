import pygame
import random
import math
from games.grarantanna import grarantanna_game

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Grarantanna')


def main():
    game = grarantanna_game.Grarantanna(width=WIDTH, height=HEIGHT, fps=60)

    clock = pygame.time.Clock()
    while game.run:
        clock.tick(game.FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.run = False

        game.update()
        game.draw()
        x = game.get_surface()
        win.blit(x, (0, 0))  # Real drawing
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
