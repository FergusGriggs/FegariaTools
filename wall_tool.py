# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
import subprocess
import os
from base_tool import Tool
from widget import *
import game_data


class WallTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Wall Tool"
        self.entity_type = "Wall"
        self.xml_group_name = "walls"
        self.xml_type_name = "wall"

        self.set_xml_data_root()

        self.icon = commons.wt_icon_small
        self.accent_col = commons.wall_tool_col

        self.basic_properties_collapsed = False
        self.image_properties_collapsed = False
        self.mask_properties_collapsed = False
        self.sound_properties_collapsed = False
        self.loot_properties_collapsed = False

        self.wall_image_colourkey_active = True

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.wall_data

    def export_tool_data(self):
        game_data.save_wall_data()

    def reload_tool_data(self):
        game_data.load_wall_data()

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "open_wall_image_folder":
                dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\res\\images\\walls\\"
                subprocess.Popen(f'explorer "' + dir_path + '"')

        elif widget.type == WidgetType.TEXT_INPUT:
            if widget.widget_id == "wall_name":
                self.current_entity["@name"] = widget.text

            elif widget.widget_id == "wall_id_str":
                self.current_entity["@id_str"] = "fg.wall." + widget.text
                self.update_entity_list()
                self.reselect_current_entity()

            elif widget.widget_id == "image_file_path":
                self.current_entity["@image_path"] = widget.text

                wall_image_widget = self.find_container("entity_properties").find_widget("wall_image")
                wall_image_widget.set_image(methods.safe_load_image(widget.text), image_scale=4.0, update_container=False)
                if wall_image_widget.loaded:
                    self.find_container("entity_properties").find_widget("wall_image_load_fail").hide()
                else:
                    self.find_container("entity_properties").find_widget("wall_image_load_fail").show()
                self.update_container("entity_properties")

                self.find_container("entity_properties").find_widget("wall_image_back_checkbox").checked = True

            elif widget.widget_id == "wall_item_count_range":
                self.current_entity["@item_count_range"] = widget.text

            elif widget.widget_id == "wall_average_colour":
                self.current_entity["@average_colour"] = widget.text

        elif widget.type == WidgetType.BEGIN_COLLAPSE:
            if widget.widget_id == "basic_properties":
                self.basic_properties_collapsed = widget.collapsed

            elif widget.widget_id == "mask_properties":
                self.mask_properties_collapsed = widget.collapsed

            elif widget.widget_id == "image_properties":
                self.image_properties_collapsed = widget.collapsed

            elif widget.widget_id == "sound_properties":
                self.sound_properties_collapsed = widget.collapsed

            elif widget.widget_id == "loot_properties":
                self.loot_properties_collapsed = widget.collapsed

        elif widget.type == WidgetType.DROP_DOWN:
            if widget.widget_id == "wall_mask_type":
                self.current_entity["@mask_type"] = widget.selected_string

            elif widget.widget_id == "wall_mask_merge_id_strs":
                self.current_entity["@mask_merge_id_strs"] = methods.make_comma_seperated_string(widget.selected_strings)

            elif widget.widget_id == "wall_place_sound":
                self.current_entity["@place_sound"] = widget.selected_string

            elif widget.widget_id == "wall_hit_sound":
                self.current_entity["@hit_sound"] = widget.selected_string

            elif widget.widget_id == "wall_item_id_str":
                self.current_entity["@item_id_str"] = widget.selected_string

        super().widget_altered(widget)

    def load_property_page_for_entity(self, entity):
        wall_properties = self.find_container("entity_properties")
        wall_properties.widgets.clear()

        # Basic properties
        wall_properties.add_widget(BeginCollapseWidget("basic_properties", "Basic Properties", collapsed=self.basic_properties_collapsed))

        # Numerical Id
        wall_properties.add_widget(TextWidget("wall_id", "Id: " + entity["@id"]))

        # Name
        wall_properties.add_widget(TextWidget("wall_name_text", "Name:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(TextInputWidget("wall_name", entity["@name"], TextInputType.STRING))

        # String Id
        wall_properties.add_widget(TextWidget("wall_id_str_text", "Id Str:"))

        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset - commons.font_20.size("fg.wall.")[0]))
        wall_properties.add_widget(TextWidget("wall_id_str_text_pre", "fg.wall.", commons.selected_border_col))
        wall_properties.add_widget(SameLineWidget(0))
        wall_properties.add_widget(TextInputWidget("wall_id_str", entity["@id_str"].split(".")[-1], TextInputType.STRING))

        wall_properties.add_widget(EndCollapseWidget())

        # Mask properties
        wall_properties.add_widget(BeginCollapseWidget("mask_properties", "Mask Properties", collapsed=self.mask_properties_collapsed))

        # Mask Type
        wall_properties.add_widget(TextWidget("wall_mask_type_text", "Mask Type:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(DropDownWidget("wall_mask_type", ["None", "Noisy"], DropDownType.SELECT, initial_string=entity["@mask_type"]))

        # Mask Merge Id Strs
        wall_properties.add_widget(TextWidget("wall_mask_merge_id_strs_text", "Mask Merge Id Strs:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(DropDownWidget("wall_mask_merge_id_strs", game_data.wall_id_strs, DropDownType.MULTISELECT, initial_strings=entity["@mask_merge_id_strs"].split(",")))

        # Average Colour
        wall_properties.add_widget(TextWidget("wall_average_colour", "Average Colour:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(TextInputWidget("wall_average_colour", entity["@average_colour"], TextInputType.STRING))

        wall_properties.add_widget(EndCollapseWidget())

        # Image properties
        wall_properties.add_widget(BeginCollapseWidget("wall_image_properties", "Image Properties", collapsed=self.image_properties_collapsed))

        # Image path
        wall_properties.add_widget(TextWidget("image_path_text", "Image Path:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(TextInputWidget("image_file_path", entity["@image_path"], TextInputType.STRING))
        wall_properties.add_widget(SameLineWidget(10))
        wall_properties.add_widget(ButtonWidget("open_wall_image_folder", "Open Folder"))

        # Image
        wall_properties.add_widget(TextWidget("image_text", "Wall Image:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(ImageWidget("wall_image", methods.safe_load_image(entity["@image_path"]), image_scale=4.0))
        if not self.wall_image_colourkey_active:
            wall_properties.find_widget("wall_image").toggle_colourkey()

        # Load fail text
        wall_properties.add_widget(TextWidget("wall_image_load_fail", "Wall image failed to load", colour=(255, 128, 128)))
        wall_image_widget = wall_properties.find_widget("wall_image")
        if wall_image_widget.loaded:
            wall_properties.find_widget("wall_image_load_fail").hide()
        else:
            wall_properties.find_widget("wall_image_load_fail").show()

        # Colourkey checkbox
        wall_properties.add_widget(TextWidget("wall_image_back_checkbox_text", "Colourkey Active?"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(CheckboxWidget("wall_image_back_checkbox", checked=self.wall_image_colourkey_active))

        wall_properties.add_widget(EndCollapseWidget())

        # Loot properties
        wall_properties.add_widget(BeginCollapseWidget("loot_properties", "Loot Properties", collapsed=self.loot_properties_collapsed))

        # Item id str
        wall_properties.add_widget(TextWidget("wall_item_id_str_text", "Item Id Str:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(DropDownWidget("wall_item_id_str", game_data.item_id_strs, DropDownType.SELECT, initial_string=entity["@item_id_str"]))

        # Item count range
        wall_properties.add_widget(TextWidget("wall_item_count_range_text", "Item Count Range:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(TextInputWidget("wall_item_count_range", entity["@item_count_range"], TextInputType.INT_TUPLE, min_value=0))

        wall_properties.add_widget(EndCollapseWidget())

        # Sound properties
        wall_properties.add_widget(BeginCollapseWidget("sound_properties", "Sound Properties", collapsed=self.sound_properties_collapsed))

        # Place Sound
        wall_properties.add_widget(TextWidget("wall_place_sound_text", "Place Sound:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(DropDownWidget("wall_place_sound", game_data.sound_id_strs, DropDownType.SELECT, initial_string=entity["@place_sound"]))

        # Place Sound
        wall_properties.add_widget(TextWidget("wall_hit_sound_text", "Hit Sound:"))
        wall_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        wall_properties.add_widget(DropDownWidget("wall_hit_sound", game_data.sound_id_strs, DropDownType.SELECT, initial_string=entity["@hit_sound"]))

        wall_properties.add_widget(EndCollapseWidget())

        wall_properties.update(None)

    def get_default_entity_dict(self):
        entity_dict = super().get_default_entity_dict()

        entity_dict["@name"] = "UNNAMED"
        entity_dict["@image_path"] = "res/images/walls/"
        entity_dict["@mask_type"] = "Noisy"
        entity_dict["@mask_merge_id_strs"] = ""
        entity_dict["@average_colour"] = "255,0,255"

        entity_dict["@place_sound"] = "fg.sound.dig"
        entity_dict["@hit_sound"] = "fg.sound.dig"

        return entity_dict
