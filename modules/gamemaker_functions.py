import math


def length_dir_x(speed, angle):
    return math.cos(angle * (math.pi/180)) * speed


def length_dir_y(speed, angle):
    return math.sin(angle * (math.pi / 180)) * speed


def get_angle(w, h):
    return (math.atan(h/w) * 180) / math.pi


def point_direction(x1, y1, x2, y2):
    angle = math.atan2(y2-y1, x2-x1)

    if angle < 0:
        angle = abs(angle)
    else:
        angle = 2 * math.pi - angle

    return math.degrees(angle)


def place_meeting(x, y, b, p):  # For predicting the position
    """
    :param x: x offset of player
    :param y: y offset of player
    :param b: block object, child of block.Block
    :param p: player object, child of grarantanna_player.Player
    :return: collision
    """

    if x + p.width < b.x:
        return False
    if x > b.x + b.width:
        return False
    if y + p.height < b.y:
        return False
    if y > b.y + b.height:
        return False
    return True


def point_in_rectangle(point_x, point_y, x_rect, y_rect, width, height):
    if not x_rect < point_x < x_rect + width:
        return False
    if not y_rect < point_y < y_rect + height:
        return False
    return True


def sign(x):
    if x > 0:
        return 1

    elif x < 0:
        return -1

    elif x == 0:
        return 0
