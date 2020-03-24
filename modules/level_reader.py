import pygame
import os
from modules import basic_globals, block


def flip(tile, board_w, board_h):
    y = (board_h * tile.height) - tile.y
    tile.y = y


def decode(lines):
    tiles = []
    board_w, board_h = lines[2][12:].split(',')
    board_w = int(board_w)
    board_h = int(board_h)
    for line in lines:
        if line[:5] == 'tile:':
            line = line[5:-1]  # Strip from \n and tile:
            vals = line.split(',')

            size = int(vals[4])
            img = pygame.image.load(os.path.join('resources', f'{vals[0]}'))
            index = int(vals[1])
            img_w = img.get_width()
            img_h = img.get_height()
            sprites = []
            for sprite in range(img_w//size * img_h//size):
                surf = pygame.Surface((size, size))
                surf.fill(basic_globals.BG_COLOR)
                surf.blit(img, (-(sprite * size % img_w), -(sprite % img_h / size)))
                sprites.append(surf)
            tag = vals[7]

            new_tile = block.Block(sprites=sprites, sprite_index=int(index), x=float(vals[2]), y=float(vals[3]),
                                   size=size, tag=tag)
            flip(new_tile, board_w, board_h)

            tiles.append(new_tile)

    return tiles


def read_file(file_name):
    file = open('levels/' + file_name + '.txt', 'r')
    lines = file.readlines()
    file.close()
    return lines


def read(file_name):
    lines = read_file(file_name)
    return decode(lines)
