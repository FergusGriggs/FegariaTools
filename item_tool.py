# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from ui_container import SplitType
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

        self.main_window.split_line_colour = (8, 179, 132)

        window_top_bar = self.find_container("window_top_bar")
        window_top_bar.add_widget(SameLineWidget(10))
        window_top_bar.add_widget(ButtonWidget("export_data", "Export"))
        window_top_bar.add_widget(SameLineWidget(10))
        window_top_bar.add_widget(ButtonWidget("load_data", "Load"))

        window_main = self.find_container("window_main")
        window_main.draw_line = False

        window_main.add_split(SplitType.HORIZONTAL, 170, True, "item_list_section", "item_properties_section")

        item_list_section = self.find_container("item_list_section")
        item_list_section.add_split(SplitType.VERTICAL, 40, False, "item_list_title", "item_list")
        item_list_section.split_line_colour = (4, 90, 66)

        item_list_title = self.find_container("item_list_title")
        item_list_title.add_widget(TextWidget("item_list_title", "Item List", font=commons.font_30))
        item_list_title.background_colour = (6, 135, 99)

        item_list = self.find_container("item_list")
        item_list.background_colour = (60, 60, 60)

        item_properties_section = self.find_container("item_properties_section")
        item_properties_section.add_split(SplitType.VERTICAL, 40, False, "item_properties_title", "item_properties")
        item_properties_section.split_line_colour = (4, 90, 66)

        item_properties_title = self.find_container("item_properties_title")
        item_properties_title.add_widget(TextWidget("item_properties_title", "Item Properties", font=commons.font_30))
        item_properties_title.background_colour = (6, 135, 99)

        item_properties = self.find_container("item_properties")

        self.create_item_list()

    def create_item_list(self):
        item_list = self.find_container("item_list")
        item_list.widgets.clear()

        for element in game_data.item_data["items"]["item"]:
            item_list.add_widget(TextWidget(element["@name"], element["@name"]))
            item_list.add_widget(LineSelectorWidget("selector_" + element["@name"]))

        item_list.update(None)

    def load_property_page_for_item(self, item):
        item_properties = self.find_container("item_properties")
        item_properties.widgets.clear()

        item_properties.add_widget(TextWidget("item_id", "Id: " + item["@id"]))
        item_properties.add_widget(TextWidget("item_name", "Name: " + item["@name"]))
        item_properties.add_widget(TextWidget("item_strength", "Strength: " + item["@strength"]))

        item_properties.update(None)

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "reload_item_data":
                game_data.load_item_data()
                self.create_item_list()
        if widget.type == WidgetType.LINE_SELECTOR:
            self.find_container("item_list").deselect_all()
            widget.selected = True
            item = game_data.find_element_by_attribute(game_data.item_data["items"]["item"], "@name", widget.widget_id.split("_")[1])
            self.load_property_page_for_item(item)

        super().widget_altered(widget)

    def quit(self):
        super().quit()

        game_data.unload_item_data()
