# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data


class ProjectileTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Projectile Tool"
        self.entity_type = "Projectile"
        self.xml_group_name = "projectiles"
        self.xml_type_name = "projectile"

        self.set_xml_data_root()

        self.icon = commons.pt_icon_small
        self.accent_col = commons.projectile_tool_col

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.projectile_data

    def reload_tool_data(self):
        game_data.load_projectile_data()

    def export_tool_data(self):
        game_data.save_projectile_data()

    def widget_altered(self, widget):
        super().widget_altered(widget)

    def load_property_page_for_entity(self, entity):
        entity_properties = self.find_container("entity_properties")

        entity_properties.update(None)
