# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
import game_data
import methods
import os
from widget import WidgetBoxStyle

from crafting_tool import CraftingTool
from entity_tool import EntityTool
from item_tool import ItemTool
from loot_tool import LootTool
from structure_tool import StructureTool
from tile_tool import TileTool
from ai_tool import AITool
from sound_tool import SoundTool
from world_gen_tool import WorldGenTool
from projectile_tool import ProjectileTool
from wall_tool import WallTool
from widget_test import WidgetTest


def set_tool_using_str(tool_string):
    commons.screen_w = 1300
    commons.screen_h = 800

    if tool_string == "Crafting Tool":
        commons.current_tool = CraftingTool()
    elif tool_string == "Entity Tool":
        commons.current_tool = EntityTool()
    elif tool_string == "Item Tool":
        commons.current_tool = ItemTool()
    elif tool_string == "Loot Tool":
        commons.current_tool = LootTool()
    elif tool_string == "Structure Tool":
        commons.current_tool = StructureTool()
    elif tool_string == "Tile Tool":
        commons.current_tool = TileTool()
    elif tool_string == "AI Tool":
        commons.current_tool = AITool()
    elif tool_string == "Sound Tool":
        commons.current_tool = SoundTool()
    elif tool_string == "World Gen Tool":
        commons.current_tool = WorldGenTool()
    elif tool_string == "Projectile Tool":
        commons.current_tool = ProjectileTool()
    elif tool_string == "Wall Tool":
        commons.current_tool = WallTool()
    elif tool_string == "Widget Test":
        commons.current_tool = WidgetTest()

    commons.window = pygame.display.set_mode((commons.screen_w, commons.screen_h), pygame.RESIZABLE)


def get_tool_image_from_string(tool_string):
    if tool_string == "Crafting Tool":
        return commons.ct_icon
    elif tool_string == "Entity Tool":
        return commons.et_icon
    elif tool_string == "Item Tool":
        return commons.it_icon
    elif tool_string == "Loot Tool":
        return commons.lt_icon
    elif tool_string == "Structure Tool":
        return commons.st_icon
    elif tool_string == "Tile Tool":
        return commons.tt_icon
    elif tool_string == "Wall Tool":
        return commons.wt_icon
    elif tool_string == "AI Tool":
        return commons.at_icon
    elif tool_string == "World Gen Tool":
        return commons.wgt_icon
    elif tool_string == "Sound Tool":
        return commons.sot_icon
    elif tool_string == "Projectile Tool":
        return commons.pt_icon
    elif tool_string == "Widget Test":
        return commons.widget_test_icon


os.environ['PYTHONHASHSEED'] = '0'


pygame.init()
pygame.display.set_caption("Tool Selector")
commons.window = pygame.display.set_mode((400, 350))


font_names = ["Calibri", "Courier New", "Windings", "Microsoft Sans Serif", "res/fonts/monofonto.ttf", "res/fonts/VCR_OSD_MONO_1.001.ttf"]
font_name = "res/fonts/VCR_OSD_MONO_1.001.ttf"
font_sizes = [16, 25, 30, 40, 50, 60]
sys_font = False
bold = False
italic = False
commons.widget_text_y_offset = 1
commons.widget_padding_y = 4

icons_per_row = 4
icon_size = 100
icon_tool_names = ["Crafting Tool", "Entity Tool", "Item Tool", "Loot Tool", "Structure Tool", "Tile Tool", "AI Tool",
                   "Sound Tool", "World Gen Tool", "Projectile Tool", "Wall Tool", "Widget Test"]

if sys_font:
    commons.font_20 = pygame.font.SysFont(font_name, font_sizes[0], bold, italic)
    commons.font_25 = pygame.font.SysFont(font_name, font_sizes[1], bold, italic)
    commons.font_30 = pygame.font.SysFont(font_name, font_sizes[2], bold, italic)
    commons.font_40 = pygame.font.SysFont(font_name, font_sizes[3], bold, italic)
    commons.font_50 = pygame.font.SysFont(font_name, font_sizes[4], bold, italic)
    commons.font_60 = pygame.font.SysFont(font_name, font_sizes[5], bold, italic)
else:
    commons.font_20 = pygame.font.Font(font_name, font_sizes[0])
    commons.font_25 = pygame.font.Font(font_name, font_sizes[1])
    commons.font_30 = pygame.font.Font(font_name, font_sizes[2])
    commons.font_40 = pygame.font.Font(font_name, font_sizes[3])
    commons.font_50 = pygame.font.Font(font_name, font_sizes[4])
    commons.font_60 = pygame.font.Font(font_name, font_sizes[5])

menu_text = commons.font_40.render("Fegaria Tools", True, (255, 255, 255))

# Load/compile all cursors
commons.default_cursor = pygame.cursors.arrow
compiled_cursor = pygame.cursors.compile(commons.button_cursor_strings)
commons.button_cursor = (24, 24), (5, 0), compiled_cursor[0], compiled_cursor[1]
compiled_cursor = pygame.cursors.compile(pygame.cursors.sizer_x_strings)
commons.size_cursor_x = (24, 16), (9, 5), compiled_cursor[0], compiled_cursor[1]
compiled_cursor = pygame.cursors.compile(pygame.cursors.sizer_y_strings)
commons.size_cursor_y = (16, 24), (5, 9), compiled_cursor[0], compiled_cursor[1]
compiled_cursor = pygame.cursors.compile(commons.text_hover_strings)
commons.text_input_cursor = (16, 16), (5, 6), compiled_cursor[0], compiled_cursor[1]
compiled_cursor = pygame.cursors.compile(commons.long_boi_cursor_strings)
commons.long_boi_cursor = (24, 32), (5, 0), compiled_cursor[0], compiled_cursor[1]
compiled_cursor = None

commons.current_tool = None

commons.current_cursor = commons.default_cursor
current_cursor = commons.default_cursor
commons.widget_box_style = WidgetBoxStyle.GRADIENT_1

pygame.key.set_repeat(250, 40)

clock = pygame.time.Clock()

game_data.load_all_data()


running = True
has_focus = True
render_one_frame = True
frames_not_focused = 0
while running:
    commons.delta_time = clock.tick(commons.target_fps) * 0.001
    commons.mouse_diff = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if commons.current_tool is None:
            if event.type == pygame.QUIT:
                running = False
        else:
            commons.current_tool.process_event(event)

    if pygame.mouse.get_focused() == 0:
        frames_not_focused += 1
        has_focus = False
    else:
        has_focus = True

    if has_focus or render_one_frame:
        frames_not_focused = 0
        render_one_frame = False

        if not running:
            break

        if not pygame.mouse.get_pressed()[0]:
            commons.first_mouse_action = True
            commons.dragging_object = False

        commons.first_mouse_hover = True
        commons.first_scroll_action = True
        commons.current_cursor = commons.default_cursor

        if commons.dragging_object:
            commons.first_mouse_action = False
            commons.first_mouse_hover = False

        if commons.current_tool is None:
            if pygame.mouse.get_pressed()[0]:
                for icon_index in range(len(icon_tool_names)):
                    icon_x = icon_index % icons_per_row
                    icon_y = icon_index // icons_per_row
                    if Rect(icon_x * icon_size, 50 + icon_y * icon_size, 100, 100).collidepoint(pygame.mouse.get_pos()):
                        set_tool_using_str(icon_tool_names[icon_index])
                continue
        else:
            commons.current_tool.frame_update()
            if commons.current_tool is None:
                pygame.mixer.music.stop()
                if commons.next_tool != "":
                    set_tool_using_str(commons.next_tool)
                    commons.next_tool = ""
                else:
                    running = False
                continue

        if current_cursor != commons.current_cursor:
            current_cursor = commons.current_cursor
            pygame.mouse.set_cursor(*current_cursor)

        if commons.current_tool is None:
            commons.window.fill((68, 68, 68))
            commons.window.blit(menu_text, (5, 0))
            for icon_index in range(len(icon_tool_names)):
                icon_x = icon_index % icons_per_row
                icon_y = icon_index // icons_per_row
                commons.window.blit(get_tool_image_from_string(icon_tool_names[icon_index]), (icon_x * icon_size, 50 + icon_y * icon_size))

        else:
            commons.current_tool.draw()

        pygame.display.flip()
    else:
        if frames_not_focused < 30:
            first_frame_no_focus = True

            dark_surface = pygame.Surface((commons.screen_w, commons.screen_h))
            dark_surface.set_alpha(2)
            dark_surface.fill((255, 255, 255))
            commons.window.blit(dark_surface, (0, 0))
            pygame.display.flip()

pygame.quit()
