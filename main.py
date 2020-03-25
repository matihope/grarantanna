import pygame
from games.grarantanna import grarantanna_game

WIDTH, HEIGHT = 1200, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Grarantanna v0.4')


def main():
    game = grarantanna_game.Grarantanna(width=WIDTH, height=HEIGHT, fps=60)
    menu = grarantanna_game.Menu(width=WIDTH, height=HEIGHT, game=game)
    level_select = grarantanna_game.LevelSelect(width=WIDTH, height=HEIGHT, game=game)
    settings = grarantanna_game.Settings(width=WIDTH, height=HEIGHT, game=game)
    stop = grarantanna_game.Stop(width=WIDTH, height=HEIGHT, game=game)
    settings_in_game = grarantanna_game.Settings_in_game(width=WIDTH, height=HEIGHT, game=game)

    clock = pygame.time.Clock()
    while game.run:
        if game.show_screen == 0:  # Menu
            menu.update(clock.tick(game.FPS))
            menu.draw()
            screen = menu.get_surface()
        elif game.show_screen == 1:  # Game
            game.update(clock.tick(game.FPS))
            game.draw()
            screen = game.get_surface()
        elif game.show_screen == 2:  # Select level
            level_select.update(clock.tick(game.FPS))
            level_select.draw()
            screen = level_select.get_surface()
        elif game.show_screen == 3:  # Settings
            settings.update(clock.tick(game.FPS))
            settings.draw()
            screen = settings.get_surface()
        elif game.show_screen == 4:  # Stop
            stop.update(clock.tick(game.FPS))
            stop.draw()
            screen = stop.get_surface()
        elif game.show_screen == 5:  # Setings in game
            settings_in_game.update(clock.tick(game.FPS))
            settings_in_game.draw()
            screen = settings_in_game.get_surface()

        win.blit(screen, (0, 0))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if game.show_screen == 4:
                        game.show_screen = 1
                    elif game.show_screen == 1:
                        game.show_screen = 4
                    elif game.show_screen == 3:
                        game.show_screen = 0
                    elif game.show_screen == 2:
                        game.show_screen = 0


if __name__ == '__main__':
    pygame.init()
    print(pygame.display.Info())
    main()
    pygame.quit()
