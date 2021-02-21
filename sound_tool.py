# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class SoundTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Sound Tool"
        self.entity_type = "Sound"
        self.xml_data_root = game_data.sound_data
        self.xml_group_name = "sounds"
        self.xml_type_name = "sound"

        self.icon = commons.sot_icon_small
        self.accent_col = commons.sound_tool_col

        super().init()
