import pygame


screen_w = 600
screen_h = 150

ct_icon_small = pygame.image.load("res/images/icons/40x40/crafting_tool.png")
et_icon_small = pygame.image.load("res/images/icons/40x40/entity_tool.png")
it_icon_small = pygame.image.load("res/images/icons/40x40/item_tool.png")
lt_icon_small = pygame.image.load("res/images/icons/40x40/loot_tool.png")
st_icon_small = pygame.image.load("res/images/icons/40x40/structure_tool.png")
tt_icon_small = pygame.image.load("res/images/icons/40x40/tile_tool.png")

ct_icon = pygame.image.load("res/images/icons/100x100/crafting_tool.png")
et_icon = pygame.image.load("res/images/icons/100x100/entity_tool.png")
it_icon = pygame.image.load("res/images/icons/100x100/item_tool.png")
lt_icon = pygame.image.load("res/images/icons/100x100/loot_tool.png")
st_icon = pygame.image.load("res/images/icons/100x100/structure_tool.png")
tt_icon = pygame.image.load("res/images/icons/100x100/tile_tool.png")

placeholder_image = pygame.image.load("res/images/misc/placeholder.png")

window = None
current_tool = None

font_20 = None
font_30 = None
font_40 = None
font_50 = None
font_60 = None

first_mouse_action = False
first_mouse_hover = False
dragging_object = False

text_col = (255, 255, 255)
back_col = (50, 50, 50)
border_col = (90, 90, 90)
hover_border_col = (128, 128, 128)
selected_border_col = (192, 192, 192)

item_tool_col = (65, 141, 255)
tile_tool_col = (7, 155, 115)

colour_key_col = (255, 0, 255)

delta_time = 0.0
target_fps = 144

x_scroll_bar_width = 13
x_scroll_bar_spacing = x_scroll_bar_width * 1.0
y_scroll_bar_width = 10
y_scroll_bar_spacing = y_scroll_bar_width * 1.0

mouse_diff = (0, 0)

default_cursor = None
size_cursor_x = None
size_cursor_y = None
button_cursor = None
text_input_cursor = None
current_cursor = None
long_boi_cursor = None

text_hover_strings = (
  "  .... ....     ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "      .         ",
  "  .... ....     ")

button_cursor_strings = (
  "     ..                 ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX...              ",
  "    .XX.XX...           ",
  "    .XX.XX.XX..         ",
  "    .XX.XX.XX.X.        ",
  "... .XX.XX.XX.XX.       ",
  ".XX..XXXXXXXX.XX.       ",
  ".XXX.XXXXXXXXXXX.       ",
  " .XXXXXXXXXXXXXX.       ",
  "  .XXXXXXXXXXXXX.       ",
  "  .XXXXXXXXXXXXX.       ",
  "   .XXXXXXXXXXXX.       ",
  "   .XXXXXXXXXXX.        ",
  "    .XXXXXXXXXX.        ",
  "    .XXXXXXXXXX.        ",
  "     .XXXXXXXX.         ",
  "      .XXXXXX.          ",
  "       ......           ",
  "                        ",
  "                        ")

long_boi_cursor_strings = (
  "     ..                 ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX.                ",
  "    .XX...              ",
  "    .XX.XX...           ",
  "    .XX.XX.XX..         ",
  "    .XX.XX.XX.X.        ",
  "... .XX.XX.XX.XX.       ",
  ".XX..XXXXXXXX.XX.       ",
  ".XXX.XXXXXXXXXXX.       ",
  " .XXXXXXXXXXXXXX.       ",
  "  .XXXXXXXXXXXXX.       ",
  "  .XXXXXXXXXXXXX.       ",
  "   .XXXXXXXXXXXX.       ",
  "   .XXXXXXXXXXX.        ",
  "    .XXXXXXXXXX.        ",
  "    .XXXXXXXXXX.        ",
  "     .XXXXXXXX.         ",
  "      .XXXXXX.          ",
  "       ......           ",
  "                        ",
  "                        ")

