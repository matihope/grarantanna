import pygame
from games.grarantanna import grarantanna_game

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Grarantanna v0.1')


def main():
    game = grarantanna_game.Grarantanna(width=WIDTH, height=HEIGHT)

    clock = pygame.time.Clock()
    while game.run:
        game.update(clock.tick())
        game.draw()
        win.blit(game.get_surface(), (0, 0))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    game.run = False


if __name__ == '__main__':
    pygame.init()
    print(pygame.display.Info())
    main()
    pygame.quit()
