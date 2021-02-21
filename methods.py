import pygame
import math

from pygame.locals import *
import commons


def get_char_index(string, font, x_offset):
    current_char_index = 0
    current_length = 0
    for char in string:
        char_length = font.size(char)[0]
        if current_length + char_length > x_offset:
            break
        else:
            current_length += char_length
            current_char_index += 1

    return current_char_index


def get_size_up_to_char_index(string, font, index):
    sub_str = string[:index]
    return font.size(sub_str)[0]


avoid_keys = [
    pygame.K_TAB, pygame.K_CAPSLOCK, pygame.K_LSHIFT,
    pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL,
    pygame.K_LALT, pygame.K_RALT, pygame.K_RETURN,
    pygame.K_NUMLOCK, pygame.K_ESCAPE, pygame.K_DELETE,
    pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN
]


def str_from_key_event(key_event):
    if key_event.key in avoid_keys:
        return None
    return key_event.unicode


numeric_chars = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"
]


def limit_to_numeric_chars(char, allow_period, allow_comma):
    if char in numeric_chars or (allow_period and char == '.') or (allow_comma and char == ','):
        return char
    return None


def clamp_int_0_255(value):
    return int(min(255, max(0, value)))


def modify_col(col, mod):
    return clamp_int_0_255(col[0] * mod), clamp_int_0_255(col[1] * mod), clamp_int_0_255(col[2] * mod)


def safe_load_image(path):
    try:
        return pygame.image.load(path).convert()
    except pygame.error:
        return commons.placeholder_image


def draw_rect_clipped(surface, colour, rect, width, clipping_rect):
    new_rect = rect.clip(clipping_rect)
    if new_rect.w == 0 or new_rect.h == 0:
        return
    render_surface = pygame.Surface((new_rect.w, new_rect.h))
    render_surface.fill((255, 0, 255))
    render_surface.set_colorkey((255, 0, 255))
    pygame.draw.rect(render_surface, colour, Rect(rect.x - new_rect.x, rect.y - new_rect.y, rect.w, rect.h), width)
    surface.blit(render_surface, new_rect)


def draw_arrow(surface, centre, size, angle):
    arrow_points = [
        (-0.75, 0.25),
        (-0.15, -0.6),
        (0.15, -0.6),
        (0.75, 0.25),
        (0.45, 0.45),
        (0.0, -0.15),
        (-0.45, 0.45)
    ]

    final_arrow_points = []

    for point in arrow_points:
        x = point[0]
        y = point[1]

        point_angle = math.atan2(y, x)
        point_dist = math.sqrt(x**2 + y**2)

        point_angle += angle

        final_arrow_points.append((centre[0] + int(math.cos(point_angle) * point_dist * size), centre[1] + int(math.sin(point_angle) * point_dist * size)))

    pygame.draw.polygon(surface, commons.text_col, final_arrow_points)


def make_comma_seperated_string(string_list, order_list=True):
    if order_list:
        string_list.sort()
    string = ""
    for i in range(len(string_list)):
        if i != 0:
            string += ","
        string += string_list[i]
    return string


def get_tags(dict_with_tags):
    tags = dict_with_tags["@tags"].split(",")
    if tags[0] == "":
        tags = []
    return tags

def get_item_prefixes(item):
    prefixes = item["@prefixes"].split(",")
    if prefixes[0] == "":
        prefixes = []
    return prefixes
