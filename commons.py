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

window = None
current_tool = None

font_20 = None
font_30 = None
font_40 = None
font_50 = None
font_60 = None

first_mouse_action = False
first_mouse_hover = False

text_col = (255, 255, 255)
back_col = (50, 50, 50)
border_col = (90, 90, 90)

default_cursor = None
size_cursor_x = None
size_cursor_y = None
button_cursor = None
text_input_cursor = None
current_cursor = None

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
  "     .XXXXXXXX.         ",
  "     ..........         ",
  "                        ",
  "                        ")

