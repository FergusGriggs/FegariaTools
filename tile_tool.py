
# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
import subprocess
import os
from ui_container import SplitType, SortType
from base_tool import Tool
from widget import *
import game_data
import ui_container

# Other imports
import collections

class TileTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Tile Tool"
        self.entity_type = "Tile"
        self.xml_data_root = game_data.tile_data
        self.xml_group_name = "tiles"
        self.xml_type_name = "tile"

        self.icon = commons.tt_icon_small
        self.accent_col = commons.tile_tool_col

        self.tile_image_colourkey_active = True

        self.tile_list_sort_type = SortType.BY_ID

        self.basic_properties_collapsed = False
        self.tags_collapsed = True
        self.multitile_properties_collapsed = False
        self.image_properties_collapsed = False
        self.loot_properties_collapsed = False
        self.cyclable_properties_collapsed = False

        super().init()

    def load_property_page_for_entity(self, entity):
        tile_properties = self.find_container("entity_properties")
        tile_properties.widgets.clear()

        # Basic properties
        tile_properties.add_widget(BeginCollapseWidget("tile_basic_properties", "Basic Properties", collapsed=self.basic_properties_collapsed))

        # Numerical Id
        tile_properties.add_widget(TextWidget("tile_id", "Id: " + entity["@id"]))

        # Name
        tile_properties.add_widget(TextWidget("tile_name", "Name:"))
        tile_properties.add_widget(SameLineFillToLineWidget(250))
        tile_properties.add_widget(TextInputWidget("tile_name_input", entity["@name"], TextInputType.STRING))

        # String Id
        tile_properties.add_widget(TextWidget("tile_id_str_text", "Id Str:"))
        tile_properties.add_widget(SameLineFillToLineWidget(170))
        tile_properties.add_widget(TextWidget("tile_id_str_text_pre", "fg.tile.", commons.selected_border_col))
        tile_properties.add_widget(SameLineWidget(0))
        tile_properties.add_widget(TextInputWidget("tile_id_str", entity["@id_str"][8:], TextInputType.STRING))

        # Strength
        tile_properties.add_widget(TextWidget("tile_strength_text", "Strength:"))
        tile_properties.add_widget(SameLineFillToLineWidget(250))
        tile_properties.add_widget(TextInputWidget("tile_strength", entity["@strength"], TextInputType.FLOAT))

        # Light Reduction
        tile_properties.add_widget(TextWidget("tile_light_reduction_text", "Light Reduction:"))
        tile_properties.add_widget(SameLineFillToLineWidget(250))
        tile_properties.add_widget(TextInputWidget("tile_light_reduction", entity["@light_reduction"], TextInputType.INT, min_value=0, max_value=10))

        # Light Emission
        tile_properties.add_widget(TextWidget("tile_light_emission_text", "Light Emission:"))
        tile_properties.add_widget(SameLineFillToLineWidget(250))
        tile_properties.add_widget(TextInputWidget("tile_light_emission", entity["@light_emission"], TextInputType.INT,  min_value=0, max_value=32))

        # Strength Type
        tile_properties.add_widget(TextWidget("strength_type_text", "Strength Type:"))
        tile_properties.add_widget(SameLineFillToLineWidget(250))
        tile_properties.add_widget(DropDownWidget("strength_type", ["Hammer", "Pickaxe", "Axe"], DropDownType.SELECT, initial_string="fg.strength.axe"))

        tile_properties.add_widget(EndCollapseWidget())

        # Tile tags
        tile_properties.add_widget(BeginCollapseWidget("tile_tags", "Tags [" + entity["@tags"] + "]", collapsed=self.tags_collapsed))

        tile_properties.add_widget(TextWidget("tile_tags_intro", "Select any tags that apply to the tile (Additional menus may appear at the bottom)"))

        tags = methods.get_tags(entity)

        tile_properties.add_widget(CheckboxWidget("tiletag_nowall", checked=("nowall" in tags)))
        tile_properties.add_widget(SameLineWidget(10))
        tile_properties.add_widget(TextWidget("nowall_tag_text", "nowall"))

        tile_properties.add_widget(CheckboxWidget("tiletag_nocollide", checked=("nocollide" in tags)))
        tile_properties.add_widget(SameLineWidget(10))
        tile_properties.add_widget(TextWidget("nocollide_tag_text", "nocollide"))

        tile_properties.add_widget(CheckboxWidget("tiletag_multitile", checked=("multitile" in tags)))
        tile_properties.add_widget(SameLineWidget(10))
        tile_properties.add_widget(TextWidget("multitile_tag_text", "multitile"))

        tile_properties.add_widget(CheckboxWidget("tiletag_cyclable", checked=("cyclable" in tags)))
        tile_properties.add_widget(SameLineWidget(10))
        tile_properties.add_widget(TextWidget("cyclable_tag_text", "cyclable"))

        tile_properties.add_widget(CheckboxWidget("tiletag_chest", checked=("chest" in tags)))
        tile_properties.add_widget(SameLineWidget(10))
        tile_properties.add_widget(TextWidget("chest_tag_text", "chest"))

        tile_properties.add_widget(CheckboxWidget("tiletag_breakable", checked=("breakable" in tags)))
        tile_properties.add_widget(SameLineWidget(10))
        tile_properties.add_widget(TextWidget("breakable_tag_text", "breakable"))

        tile_properties.add_widget(CheckboxWidget("tiletag_crafttable", checked=("crafttable" in tags)))
        tile_properties.add_widget(SameLineWidget(10))
        tile_properties.add_widget(TextWidget("crafting_table_tag_text", "crafting_table"))

        tile_properties.add_widget(TextWidget("tile_tags_text", "Tile Tags: [" + entity["@tags"] + "]"))
        tile_properties.add_widget(SameLineWidget(10))
        tile_properties.add_widget(ButtonWidget("clear_tile_tags", "Clear Tags"))

        tile_properties.add_widget(EndCollapseWidget())

        # Multitile properties
        if "multitile" in tags:
            tile_properties.add_widget(BeginCollapseWidget("multitile_properties", "Multitile Properties", collapsed=self.multitile_properties_collapsed))

            tile_properties.add_widget(TextWidget("tile_multitile_image_path_text", "Multitile Image Path:"))
            tile_properties.add_widget(SameLineFillToLineWidget(250))
            tile_properties.add_widget(TextInputWidget("tile_multitile_image_path", entity["@multitile_image_path"], TextInputType.STRING))
            tile_properties.add_widget(SameLineWidget(10))
            tile_properties.add_widget(ButtonWidget("open_multitile_image_folder", "Open Folder"))

            tile_properties.add_widget(TextWidget("tile_multitile_image_text", "Multitile Image:"))
            tile_properties.add_widget(SameLineFillToLineWidget(250))
            tile_properties.add_widget(ImageWidget("tile_multitile_image", methods.safe_load_image(entity["@multitile_image_path"]), image_scale=4.0))

            tile_image_widget = tile_properties.find_widget("tile_multitile_image")
            if not self.tile_image_colourkey_active:
                tile_image_widget.toggle_colourkey()

            if tile_image_widget.loaded:
                tile_image_widget.add_tile_lines()

            tile_properties.add_widget(TextWidget("tile_image_back_checkbox_text", "Colourkey Active?"))
            tile_properties.add_widget(SameLineFillToLineWidget(250))
            tile_properties.add_widget(CheckboxWidget("tile_image_back_checkbox", checked=self.tile_image_colourkey_active))

            tile_properties.add_widget(TextWidget("tile_multitile_dimensions_text", "Multitile Dimensions:"))
            tile_properties.add_widget(SameLineFillToLineWidget(250))
            tile_properties.add_widget(TextInputWidget("tile_multitile_dimensions", entity["@multitile_dimensions"], TextInputType.INT_TUPLE))

            tile_properties.add_widget(EndCollapseWidget())

        # Cyclable Properties
        if "cyclable" in tags:
            tile_properties.add_widget(BeginCollapseWidget("cyclable_properties", "Cyclable Properties", collapsed=self.cyclable_properties_collapsed))

            tile_properties.add_widget(TextWidget("tile_cycle_facing_left_tile_id_str", "Cycle Facing Left Tile Id Str:"))
            tile_properties.add_widget(SameLineFillToLineWidget(330))
            tile_properties.add_widget(DropDownWidget("tile_cycle_facing_left_tile_id_str", game_data.tile_id_strs, DropDownType.SELECT, initial_string=entity["@cycle_facing_left_tile_id_str"]))

            tile_properties.add_widget(TextWidget("tile_cycle_facing_left_tile_offset_text", "Cycle Facing Left Tile Offset:"))
            tile_properties.add_widget(SameLineFillToLineWidget(330))
            tile_properties.add_widget(TextInputWidget("tile_cycle_facing_left_tile_offset", entity["@cycle_facing_left_tile_offset"], TextInputType.INT_TUPLE))

            tile_properties.add_widget(TextWidget("tile_cycle_facing_right_tile_id_str", "Cycle Facing Right Tile Id Str:"))
            tile_properties.add_widget(SameLineFillToLineWidget(330))
            tile_properties.add_widget(DropDownWidget("tile_cycle_facing_right_tile_id_str", game_data.tile_id_strs, DropDownType.SELECT, initial_string=entity["@cycle_facing_right_tile_id_str"]))

            tile_properties.add_widget(TextWidget("tile_cycle_facing_right_tile_offset_text", "Cycle Facing Right Tile Offset:"))
            tile_properties.add_widget(SameLineFillToLineWidget(330))
            tile_properties.add_widget(TextInputWidget("tile_cycle_facing_right_tile_offset", entity["@cycle_facing_right_tile_offset"], TextInputType.INT_TUPLE))

            tile_properties.add_widget(TextWidget("tile_cycle_sound_id_str_text", "Cycle Sound Id Str:"))
            tile_properties.add_widget(SameLineFillToLineWidget(330))
            tile_properties.add_widget(DropDownWidget("tile_cycle_sound_id_str", game_data.sound_id_strs, DropDownType.SELECT, initial_string=""))

            tile_properties.add_widget(EndCollapseWidget())

        # Image properties
        if "multitile" not in tags:
            tile_properties.add_widget(BeginCollapseWidget("tile_image_properties", "Image Properties", collapsed=self.image_properties_collapsed))

            tile_properties.add_widget(TextWidget("image_path", "Image Path:"))
            tile_properties.add_widget(SameLineFillToLineWidget(250))
            tile_properties.add_widget(TextInputWidget("image_file_path_input", entity["@image_path"], TextInputType.STRING))
            tile_properties.add_widget(SameLineWidget(10))
            tile_properties.add_widget(ButtonWidget("open_tile_image_folder", "Open Folder"))

            tile_properties.add_widget(TextWidget("image_text", "Tile Image:"))
            tile_properties.add_widget(SameLineFillToLineWidget(250))
            tile_properties.add_widget(ImageWidget("tile_image", methods.safe_load_image(entity["@image_path"]), image_scale=4.0))
            if not self.tile_image_colourkey_active:
                tile_properties.find_widget("tile_image").toggle_colourkey()

            tile_properties.add_widget(TextWidget("tile_image_load_fail", "Tile image failed to load", colour=(255, 128, 128)))
            tile_image_widget = tile_properties.find_widget("tile_image")
            if tile_image_widget.loaded:
                tile_properties.find_widget("tile_image_load_fail").hide()
            else:
                tile_properties.find_widget("tile_image_load_fail").show()

            tile_properties.add_widget(TextWidget("tile_image_back_checkbox_text", "Colourkey Active?"))
            tile_properties.add_widget(SameLineFillToLineWidget(250))
            tile_properties.add_widget(CheckboxWidget("tile_image_back_checkbox", checked=self.tile_image_colourkey_active))

            tile_properties.add_widget(EndCollapseWidget())

        # Loot properties
        tile_properties.add_widget(BeginCollapseWidget("loot_properties", "Loot Properties", collapsed=self.loot_properties_collapsed))

        tile_properties.add_widget(TextWidget("tile_item_id_str_text", "Item Id Str:"))
        tile_properties.add_widget(SameLineFillToLineWidget(250))
        tile_properties.add_widget(DropDownWidget("tile_item_id_str", game_data.item_id_strs, DropDownType.SELECT, initial_string=entity["@item_id_str"]))

        if "breakable" in tags:
            tile_properties.add_widget(TextWidget("tile_loot_group_id_str_text", "Loot Group Id Str:"))
            tile_properties.add_widget(SameLineFillToLineWidget(250))
            tile_properties.add_widget(DropDownWidget("tile_loot_group_id_str", game_data.loot_id_strs, DropDownType.SELECT, initial_string=entity["@loot_group_id_str"]))

        tile_properties.add_widget(EndCollapseWidget())

        tile_properties.update(None)

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "export_data":
                game_data.save_tile_data()

            elif widget.widget_id == "load_data":
                game_data.load_tile_data()
                self.update_entity_list()

                self.reselect_current_entity()
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id == "clear_tile_tags":
                tags = methods.get_tags(self.current_entity)
                tags.clear()
                self.current_entity["@tags"] = methods.make_comma_seperated_string(tags)
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id == "open_tile_image_folder":
                dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\res\\images\\tiles\\"
                subprocess.Popen(f'explorer "' + dir_path + '"')

            elif widget.widget_id == "open_multitile_image_folder":
                dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\res\\images\\tiles\\multitiles\\"
                subprocess.Popen(f'explorer "' + dir_path + '"')

        elif widget.type == WidgetType.TEXT_INPUT:
            if widget.widget_id == "tile_name_input":
                self.current_entity["@name"] = widget.text

            elif widget.widget_id == "tile_id_str":
                self.current_entity["@id_str"] = "fg.tile." + widget.text
                self.update_entity_list()
                self.reselect_current_entity()

            elif widget.widget_id == "tile_strength":
                self.current_entity["@strength"] = widget.text

            elif widget.widget_id == "tile_light_reduction":
                self.current_entity["@light_reduction"] = widget.text

            elif widget.widget_id == "tile_light_emission":
                self.current_entity["@light_emission"] = widget.text

            elif widget.widget_id == "image_file_path_input":
                self.current_entity["@image_path"] = widget.text

                tile_image_widget = self.find_container("tile_properties").find_widget("tile_image")
                tile_image_widget.set_image(methods.safe_load_image(widget.text), image_scale=4.0, pdate_container=False)
                if tile_image_widget.loaded:
                    self.find_container("tile_properties").find_widget("tile_image_load_fail").hide()
                else:
                    self.find_container("tile_properties").find_widget("tile_image_load_fail").show()
                self.update_container("tile_properties")

                self.find_container("tile_properties").find_widget("tile_image_back_checkbox").checked = True

            elif widget.widget_id == "tile_multitile_image_path":
                self.current_entity["@multitile_image_path"] = widget.text

                tile_image_widget = self.find_container("tile_properties").find_widget("tile_multitile_image")
                tile_image_widget.set_image(methods.safe_load_image(widget.text), image_scale=4.0, update_container=False)

                if tile_image_widget.loaded:
                    tile_image_widget.add_tile_lines()

                self.update_container("tile_properties")

            elif widget.widget_id == "tile_multitile_dimensions":
                self.current_entity["@multitile_dimensions"] = widget.text

            elif widget.widget_id == "tile_item_id_str":
                self.current_entity["@item_id_str"] = "fg.item." + widget.text

            elif widget.widget_id == "tile_loot_group_id_str":
                self.current_entity["@loot_group_id_str"] = "fg.loot." + widget.text

            elif widget.widget_id == "tile_cycle_facing_left_tile_id_str":
                self.current_entity["@cycle_facing_left_tile_id_str"] = "fg.tile." + widget.text

            elif widget.widget_id == "tile_cycle_facing_left_tile_offset":
                self.current_entity["@cycle_facing_left_tile_offset"] = widget.text

            elif widget.widget_id == "tile_cycle_facing_right_tile_id_str":
                self.current_entity["@cycle_facing_right_tile_id_str"] = "fg.tile." + widget.text

            elif widget.widget_id == "tile_cycle_facing_right_tile_offset":
                self.current_entity["@cycle_facing_right_tile_offset"] = widget.text

        elif widget.type == WidgetType.CHECKBOX:
            split_id = widget.widget_id.split("_")
            if len(split_id) > 0:
                if split_id[0] == "tiletag":
                    self.modify_tile_tags(split_id[1], widget.checked)
                    self.load_property_page_for_entity(self.current_entity)

            if widget.widget_id == "tile_image_back_checkbox":
                tile_properties = self.find_container("tile_properties")

                tile_image = tile_properties.find_widget("tile_image")
                if tile_image is not None:
                    tile_image.toggle_colourkey()

                tile_multitile_image = tile_properties.find_widget("tile_multitile_image")
                if tile_multitile_image is not None:
                    tile_multitile_image.toggle_colourkey()

                tile_properties.render_widget_surface()
                self.tile_image_colourkey_active = not self.tile_image_colourkey_active

        elif widget.type == WidgetType.BEGIN_COLLAPSE:
            if widget.widget_id == "tile_basic_properties":
                self.basic_properties_collapsed = widget.collapsed
            elif widget.widget_id == "tile_tags":
                self.tags_collapsed = widget.collapsed
            elif widget.widget_id == "multitile_properties":
                self.multitile_properties_collapsed = widget.collapsed
            elif widget.widget_id == "loot_properties":
                self.loot_properties_collapsed = widget.collapsed
            elif widget.widget_id == "cyclable_properties":
                self.cyclable_properties_collapsed = widget.collapsed

        super().widget_altered(widget)

    def quit(self):
        super().quit()

    def modify_tile_tags(self, tag_name, adding):
        tags = methods.get_tags(self.current_entity)
        if adding:
            if tag_name not in tags:
                tags.append(tag_name)
                self.current_entity["@tags"] = methods.make_comma_seperated_string(tags)
        else:
            tags.remove(tag_name)
            self.current_entity["@tags"] = methods.make_comma_seperated_string(tags)

        if tag_name == "multitile":
            if adding:
                self.current_entity["@multitile_image_path"] = "res/images/tiles/multitiles/"
                self.current_entity["@multitile_dimensions"] = "0,0"

            else:
                del self.current_entity["@multitile_image_path"]
                del self.current_entity["@multitile_dimensions"]

        elif tag_name == "breakable":
            if adding:
                self.current_entity["@loot_group_id_str"] = "fg.loot.INVALID"
            else:
                del self.current_entity["@loot_group_id_str"]

        elif tag_name == "cyclable":
            if adding:
                self.current_entity["@cycle_facing_left_tile_id_str"] = "fg.tile.INVALID"
                self.current_entity["@cycle_facing_left_tile_offset"] = "0,0"
                self.current_entity["@cycle_facing_right_tile_id_str"] = "fg.tile.INVALID"
                self.current_entity["@cycle_facing_right_tile_offset"] = "0,0"
            else:
                del self.current_entity["@cycle_facing_left_tile_id_str"]
                del self.current_entity["@cycle_facing_left_tile_offset"]
                del self.current_entity["@cycle_facing_right_tile_id_str"]
                del self.current_entity["@cycle_facing_right_tile_offset"]

    def get_default_entity_dict(self):
        entity_dict = super().get_default_entity_dict()

        entity_dict["@name"] = "UNNAMED"
        entity_dict["@strength"] = "0"
        entity_dict["@light_reduction"] = "0"
        entity_dict["@light_emission"] = "0"
        entity_dict["@tags"] = ""
        entity_dict["@image_path"] = "res/images/tiles/"

        entity_dict["@item_id_str"] = "fg.item.INVALID"

        return entity_dict
