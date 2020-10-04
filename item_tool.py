# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data


class ItemTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Item Tool"
        self.icon = commons.it_icon_small

        game_data.load_item_data()

        super().init()

    def create_windows(self):
        super().create_windows()

        self.main_window.split_children[0].add_widget(SameLineWidget(10))
        self.main_window.split_children[0].add_widget(ButtonWidget("reload_item_data", "Reload item data"))

        self.create_item_list()

    def create_item_list(self):
        self.main_window.split_children[1].widgets.clear()

        for element in game_data.item_data["items"]["item"]:
            self.main_window.split_children[1].add_widget(TextWidget(element["@name"], element["@name"]))

        self.main_window.split_children[1].update(None)

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "reload_item_data":
                game_data.load_item_data()
                self.create_item_list()

    def quit(self):
        super().quit()

        game_data.unload_item_data()
