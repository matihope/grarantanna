import pygame
import os


def flip(tile, board_w, board_h):
    y = (board_h * tile.size) - tile.y
    tile.y = y


def decode(lines, tile_sprite_class):
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
            texture = pygame.Surface((size, size))
            texture.fill((50, 50, 50))
            texture.blit(img, (-(index * size % img.get_width()), -(index % img.get_width() / size)))

            new_tile = tile_sprite_class(texture=texture, x=float(vals[2]), y=float(vals[3]), size=size, tag=vals[7])
            flip(new_tile, board_w, board_h)

            tiles.append(new_tile)
            print(vals)

    return tiles


def read_file(file_name):
    file = open('levels/' + file_name + '.txt', 'r')
    lines = file.readlines()
    file.close()
    return lines


def read(file_name, tile_sprite_class):
    lines = read_file(file_name)
    return decode(lines, tile_sprite_class)
