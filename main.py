import pygame
from games.grarantanna import grarantanna_game

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Grarantanna v0.4')


def main():
    game = grarantanna_game.Grarantanna(width=WIDTH, height=HEIGHT)
    menu = grarantanna_game.Menu(width=WIDTH, height=HEIGHT, game=game)
    level_select = grarantanna_game.LevelSelect(width=WIDTH, height=HEIGHT, game=game)
    settings = grarantanna_game.Settings(width=WIDTH, height=HEIGHT, game=game)

    clock = pygame.time.Clock()
    while game.run:
        if game.show_screen == 0:  # Menu
            menu.update(clock.tick())
            menu.draw()
            screen = menu.get_surface()
        elif game.show_screen == 1:  # Game
            game.update(clock.tick())
            game.draw()
            screen = game.get_surface()
        elif game.show_screen == 2:  # Select level
            level_select.update(clock.tick())
            level_select.draw()
            screen = level_select.get_surface()
        elif game.show_screen == 3:  # Settings
            settings.update(clock.tick())
            settings.draw()
            screen = settings.get_surface()

        win.blit(screen, (0, 0))
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