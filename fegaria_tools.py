# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
import game_data
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


pygame.init()
pygame.display.set_caption("Tool Selector")
commons.window = pygame.display.set_mode((300, 350))

commons.font_20 = pygame.font.Font("res/fonts/monofonto.ttf", 20)
commons.font_30 = pygame.font.Font("res/fonts/monofonto.ttf", 30)
commons.font_40 = pygame.font.Font("res/fonts/monofonto.ttf", 40)
commons.font_50 = pygame.font.Font("res/fonts/monofonto.ttf", 50)
commons.font_60 = pygame.font.Font("res/fonts/monofonto.ttf", 60)

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

game_data.load_item_data()
game_data.load_tile_data()
game_data.load_sound_data()
game_data.load_loot_data()
game_data.load_crafting_data()
game_data.load_ai_data()
game_data.load_entity_data()
game_data.load_world_gen_data()
game_data.load_structure_data()


running = True
while running:
    commons.delta_time = clock.tick(commons.target_fps) * 0.001
    commons.mouse_diff = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if commons.current_tool is None:
            if event.type == pygame.QUIT:
                running = False
        else:
            commons.current_tool.process_event(event)
            if commons.current_tool is None:
                if commons.next_tool == "":
                    # running = False
                    break

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
            if Rect(0, 50, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = CraftingTool()
            elif Rect(100, 50, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = EntityTool()
            elif Rect(200, 50, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = ItemTool()
            elif Rect(0, 150, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = LootTool()
            elif Rect(100, 150, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = StructureTool()
            elif Rect(200, 150, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = TileTool()
            elif Rect(0, 250, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = AITool()
            elif Rect(100, 250, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = WorldGenTool()
            elif Rect(200, 250, 100, 100).collidepoint(pygame.mouse.get_pos()):
                commons.current_tool = SoundTool()

            if commons.current_tool is not None:
                commons.screen_w = 1300
                commons.screen_h = 800

                commons.window = pygame.display.set_mode((commons.screen_w, commons.screen_h))
            continue
    else:
        commons.current_tool.frame_update()
        if commons.current_tool is None:
            if commons.next_tool != "":
                if commons.next_tool == "Crafting Tool":
                    commons.current_tool = CraftingTool()
                elif commons.next_tool == "Entity Tool":
                    commons.current_tool = EntityTool()
                elif commons.next_tool == "Item Tool":
                    commons.current_tool = ItemTool()
                elif commons.next_tool == "Loot Tool":
                    commons.current_tool = LootTool()
                elif commons.next_tool == "Structure Tool":
                    commons.current_tool = StructureTool()
                elif commons.next_tool == "Tile Tool":
                    commons.current_tool = TileTool()
                elif commons.next_tool == "AI Tool":
                    commons.current_tool = AITool()
                elif commons.next_tool == "Sound Tool":
                    commons.current_tool = SoundTool()
                elif commons.next_tool == "World Gen Tool":
                    commons.current_tool = WorldGenTool()
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
        commons.window.blit(commons.ct_icon, (0, 50))
        commons.window.blit(commons.et_icon, (100, 50))
        commons.window.blit(commons.it_icon, (200, 50))
        commons.window.blit(commons.lt_icon, (0, 150))
        commons.window.blit(commons.st_icon, (100, 150))
        commons.window.blit(commons.tt_icon, (200, 150))
        commons.window.blit(commons.at_icon, (0, 250))
        commons.window.blit(commons.wgt_icon, (100, 250))
        commons.window.blit(commons.sot_icon, (200, 250))
    else:
        commons.current_tool.draw()

    pygame.display.flip()

pygame.quit()
