# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data
import os
import random


class SoundTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Sound Tool"
        self.entity_type = "Sound"
        self.xml_group_name = "sounds"
        self.xml_type_name = "sound"

        self.set_xml_data_root()

        self.icon = commons.sot_icon_small
        self.accent_col = commons.sound_tool_col

        self.basic_properties_collapsed = False

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.sound_data

    def export_tool_data(self):
        game_data.save_sound_data()

    def reload_tool_data(self):
        game_data.load_sound_data()

    def load_property_page_for_entity(self, entity):
        sound_properties = self.main_window.find_container("entity_properties")
        sound_properties.widgets.clear()

        # Basic properties
        sound_properties.add_widget(BeginCollapseWidget("sound_basic_properties", "Basic Properties", collapsed=self.basic_properties_collapsed))

        # Numerical Id
        sound_properties.add_widget(TextWidget("sound_id", "Id: " + entity["@id"]))

        # String Id
        sound_properties.add_widget(TextWidget("sound_id_str_text", "Id Str:"))
        sound_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset - commons.font_20.size("fg.sound.")[0]))
        sound_properties.add_widget(TextWidget("sound_id_str_text_pre", "fg.sound.", commons.selected_border_col))
        sound_properties.add_widget(SameLineWidget(0))
        sound_properties.add_widget(TextInputWidget("sound_id_str", entity["@id_str"].split(".")[-1], TextInputType.STRING))

        # Variation paths
        path = "res/sounds"
        available_sound_paths = os.listdir(path)
        selected_sound_paths = methods.trim_strings(entity["@variation_paths"].split(","), front_trim=11)

        sound_properties.add_widget(TextWidget("variation_paths_text", "Variation Paths:"))
        sound_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        sound_properties.add_widget(DropDownWidget("sound_variation_paths", available_sound_paths, DropDownType.MULTISELECT, initial_strings=selected_sound_paths))

        sound_properties.add_widget(TextWidget("sound_volume_text", "Sound Volume:"))
        sound_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        sound_properties.add_widget(TextInputWidget("sound_volume", entity["@volume"], TextInputType.FLOAT, min_value=0.0, max_value=1.0))

        sound_properties.add_widget(ButtonWidget("play_random_variation", "Play Random Variation"))

        sound_properties.add_widget(EndCollapseWidget())

        sound_properties.update(None)

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "play_random_variation":
                variation_paths = self.find_container("entity_properties").find_widget("sound_variation_paths").selected_strings
                if len(variation_paths) > 0:
                    random_string = variation_paths[random.randint(0, len(variation_paths) - 1)]
                    if random_string[-4:] == ".mp3":
                        pygame.mixer.music.load("res/sounds/" + random_string)
                        pygame.mixer.music.set_volume(float(self.current_entity["@volume"]))
                        pygame.mixer.music.play()
                    else:
                        sound = pygame.mixer.Sound("res/sounds/" + random_string)
                        sound.set_volume(float(self.current_entity["@volume"]))
                        sound.play()

        elif widget.type == WidgetType.TEXT_INPUT:
            if widget.widget_id == "sound_id":
                self.current_entity["@id"] = widget.text

            elif widget.widget_id == "sound_id_str":
                self.current_entity["@id_str"] = "fg.sound." + widget.text
                self.update_entity_list()
                self.reselect_current_entity()

            elif widget.widget_id == "sound_volume":
                self.current_entity["@volume"] = widget.text

        elif widget.type == WidgetType.DROP_DOWN:
            if widget.widget_id == "sound_variation_paths":
                self.current_entity["@variation_paths"] = methods.make_comma_seperated_string(widget.selected_strings, pre_string="res/sounds/")

        super().widget_altered(widget)

    def get_default_entity_dict(self):
        entity_dict = super().get_default_entity_dict()

        entity_dict["@variation_paths"] = ""
        entity_dict["@volume"] = ""

        return entity_dict
