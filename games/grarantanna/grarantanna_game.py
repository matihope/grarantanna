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
        self.game_tiles_start = level_reader.read('poziom2', block.Block)
        self.game_tiles = self.game_tiles_start.copy()
        player_x = 0
        player_y = 0
        for tile in self.game_tiles:
            if tile.tag == 'start':
                player_x, player_y = tile.x, tile.y
            else:
                if tile.tag == 'kolce':
                    self.fix_kolce(tile)
                self.add_drawable(tile)

        self.player = grarantanna_player.Player(x=player_x, y=player_y, size=35)
        self.add_updatable(self.player)
        self.add_updatable(self.player.gun)

    def fix_kolce(self, tile):
        sprite = tile.sprites[0]
        surf = pygame.Surface((40, 20))
        surf.blit(sprite, (0, -15))
        tile.y += 20
        tile.sprites = [surf]

    def reset_level(self):
        for tile in self.game_tiles:
            self.remove_obj(tile)

        self.game_tiles = self.game_tiles_start.copy()
        for tile in self.game_tiles:
            tile.dead = False
            if tile.tag == 'start':
                continue
            self.add_drawable(tile)


class Menu(game_class.Game):
    def __init__(self, game, width, height, fps=60):
        super().__init__(width, height, fps)
        self.game = game
        self.bg_color = basic_globals.BG_COLOR

        self.button_start = grarantanna_button.Button(x=500, y=500, target=self.start, width=240, height=60,
                                                      bg_color=self.bg_color)

        self.add_updatable(self.button_start)

    def start(self):
        self.game.show_screen = 1
