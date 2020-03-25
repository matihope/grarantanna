import pygame
import math
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

        self.przyslowia = [
            'Testujemy Poziom 1',  # Poziom 1
            'Testujemy Poziom 2',  # Poziom 2
            'Testujemy Poziom 3______',  # Poziom 3
            'Testujemy Poziom 4',  # Poziom 4
            'Testujemy Poziom 5',  # Poziom 5
            'Testujemy Poziom 6',  # Poziom 6
            'Testujemy Poziom 7',  # Poziom 7
            'Testujemy Poziom 8',  # Poziom 8
            'Testujemy Poziom 9',  # Poziom 9
            'Testujemy Poziom 10',  # Poziom 10
            'Testujemy Poziom 11',  # Poziom 11
            'Testujemy Poziom 12',  # Poziom 12
            'Testujemy Poziom 13',  # Poziom 13
            'Testujemy Poziom 14',  # Poziom 14
            'Testujemy Poziom 15'  # Poziom 15
            ]
        self.game_tiles = []
        self.player = None

        # self.sound_przyciski_menu = pygame.mixer.Sound('resources/wybor_w_menu.wav')
        # self.sound_strzal = pygame.mixer.Sound('resources/strzal')
        # self.sound_teleport = pygame.mixer.Sound('resources/teleportacja.wav')
        # self.sound_ruszanie = pygame.mixer.Sound('resources/')
        # self.sound_skok = pygame.mixer.Sound('resources/skok.wav')
        # self.sound_smierc = pygame.mixer.Sound('resources/smierc.wav')
        # self.sound_zabicie_traktora = pygame.mixer.Sound('')
        # self.sound_zdobycie_punktu = pygame.mixer.Sound('zdobycie_punktu.wav')

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

        tiles_czesc = []
        self.game_tiles = level_reader.read(self.level_name)
        for tile in self.game_tiles:
            if tile.tag == 'start':
                continue
            if tile.tag == 'kolce':
                self.fix_kolce(tile)
            if tile.tag == 'czesc':
                tiles_czesc.append(tile)
                self.add_updatable(tile)
            else:
                self.add_updatable(tile, draw_order=4)

        self.generate_texts(tiles_czesc, self.przyslowia[int(self.level_name[6:])-1])

    def load_level(self, name):
        if self.player is not None:
            self.remove_obj(self.player)
            self.remove_obj(self.player.gun)

        for tile in self.game_tiles:
            self.remove_obj(tile)

        self.game_tiles = level_reader.read(name)
        player_x = 0
        player_y = 0
        tiles_czesc = []
        for tile in self.game_tiles:
            if tile.tag == 'start':
                player_x, player_y = tile.x + 10, tile.y+1
            else:
                if tile.tag == 'kolce':
                    self.fix_kolce(tile)
                if tile.tag == 'czesc':
                    tiles_czesc.append(tile)
                    self.add_updatable(tile)
                else:
                    self.add_updatable(tile, draw_order=4)

        self.load_player(player_x, player_y)
        self.generate_texts(tiles_czesc, self.przyslowia[int(name[6:])-1])

        self.level_name = name

    def load_player(self, player_x, player_y):
        self.player = grarantanna_player.Player(x=player_x, y=player_y, size=20)
        self.add_updatable(self.player, draw_order=1)
        self.add_updatable(self.player.gun, draw_order=3)
        self.player.reset_vars()

    def generate_texts(self, tiles_czesc, przyslowie):
        try:
            self.player.to_collect_string = przyslowie
            n = int(len(przyslowie)/len(tiles_czesc))
            text = [przyslowie[i:i + n] for i in range(0, len(przyslowie), n)]
            for i in range(len(tiles_czesc)):
                i %= len(text)-1
                tiles_czesc[i].sprite_index = 0
                tiles_czesc[i].text += text[i]
                print(tiles_czesc[i].text)

            full_by_now = ''.join(text)
            second_part_przyslowie = przyslowie[len(full_by_now)-1:]
            tiles_czesc[-1].text += second_part_przyslowie

        except Exception as e:
            print(e)


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


class LevelSelect1(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game

        self.bg_color = basic_globals.BG_COLOR
        self.font_name = 'resources/Born2bSportyV2.ttf'
        self.font_size = 60
        self.font_color = (227, 197, 56)
        font = pygame.font.Font(self.font_name, self.font_size)
        rendered = font.render('Łatwe poziomy', True, self.font_color)
        self.text = basic_classes.DrawableObj(x=self.WIDTH // 2 - rendered.get_width() // 2, y=200, sprites=[rendered],
                                              width=rendered.get_width(), height=rendered.get_height())
        self.add_drawable(self.text)

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=620, target=self.back_to_menu,
                                                             width=360, height=60, text='back to menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_next = grarantanna_button.Button(x=1000, y=100, target=self.next,
                                                     width=360, height=60, text='next',
                                                     font_grow_ratio=1.2,
                                                     bg_color=self.bg_color, folder_index=0)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=400, target=self.select_level_1,
                                                               width=100, height=100, text='Level 1', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=400, target=self.select_level_2,
                                                               width=100, height=100, text='Level 2', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=400, target=self.select_level_3,
                                                               width=100, height=100, text='Level 3', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=400, target=self.select_level_4,
                                                               width=100, height=100, text='Level 4', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_5 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=400, target=self.select_level_5,
                                                               width=100, height=100, text='Level 5', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)

        self.add_updatable(self.button_next)
        self.add_updatable(self.button_back_to_menu)
        self.add_updatable(self.button_select_level_1)
        self.add_updatable(self.button_select_level_2)
        self.add_updatable(self.button_select_level_3)
        self.add_updatable(self.button_select_level_4)
        self.add_updatable(self.button_select_level_5)

    def back_to_menu(self):
        self.game.show_screen = 0

    def next(self):
        self.game.show_screen = 6

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


class LevelSelect2(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game

        self.bg_color = basic_globals.BG_COLOR
        self.font_name = 'resources/Born2bSportyV2.ttf'
        self.font_size = 60
        self.font_color = (227, 197, 56)
        font = pygame.font.Font(self.font_name, self.font_size)
        rendered = font.render('Średnie poziomy', True, self.font_color)
        self.text = basic_classes.DrawableObj(x=self.WIDTH // 2 - rendered.get_width() // 2, y=200, sprites=[rendered],
                                              width=rendered.get_width(), height=rendered.get_height())
        self.add_drawable(self.text)

        self.button_previous = grarantanna_button.Button(x=200, y=100, target=self.previous,
                                                         width=360, height=60, text='previous',
                                                         font_grow_ratio=1.2,
                                                         bg_color=self.bg_color, folder_index=0)
        self.button_next = grarantanna_button.Button(x=1000, y=100, target=self.next,
                                                     width=360, height=60, text='next',
                                                     font_grow_ratio=1.2,
                                                     bg_color=self.bg_color, folder_index=0)

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=620, target=self.back_to_menu,
                                                             width=360, height=60, text='back to menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=400, target=self.select_level_1,
                                                               width=100, height=100, text='Level 6', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=400, target=self.select_level_2,
                                                               width=100, height=100, text='Level 7', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=400, target=self.select_level_3,
                                                               width=100, height=100, text='Level 8', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=400, target=self.select_level_4,
                                                               width=100, height=100, text='Level 9', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_5 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=400, target=self.select_level_5,
                                                               width=100, height=100, text='Level 10',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)

        self.add_updatable(self.button_next)
        self.add_updatable(self.button_previous)
        self.add_updatable(self.button_back_to_menu)
        self.add_updatable(self.button_select_level_1)
        self.add_updatable(self.button_select_level_2)
        self.add_updatable(self.button_select_level_3)
        self.add_updatable(self.button_select_level_4)
        self.add_updatable(self.button_select_level_5)

    def back_to_menu(self):
        self.game.show_screen = 0

    def previous(self):
        self.game.show_screen = 2

    def next(self):
        self.game.show_screen = 7

    def select_level_1(self):
        self.game.show_screen = 1
        self.game.load_level('poziom6')

    def select_level_2(self):
        self.game.show_screen = 1
        self.game.load_level('poziom7')

    def select_level_3(self):
        self.game.show_screen = 1
        self.game.load_level('poziom8')

    def select_level_4(self):
        self.game.show_screen = 1
        self.game.load_level('poziom9')

    def select_level_5(self):
        self.game.show_screen = 1
        self.game.load_level('poziom10')


class LevelSelect3(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game

        self.bg_color = basic_globals.BG_COLOR
        self.font_name = 'resources/Born2bSportyV2.ttf'
        self.font_size = 60
        self.font_color = (227, 197, 56)
        font = pygame.font.Font(self.font_name, self.font_size)
        rendered = font.render('Trudne poziomy', True, self.font_color)
        self.text = basic_classes.DrawableObj(x=self.WIDTH // 2 - rendered.get_width() // 2, y=200, sprites=[rendered],
                                              width=rendered.get_width(), height=rendered.get_height())
        self.add_drawable(self.text)

        self.button_previous = grarantanna_button.Button(x=200, y=100, target=self.previous,
                                                         width=360, height=60, text='previous',
                                                         font_grow_ratio=1.2,
                                                         bg_color=self.bg_color, folder_index=0)

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=620, target=self.back_to_menu,
                                                             width=360, height=60, text='back to menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=400, target=self.select_level_1,
                                                               width=100, height=100, text='Level 11',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=400, target=self.select_level_2,
                                                               width=100, height=100, text='Level 12',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=400, target=self.select_level_3,
                                                               width=100, height=100, text='Level 13',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=400, target=self.select_level_4,
                                                               width=100, height=100, text='Level 14',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)
        self.button_select_level_5 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=400, target=self.select_level_5,
                                                               width=100, height=100, text='Level 15',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2)

        self.add_updatable(self.button_back_to_menu)
        self.add_updatable(self.button_previous)
        self.add_updatable(self.button_select_level_1)
        self.add_updatable(self.button_select_level_2)
        self.add_updatable(self.button_select_level_3)
        self.add_updatable(self.button_select_level_4)
        self.add_updatable(self.button_select_level_5)

    def back_to_menu(self):
        self.game.show_screen = 0

    def previous(self):
        self.game.show_screen = 6

    def select_level_1(self):
        self.game.show_screen = 1
        self.game.load_level('poziom11')

    def select_level_2(self):
        self.game.show_screen = 1
        self.game.load_level('poziom12')

    def select_level_3(self):
        self.game.show_screen = 1
        self.game.load_level('poziom13')

    def select_level_4(self):
        self.game.show_screen = 1
        self.game.load_level('poziom14')

    def select_level_5(self):
        self.game.show_screen = 1
        self.game.load_level('poziom15')


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