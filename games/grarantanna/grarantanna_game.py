import pygame
from modules import \
    basic_classes, \
    basic_globals, \
    game_class, \
    level_reader, block

from games.grarantanna import grarantanna_player


class Grarantanna(game_class.Game):
    def __init__(self, width, height, fps=60):
        super().__init__(width, height, fps)
        self.bg_color = basic_globals.BG_COLOR

        self.game_tiles = level_reader.read('poziom1', block.Block)
        player_x = 0
        player_y = 0
        for tile in self.game_tiles:
            if tile.tag == 'start':
                player_x, player_y = tile.x, tile.y-tile.size
            else:
                if tile.tag == 'kolce':
                    self.fix_kolce(tile)
                self.add_drawable(tile)

        self.player = grarantanna_player.Player(x=player_x, y=player_y, size=20)
        self.add_updatable(self.player)
        self.add_updatable(self.player.gun)

    def fix_kolce(self, tile):
        sprite = tile.sprites[0]
        surf = pygame.Surface((40, 20))
        surf.blit(sprite, (0, -15))
        tile.y += 20
        tile.sprites = [surf]

