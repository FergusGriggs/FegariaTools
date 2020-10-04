# Pygame imports
import pygame
from pygame.locals import *

# Other imports
import random

# Project imports
import commons
from base_tool import Tool
from ui_container import UiContainer, SplitType
from widget import *
import game_data


class TileTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Tile Tool"
        self.icon = commons.tt_icon_small

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

        window_main.add_split(SplitType.HORIZONTAL, 170, True, "tile_list_section", "tile_properties_section")

        tile_list_section = self.find_container("tile_list_section")
        tile_list_section.add_split(SplitType.VERTICAL, 40, False, "tile_list_title", "tile_list")
        tile_list_section.split_line_colour = (4, 90, 66)

        tile_list_title = self.find_container("tile_list_title")
        tile_list_title.add_widget(TextWidget("tile_list_title", "Tiles", font=commons.font_30))
        tile_list_title.background_colour = (6, 135, 99)

        tile_list = self.find_container("tile_list")
        tile_list.background_colour = (60, 60, 60)

        # tile_list.add_widget(ButtonWidget("delete_selected", "Delete selected"))

        # tile_list.add_widget(TextWidget("tile_0_name", "Air"))
        # tile_list.add_widget(LineSelectorWidget("Air_selector"))
        # tile_list.add_widget(TextWidget("tile_1_name", "Dirt"))
        # tile_list.add_widget(LineSelectorWidget("Dirt_selector"))
        # tile_list.add_widget(TextWidget("tile_2_name", "Stone"))
        # tile_list.add_widget(LineSelectorWidget("Stone_selector"))
        # tile_list.add_widget(TextWidget("tile_3_name", "Wood"))
        # tile_list.add_widget(LineSelectorWidget("Wood_selector"))
        # tile_list.add_widget(TextWidget("tile_4_name", "Grass"))
        # tile_list.add_widget(LineSelectorWidget("Grass_selector"))

        tile_properties_section = self.find_container("tile_properties_section")
        tile_properties_section.add_split(SplitType.VERTICAL, 40, False, "tile_properties_title", "tile_properties")
        tile_properties_section.split_line_colour = (4, 90, 66)

        tile_properties_title = self.find_container("tile_properties_title")
        tile_properties_title.add_widget(TextWidget("tile_properties_title", "Tile Properties", font=commons.font_30))
        tile_properties_title.background_colour = (6, 135, 99)

        tile_properties = self.find_container("tile_properties")
        # tile_properties.add_widget(TextWidget("random_text_0", "Some text"))
        # tile_properties.add_widget(TextWidget("click_me_text", "Click me ->"))
        # tile_properties.add_widget(SameLineWidget(10))
        # tile_properties.add_widget(CheckboxWidget("test_checkbox_1"))
        #
        # tile_properties.add_widget(TextWidget("random_text_1", "Wow,"))
        # tile_properties.add_widget(SameLineWidget(10))
        # tile_properties.add_widget(TextWidget("random_text_2", "look at this image!", colour=(255, 128, 128)))
        # tile_properties.add_widget(SameLineWidget(10))
        # tile_properties.add_widget(ImageWidget("test_image", commons.tt_icon))
        # tile_properties.add_widget(SameLineWidget(10))
        # tile_properties.add_widget(ButtonWidget("test_button_3", "What's gonna happen?"))
        # tile_properties.add_widget(LineSelectorWidget("image_line_selector"))
        #
        # tile_properties.add_widget(TextWidget("random_text_3", "Am I gonna move? I bloodeh hope so"))
        # tile_properties.add_widget(TextWidget("random_text_4", "This is wild: "))
        # tile_properties.add_widget(SameLineWidget(0))
        # tile_properties.add_widget(ButtonWidget("test_button", "Press me!"))
        # tile_properties.add_widget(ButtonWidget("test_button_2", "Big boi", font=commons.font_60))
        #
        # tile_properties.add_widget(TextInputWidget("text_input", "Change Me!", TextInputType.STRING))

    def widget_altered(self, widget):
        if widget.type == WidgetType.CHECKBOX:
            if widget.widget_id == "test_checkbox_1":
                self.main_window.find_widget("test_checkbox_2").toggle_hidden()
                self.main_window.split_children[0].update(None)
            elif widget.widget_id == "test_checkbox_2":
                self.main_window.find_widget("test_image").toggle_hidden()
                self.main_window.split_children[1].update(None)
        elif widget.type == WidgetType.BUTTON:
            if widget.widget_id == "test_button":
                messages = ["Once more?", "Again?", "That's the spot!", "Keep em coming!", "Cheers!", "Heheh yeys"]
                widget.set_text(messages[random.randint(0, len(messages) - 1)])
                self.main_window.split_children[1].update(None)
        super().widget_altered(widget)

