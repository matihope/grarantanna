import pygame
from modules import \
    basic_classes, \
    basic_globals, \
    game_class, \
    level_reader, block

from games.grarantanna import grarantanna_player, grarantanna_button


class Grarantanna(game_class.Game):
    def __init__(self, width, height, fps=60):
        super().__init__(width, height, fps)
        self.bg_color = basic_globals.BG_COLOR
        self.show_screen = 0
        self.level_name = ''

        self.game_tiles = []
        self.player = None
        self.load_level('poziom1')

    def fix_kolce(self, tile):
        sprite = tile.sprites[0]
        surf = pygame.Surface((40, 20))
        surf.blit(sprite, (0, -15))
        tile.y += 20
        tile.sprites = [surf]

    def reset_level(self):
        for tile in self.game_tiles:
            self.remove_obj(tile)

        self.game_tiles = level_reader.read(self.level_name)
        for tile in self.game_tiles:
            if tile.tag != 'start':
                if tile.tag == 'kolce':
                    self.fix_kolce(tile)
                self.add_updatable(tile)

    def load_level(self, name):
        if self.player is not None:
            self.remove_obj(self.player)
            self.remove_obj(self.player.gun)

        for tile in self.game_tiles:
            self.remove_obj(tile)

        self.game_tiles = level_reader.read(name)
        player_x = 0
        player_y = 0
        for tile in self.game_tiles:
            if tile.tag == 'start':
                player_x, player_y = tile.x, tile.y
            else:
                if tile.tag == 'kolce':
                    self.fix_kolce(tile)
                self.add_updatable(tile)
        self.player = grarantanna_player.Player(x=player_x, y=player_y, size=20)
        self.add_updatable(self.player)
        self.add_updatable(self.player.gun)

        self.level_name = name


class Menu(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_start = grarantanna_button.Button(x=self.WIDTH // 2, y=550, target=self.start, width=240, height=60,
                                                      bg_color=self.bg_color, folder_index=0)

        self.button_select_level = grarantanna_button.Button(x=self.WIDTH // 2, y=625, target=self.select_level,
                                                             width=360, height=60,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_settings = grarantanna_button.Button(x=self.WIDTH // 2, y=700, target=self.settings, width=360,
                                                         height=60,
                                                         bg_color=self.bg_color, folder_index=5)

        self.add_updatable(self.button_start)
        self.add_updatable(self.button_select_level)
        self.add_updatable(self.button_settings)

    def start(self):
        self.game.show_screen = 1

    def select_level(self):
        self.game.show_screen = 2

    def settings(self):
        self.game.show_screen = 3


class LevelSelect(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_back_to_menu = grarantanna_button.Button(x=110, y=35, target=self.menu, width=240, height=60,
                                                             bg_color=self.bg_color, folder_index=3)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 5 * 1, y=250, target=self.select_level_1,
                                                               width=100, height=100,
                                                               bg_color=self.bg_color, folder_index=4)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 5 * 2, y=250, target=self.select_level_2,
                                                               width=100, height=100,
                                                               bg_color=self.bg_color, folder_index=4)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 5 * 3, y=250, target=self.select_level_3,
                                                               width=100, height=100,
                                                               bg_color=self.bg_color, folder_index=4)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 5 * 4, y=250, target=self.select_level_4,
                                                               width=100, height=100,
                                                               bg_color=self.bg_color, folder_index=4)
        self.add_updatable(self.button_back_to_menu)
        self.add_updatable(self.button_select_level_1)
        self.add_updatable(self.button_select_level_2)
        self.add_updatable(self.button_select_level_3)
        self.add_updatable(self.button_select_level_4)

    def menu(self):
        self.game.show_screen = 0

    def select_level_1(self):
        self.game.show_screen = 1
        self.game.load_level('poziom1')

    def select_level_2(self):
        self.game.show_screen = 1
        self.game.load_level('poziom2')

    def select_level_3(self):
        self.game.show_screen = 1

    def select_level_4(self):
        self.game.show_screen = 1


class Settings(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_back_to_menu = grarantanna_button.Button(x=110, y=35, target=self.back_to_menu, width=240,
                                                             height=60,
                                                             bg_color=self.bg_color, folder_index=3)

        self.add_updatable(self.button_back_to_menu)

    def back_to_menu(self):
        self.game.show_screen = 0
