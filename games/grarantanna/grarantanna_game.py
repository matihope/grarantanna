import pygame
from modules import \
    basic_classes, \
    basic_globals, \
    game_class, \
    gamemaker_functions as gmf, \
    level_reader, block

from games.grarantanna import grarantanna_player, grarantanna_button, grarantanna_slider


class Grarantanna(game_class.Game):
    def __init__(self, width, height, fps=60):
        super().__init__(width, height, fps)
        self.bg_color = basic_globals.BG_COLOR
        self.show_screen = 0
        self.level_name = ''

        self.game_tiles = []
        self.player = None

    def fix_kolce(self, tile):
        sprite = tile.sprites[tile.sprite_index]
        surf = pygame.Surface((40, 20))
        surf.blit(sprite, (0, -15))
        tile.y += 20
        tile.height = 20
        tile.sprites = [surf]

    def reset_level(self):
        for tile in self.game_tiles:
            self.remove_obj(tile)

        self.game_tiles = level_reader.read(self.level_name)
        for tile in self.game_tiles:
            if tile.tag != 'start':
                if tile.tag == 'kolce':
                    self.fix_kolce(tile)
                if tile.tag == 'czesc':
                    self.add_updatable(tile)
                else:
                    self.add_updatable(tile, draw_order=4)

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
                # self.add_updatable(tile)
                player_x, player_y = tile.x + 10, tile.y
            else:
                if tile.tag == 'kolce':
                    self.fix_kolce(tile)
                if tile.tag == 'czesc':
                    self.add_updatable(tile)
                else:
                    self.add_updatable(tile, draw_order=4)

        self.load_player(player_x, player_y)

        self.level_name = name

    def load_player(self, player_x, player_y):
        self.player = grarantanna_player.Player(x=player_x, y=player_y, size=20)
        self.add_updatable(self.player, draw_order=1)
        self.add_updatable(self.player.gun, draw_order=3)
        self.player.reset_vars()


class Menu(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_start = grarantanna_button.Button(x=self.WIDTH // 2, y=550, target=self.start, width=240, height=60,
                                                      bg_color=self.bg_color, folder_index=0, text='START')

        self.button_select_level = grarantanna_button.Button(x=self.WIDTH // 2, y=625, target=self.select_level,
                                                             width=360, height=60, text='select level',
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_settings = grarantanna_button.Button(x=self.WIDTH // 2, y=700, target=self.settings, width=240,
                                                         height=60, text='settings',
                                                         bg_color=self.bg_color, folder_index=0)

        self.add_updatable(self.button_start)
        self.add_updatable(self.button_select_level)
        self.add_updatable(self.button_settings)

    def start(self):
        self.game.show_screen = 1
        self.game.load_level('poziom1')

    def select_level(self):
        self.game.show_screen = 2

    def settings(self):
        self.game.show_screen = 3


class LevelSelect(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=620, target=self.back_to_menu,
                                                             width=360, height=60, text='back to menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=250, target=self.select_level_1,
                                                               width=100, height=100, text='Level 1', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=250, target=self.select_level_2,
                                                               width=100, height=100, text='Level 2', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=250, target=self.select_level_3,
                                                               width=100, height=100, text='Level 3', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=250, target=self.select_level_4,
                                                               width=100, height=100, text='Level 4', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_5 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=250, target=self.select_level_5,
                                                               width=100, height=100, text='Level 5', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)

        self.button_select_level_6 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=250 + self.WIDTH // 6,
                                                               target=self.select_level_6,
                                                               width=100, height=100, text='Level 6', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_7 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=250 + self.WIDTH // 6,
                                                               target=self.select_level_7,
                                                               width=100, height=100, text='Level 7', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_8 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=250 + self.WIDTH // 6,
                                                               target=self.select_level_8,
                                                               width=100, height=100, text='Level 8', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_9 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=250 + self.WIDTH // 6,
                                                               target=self.select_level_9,
                                                               width=100, height=100, text='Level 9', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_10 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=250 + self.WIDTH // 6,
                                                                target=self.select_level_10,
                                                                width=100, height=100, text='Level 10',
                                                                font_grow_ratio=1,
                                                                bg_color=self.bg_color, folder_index=2)
        self.add_updatable(self.button_back_to_menu)
        self.add_updatable(self.button_select_level_1)
        self.add_updatable(self.button_select_level_2)
        self.add_updatable(self.button_select_level_3)
        self.add_updatable(self.button_select_level_4)
        self.add_updatable(self.button_select_level_5)
        self.add_updatable(self.button_select_level_6)
        self.add_updatable(self.button_select_level_7)
        self.add_updatable(self.button_select_level_8)
        self.add_updatable(self.button_select_level_9)
        self.add_updatable(self.button_select_level_10)

    def back_to_menu(self):
        self.game.show_screen = 0

    def select_level_1(self):
        self.game.show_screen = 1
        self.game.load_level('poziom1')

    def select_level_2(self):
        self.game.show_screen = 1
        self.game.load_level('poziom2')

    def select_level_3(self):
        self.game.show_screen = 1
        self.game.load_level('poziom3')

    def select_level_4(self):
        self.game.show_screen = 1
        self.game.load_level('poziom4')

    def select_level_5(self):
        self.game.show_screen = 1
        self.game.load_level('poziom5')

    def select_level_6(self):
        self.game.show_screen = 1
        self.game.load_level('poziom6')

    def select_level_7(self):
        self.game.show_screen = 1
        self.game.load_level('poziom7')

    def select_level_8(self):
        self.game.show_screen = 1
        self.game.load_level('poziom8')

    def select_level_9(self):
        self.game.show_screen = 1
        self.game.load_level('poziom9')

    def select_level_10(self):
        self.game.show_screen = 1
        self.game.load_level('poziom10')


class Settings(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=650, target=self.back_to_menu,
                                                             width=360, height=60, text='back to menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.add_updatable(self.button_back_to_menu)

        self.volume_slider = grarantanna_slider.Slider(x=self.WIDTH // 2, y=350, text='glosnoc')
        self.add_updatable(self.volume_slider)

    def back_to_menu(self):
        self.game.show_screen = 0


class Settings_in_game(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_back_to_game = grarantanna_button.Button(x=self.WIDTH // 2, y=650, target=self.back_to_game,
                                                             width=360, height=60, text='back to game',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.add_updatable(self.button_back_to_game)

        self.volume_slider = grarantanna_slider.Slider(x=self.WIDTH // 2, y=350, text='glosnoc')
        self.add_updatable(self.volume_slider)

    def back_to_game(self):
        self.game.show_screen = 1


class Stop(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_back_to_game = grarantanna_button.Button(x=self.WIDTH // 2, y=250, target=self.back_to_game,
                                                             width=360, height=60, text='back to game',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)
        self.button_reset_level = grarantanna_button.Button(x=self.WIDTH // 2, y=250 + 75, target=self.reset_level,
                                                            width=360, height=60, text='reset level',
                                                            font_grow_ratio=1.2,
                                                            bg_color=self.bg_color, folder_index=1)
        self.button_settings_in_game = grarantanna_button.Button(x=self.WIDTH // 2, y=250 + 75 * 2,
                                                                 target=self.settings_in_game,
                                                                 width=360, height=60, text='settings',
                                                                 font_grow_ratio=1.2,
                                                                 bg_color=self.bg_color, folder_index=1)
        self.button_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=250 + 75 * 4, target=self.menu,
                                                     width=360, height=60, text='menu', font_grow_ratio=1.2,
                                                     bg_color=self.bg_color, folder_index=1)

        self.add_updatable(self.button_reset_level)
        self.add_updatable(self.button_menu)
        self.add_updatable(self.button_back_to_game)
        self.add_updatable(self.button_settings_in_game)

    def reset_level(self):
        self.game.reset_level()
        self.game.player.reset_vars()
        self.game.show_screen = 1

    def menu(self):
        self.game.show_screen = 0

    def back_to_game(self):
        self.game.show_screen = 1

    def settings_in_game(self):
        self.game.show_screen = 5
