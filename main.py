import pygame
from pygame.locals import *
from games.grarantanna import grarantanna_game

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))  # , HWSURFACE | DOUBLEBUF | RESIZABLE)
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
        win.blit(game.get_surface(), (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
