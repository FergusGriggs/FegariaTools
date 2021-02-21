# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
import game_data


class EntityTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Entity Tool"
        self.entity_type = "Entity"
        self.xml_data_root = game_data.entity_data
        self.xml_group_name = "entities"
        self.xml_type_name = "entity"

        self.icon = commons.et_icon_small
        self.accent_col = commons.entity_tool_col

        super().init()
