# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class AITool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "AI Tool"
        self.entity_type = "AI"
        self.xml_data_root = game_data.ai_data
        self.xml_group_name = "ais"
        self.xml_type_name = "ai"

        self.icon = commons.at_icon_small
        self.accent_col = commons.ai_tool_col

        super().init()
