import pygame
import copy
from modules import \
    basic_classes, \
    basic_globals, \
    game_class, \
    gamemaker_functions as gmf, \
    level_reader, block
import os

from games.grarantanna import grarantanna_player, grarantanna_button, grarantanna_slider


class Grarantanna(game_class.Game):
    def __init__(self, width, height, fps=60):
        super().__init__(width, height, fps)
        self.bg_color = basic_globals.BG_COLOR
        self.show_screen = 0
        self.level_name = ''
        self.volume = 25

        self.finished_levels = []

        self.przyslowia = [
            'CO NAGLE, TO PO DIABLE',  # Poziom 1
            'GDY KOTA NIE MA, MYSZY HARCUJĄ',  # Poziom 2
            'KRADZIONE NIE TUCZY',  # Poziom 3
            'KTO PYTA, NIE BŁĄDZI',  # Poziom 4
            'KUĆ ŻELAZO, PUKI GORĄCE',  # Poziom 5
            'Testujemy poz 6',  # Poziom 6
            'Testujemy poz 7',  # Poziom 7
            'BEZ PRACY NIE MA KOŁACZY',  # Poziom 8
            'DAROWANEMU KONIOWI W ZĘBY SIĘ NIE ZAGLĄDA',  # Poziom 9
            'NIE CHWAL DNIA PRZED ZACHODEM SŁOŃCA',  # Poziom 10
            'FORTUNA KOŁEM SIĘ TOCZY',  # Poziom 11
            'APETYT ROŚNIE W MIARĘ JEDZENIA',  # Poziom 12
            'Testujemy Poziom 13',  # Poziom 13
            'DZIECI I RYBY GŁOSU NIE MAJĄ',  # Poziom 14
            'Testujemy Poziom 15',  # Poziom 15
            'CO MA WISIEĆ, NIE UTONIE',  # Poziom 16
            'LEPSZY WRÓBEL W GARŚCI NIŻ GOŁĄB NA DACHU',  # Poziom 17
            'Testujemy poz 18',  # Poziom 18
            'DZIECI I RYBY GŁOSU NIE MAJĄ',  # Poziom 19
            'Testujemy poz 20'  # Poziom 20
            ]

        self.game_tiles = []
        self.player = None

        self.sound_przyciski_menu = pygame.mixer.Sound('resources/sounds/wybor_w_menu.wav')
        self.sound_przyciski_menu.set_volume(0.3)
        self.sound_strzal = pygame.mixer.Sound('resources/sounds/strzal.wav')
        self.sound_strzal.set_volume(0.3)
        self.sound_teleport = pygame.mixer.Sound('resources/sounds/teleportacja.wav')
        self.sound_skok = pygame.mixer.Sound('resources/sounds/skok.wav')
        self.sound_smierc = pygame.mixer.Sound('resources/sounds/smierc.wav')
        self.sound_zabicie_traktora = pygame.mixer.Sound('resources/sounds/traktor.wav')
        self.sound_zdobycie_punktu = pygame.mixer.Sound('resources/sounds/zdobycie_punktu.wav')
        self.channel = pygame.mixer.find_channel(True)

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
        self.player.to_collect_string = przyslowie
        self.player.to_collect_string_colored = ' ' * len(przyslowie)
        n = round(len(przyslowie)/len(tiles_czesc))
        text = [przyslowie[i:i + n] for i in range(0, len(przyslowie), n)]
        for i in range(len(tiles_czesc)):
            tiles_czesc[i].sprite_index = 0
            tiles_czesc[i].text += text[i]
            print(tiles_czesc[i].text)

    def set_volume(self, value):
        self.volume = value
        self.channel.set_volume(value/50)

    def next_level(self):
        level_index = int(self.level_name[6:])
        self.finished_levels.append(level_index)
        self.load_level('poziom' + str(level_index + 1))


class Menu(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        rendered = pygame.image.load(os.path.join(f'resources/logo.png'))
        self.logo = basic_classes.DrawableObj(x=300, y=105, sprites=[rendered],
                                              width=rendered.get_width(), height=rendered.get_height())
        self.add_drawable(self.logo)

        self.font_name = 'resources/Born2bSportyV2.ttf'
        self.font_size = 120
        self.font_color = (227, 197, 56)
        font = pygame.font.Font(self.font_name, self.font_size)
        rendered = font.render('DISK-O-TRUCK', True, self.font_color)
        self.text = basic_classes.DrawableObj(x=75, y=80, sprites=[rendered],
                                              width=rendered.get_width(), height=rendered.get_height())
        self.add_drawable(self.text)

        self.button_start = grarantanna_button.Button(x=self.WIDTH // 2, y=550, target=self.start, width=240, height=60,
                                                      bg_color=self.bg_color, folder_index=0, text='START')

        self.button_select_level = grarantanna_button.Button(x=self.WIDTH // 2, y=625, target=self.select_level,
                                                             width=360, height=60, text='wybierz pokój',
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_settings = grarantanna_button.Button(x=self.WIDTH // 2, y=700, target=self.settings, width=240,
                                                         height=60, text='ustawienia',
                                                         bg_color=self.bg_color, folder_index=0)

        self.add_updatable(self.button_start)
        self.add_updatable(self.button_select_level)
        self.add_updatable(self.button_settings)

    def start(self):
        self.game.show_screen = 1
        self.game.load_level('poziom1')

    def select_level(self):
        self.game.show_screen = 8

    def settings(self):
        self.game.show_screen = 3


class LevelSelect0(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game

        self.bg_color = basic_globals.BG_COLOR
        self.font_name = 'resources/Born2bSportyV2.ttf'
        self.font_size = 60
        self.font_color = (227, 197, 56)
        font = pygame.font.Font(self.font_name, self.font_size)
        rendered = font.render('Wprowadzenie', True, self.font_color)
        self.text = basic_classes.DrawableObj(x=self.WIDTH // 2 - rendered.get_width() // 2, y=200, sprites=[rendered],
                                              width=rendered.get_width(), height=rendered.get_height())
        self.add_drawable(self.text)

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=620, target=self.back_to_menu,
                                                             width=360, height=60, text='wróć do menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_next = grarantanna_button.Button(x=1000, y=100, target=self.next,
                                                     width=360, height=60, text='następne',
                                                     font_grow_ratio=1.2,
                                                     bg_color=self.bg_color, folder_index=0)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=400, target=self.select_level_1,
                                                               width=100, height=100, text='Pokój 1', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=400, target=self.select_level_2,
                                                               width=100, height=100, text='Pokój 2', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=400, target=self.select_level_3,
                                                               width=100, height=100, text='Pokój 3', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=400, target=self.select_level_4,
                                                               width=100, height=100, text='Pokój 4', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_5 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=400, target=self.select_level_5,
                                                               width=100, height=100, text='Pokój 5', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)

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
        self.game.show_screen = 2

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
                                                             width=360, height=60, text='wróć do menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_next = grarantanna_button.Button(x=1000, y=100, target=self.next,
                                                     width=360, height=60, text='następne',
                                                     font_grow_ratio=1.2,
                                                     bg_color=self.bg_color, folder_index=0)
        self.button_previous = grarantanna_button.Button(x=200, y=100, target=self.previous,
                                                         width=360, height=60, text='poprzednie',
                                                         font_grow_ratio=1.2,
                                                         bg_color=self.bg_color, folder_index=0)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=400, target=self.select_level_1,
                                                               width=100, height=100, text='Pokój 6', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=400, target=self.select_level_2,
                                                               width=100, height=100, text='Pokój 7', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=400, target=self.select_level_3,
                                                               width=100, height=100, text='Pokój 8', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=400, target=self.select_level_4,
                                                               width=100, height=100, text='Pokój 9', font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_5 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=400, target=self.select_level_5,
                                                               width=100, height=100, text='Pokój 10',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)

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

    def next(self):
        self.game.show_screen = 6

    def previous(self):
        self.game.show_screen = 8

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
                                                         width=360, height=60, text='poprzednie',
                                                         font_grow_ratio=1.2,
                                                         bg_color=self.bg_color, folder_index=0)
        self.button_next = grarantanna_button.Button(x=1000, y=100, target=self.next,
                                                     width=360, height=60, text='następne',
                                                     font_grow_ratio=1.2,
                                                     bg_color=self.bg_color, folder_index=0)

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=620, target=self.back_to_menu,
                                                             width=360, height=60, text='wróć do menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=400, target=self.select_level_1,
                                                               width=100, height=100, text='Pokój 11',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=400, target=self.select_level_2,
                                                               width=100, height=100, text='Pokój 12',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=400, target=self.select_level_3,
                                                               width=100, height=100, text='Pokój 13',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=400, target=self.select_level_4,
                                                               width=100, height=100, text='Pokój 14',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_5 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=400, target=self.select_level_5,
                                                               width=100, height=100, text='Pokój 15',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)

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
                                                         width=360, height=60, text='poprzednie',
                                                         font_grow_ratio=1.2,
                                                         bg_color=self.bg_color, folder_index=0)

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=620, target=self.back_to_menu,
                                                             width=360, height=60, text='wróć do menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.button_select_level_1 = grarantanna_button.Button(x=self.WIDTH // 6 * 1, y=400, target=self.select_level_1,
                                                               width=100, height=100, text='Pokój 16',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_2 = grarantanna_button.Button(x=self.WIDTH // 6 * 2, y=400, target=self.select_level_2,
                                                               width=100, height=100, text='Pokój 17',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_3 = grarantanna_button.Button(x=self.WIDTH // 6 * 3, y=400, target=self.select_level_3,
                                                               width=100, height=100, text='Pokój 18',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_4 = grarantanna_button.Button(x=self.WIDTH // 6 * 4, y=400, target=self.select_level_4,
                                                               width=100, height=100, text='Pokój 19',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)
        self.button_select_level_5 = grarantanna_button.Button(x=self.WIDTH // 6 * 5, y=400, target=self.select_level_5,
                                                               width=100, height=100, text='Pokój 20',
                                                               font_grow_ratio=1,
                                                               bg_color=self.bg_color, folder_index=2,
                                                               level_button=True)

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
        self.game.load_level('poziom16')

    def select_level_2(self):
        self.game.show_screen = 1
        self.game.load_level('poziom17')

    def select_level_3(self):
        self.game.show_screen = 1
        self.game.load_level('poziom18')

    def select_level_4(self):
        self.game.show_screen = 1
        self.game.load_level('poziom19')

    def select_level_5(self):
        self.game.show_screen = 1
        self.game.load_level('poziom20')


class Settings(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR
        self.font_name = 'resources/Born2bSportyV2.ttf'
        self.font_size = 60
        self.font_color = (227, 197, 56)
        font = pygame.font.Font(self.font_name, self.font_size)
        rendered = font.render('ustawienia', True, self.font_color)
        self.text = basic_classes.DrawableObj(x=self.WIDTH // 2 - rendered.get_width() // 2, y=200, sprites=[rendered],
                                              width=rendered.get_width(), height=rendered.get_height())
        self.add_drawable(self.text)

        self.button_back_to_menu = grarantanna_button.Button(x=self.WIDTH // 2, y=650, target=self.back_to_menu,
                                                             width=360, height=60, text='wróć do menu',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.add_updatable(self.button_back_to_menu)

        self.volume_slider = grarantanna_slider.Slider(x=self.WIDTH // 2, y=350, text='Głośność')
        self.add_updatable(self.volume_slider)

    def back_to_menu(self):
        self.game.show_screen = 0


class Settings_in_game(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR
        self.font_name = 'resources/Born2bSportyV2.ttf'
        self.font_size = 60
        self.font_color = (227, 197, 56)
        font = pygame.font.Font(self.font_name, self.font_size)
        rendered = font.render('ustawienia', True, self.font_color)
        self.text = basic_classes.DrawableObj(x=self.WIDTH // 2 - rendered.get_width() // 2, y=200, sprites=[rendered],
                                              width=rendered.get_width(), height=rendered.get_height())
        self.add_drawable(self.text)

        self.button_back_to_game = grarantanna_button.Button(x=self.WIDTH // 2, y=650, target=self.back_to_game,
                                                             width=360, height=60, text='wróć do gry',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)

        self.add_updatable(self.button_back_to_game)

        self.volume_slider = grarantanna_slider.Slider(x=self.WIDTH // 2, y=350, text='Głośność')
        self.add_updatable(self.volume_slider)

    def back_to_game(self):
        self.game.show_screen = 1


class Stop(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_back_to_game = grarantanna_button.Button(x=self.WIDTH // 2, y=250, target=self.back_to_game,
                                                             width=360, height=60, text='wróć do gry',
                                                             font_grow_ratio=1.2,
                                                             bg_color=self.bg_color, folder_index=1)
        self.button_reset_level = grarantanna_button.Button(x=self.WIDTH // 2, y=250 + 75, target=self.reset_level,
                                                            width=360, height=60, text='resetart pokoju',
                                                            font_grow_ratio=1.2,
                                                            bg_color=self.bg_color, folder_index=1)
        self.button_settings_in_game = grarantanna_button.Button(x=self.WIDTH // 2, y=250 + 75 * 2,
                                                                 target=self.settings_in_game,
                                                                 width=360, height=60, text='ustawienia',
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
