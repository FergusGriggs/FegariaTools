# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data


class LootTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Loot Tool"
        self.entity_type = "Loot"
        self.xml_group_name = "lootgroups"
        self.xml_type_name = "loot"

        self.set_xml_data_root()

        self.icon = commons.lt_icon_small
        self.accent_col = commons.loot_tool_col

        self.basic_properties_collapsed = False
        self.item_properties_collapsed = False
        self.item_list_collapsed = False
        self.coin_properties_collapsed = False

        self.items_collapsed = [True for _ in range(25)]

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.loot_data

    def export_tool_data(self):
        game_data.save_loot_data()

    def reload_tool_data(self):
        game_data.load_loot_data()

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id[:12] == "delete_item_":
                index = widget.widget_id.split("_")[-1]
                self.remove_item_from_list(int(index))
            elif widget.widget_id == "add_item":
                self.add_item_to_list()

        elif widget.type == WidgetType.TEXT_INPUT:
            if widget.widget_id == "loot_name":
                self.current_entity["@name"] = widget.text

            elif widget.widget_id == "loot_id_str":
                self.current_entity["@id_str"] = "fg.loot." + widget.text
                self.update_entity_list()
                self.reselect_current_entity()

            elif widget.widget_id == "loot_item_spawn_count_range":
                self.current_entity["@item_spawn_count_range"] = widget.text

            elif widget.widget_id == "loot_coin_spawn_range":
                self.current_entity["@coin_spawn_range"] = widget.text

            elif widget.widget_id[:23] == "loot_item_spawn_weight_":
                index = int(widget.widget_id.split("_")[-1])
                self.alter_item_list_property(index, 1, widget.text)
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id[:28] == "loot_item_spawn_depth_range_":
                index = int(widget.widget_id.split("_")[-1])
                self.alter_item_list_property(index, 2, widget.text)
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id[:28] == "loot_item_stack_count_range_":
                index = int(widget.widget_id.split("_")[-1])
                self.alter_item_list_property(index, 3, widget.text)
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id[:24] == "loot_item_slot_priority_":
                index = int(widget.widget_id.split("_")[-1])
                self.alter_item_list_property(index, 4, widget.text)
                self.load_property_page_for_entity(self.current_entity)

        elif widget.type == WidgetType.DROP_DOWN:
            if widget.widget_id[:17] == "loot_item_id_str_":
                index = int(widget.widget_id.split("_")[-1])
                self.alter_item_list_property(index, 0, widget.selected_string)

        elif widget.type == WidgetType.CHECKBOX:
            if widget.widget_id[:28] == "loot_item_once_per_instance_":
                index = int(widget.widget_id.split("_")[-1])
                self.alter_item_list_property(index, 5, str(int(widget.checked)))
                self.load_property_page_for_entity(self.current_entity)

        elif widget.type == WidgetType.BEGIN_COLLAPSE:
            if widget.widget_id[:10] == "loot_item_":
                index = int(widget.widget_id.split("_")[-1])
                self.items_collapsed[index] = widget.collapsed

        super().widget_altered(widget)

    def load_property_page_for_entity(self, entity):
        loot_properties = self.find_container("entity_properties")
        loot_properties.widgets.clear()

        # Basic properties
        loot_properties.add_widget(BeginCollapseWidget("loot_basic_properties", "Basic Properties", collapsed=self.basic_properties_collapsed))

        # Numerical Id
        loot_properties.add_widget(TextWidget("loot_id", "Id: " + entity["@id"]))

        # Name
        loot_properties.add_widget(TextWidget("loot_name_text", "Name:"))
        loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        loot_properties.add_widget(TextInputWidget("loot_name", entity["@name"], TextInputType.STRING))

        # String Id
        loot_properties.add_widget(TextWidget("loot_id_str_text", "Id Str:"))

        loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset - commons.font_20.size("fg.loot.")[0]))
        loot_properties.add_widget(TextWidget("loot_id_str_text_pre", "fg.loot.", commons.selected_border_col))
        loot_properties.add_widget(SameLineWidget(0))
        loot_properties.add_widget(TextInputWidget("loot_id_str", entity["@id_str"].split(".")[-1], TextInputType.STRING))

        # End basic properties
        loot_properties.add_widget(EndCollapseWidget())

        # Item properties
        loot_properties.add_widget(BeginCollapseWidget("loot_properties", "Item Properties", collapsed=self.item_properties_collapsed))

        # Item spawn count range
        loot_properties.add_widget(TextWidget("loot_item_spawn_count_range_text", "Item Spawn Count Range:"))
        loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        loot_properties.add_widget(TextInputWidget("loot_item_spawn_count_range", entity["@item_spawn_count_range"], TextInputType.INT_TUPLE))

        # Item list
        loot_properties.add_widget(BeginCollapseWidget("loot_list_of_items", "Item List", collapsed=self.item_list_collapsed))

        # Add item button
        loot_properties.add_widget(ButtonWidget("add_item", "Add Item"))

        item_list_str = entity["@item_list_data"]
        items = item_list_str.split("|")

        for item_index in range(len(items)):
            if items[item_index] == "":
                loot_properties.add_widget(TextWidget("no_items_text", "No Items To Show"))

            else:
                split_item_data = items[item_index].split(";")
                item_id_str = split_item_data[0]
                item_spawn_weight = split_item_data[1]
                item_spawn_depth_range = split_item_data[2]
                item_stack_count_range = split_item_data[3]
                item_slot_priority = split_item_data[4]
                once_per_instance = bool(int(split_item_data[5]))

                loot_properties.add_widget(BeginCollapseWidget("loot_item_" + str(item_index), item_id_str, collapsed=self.items_collapsed[item_index]))

                # Item id str
                loot_properties.add_widget(TextWidget("loot_item_id_str_text_" + str(item_index), "Item Id Str:"))
                loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
                loot_properties.add_widget(DropDownWidget("loot_item_id_str_" + str(item_index), game_data.item_id_strs, DropDownType.SELECT, initial_string=item_id_str))

                # Item Spawn Weight
                loot_properties.add_widget(TextWidget("loot_item_spawn_weight_text_" + str(item_index), "Item Spawn Weight:"))
                loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
                loot_properties.add_widget(TextInputWidget("loot_item_spawn_weight_" + str(item_index), item_spawn_weight, TextInputType.INT))

                # Item Depth Range
                loot_properties.add_widget(TextWidget("loot_item_spawn_depth_range_text_" + str(item_index), "Item Spawn Depth Range:"))
                loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
                loot_properties.add_widget(TextInputWidget("loot_item_spawn_depth_range_" + str(item_index), item_spawn_depth_range, TextInputType.INT_TUPLE))

                # Item stack count range
                loot_properties.add_widget(TextWidget("loot_item_stack_count_range_text_" + str(item_index), "Item Stack Count Range:"))
                loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
                loot_properties.add_widget(TextInputWidget("loot_item_stack_count_range_" + str(item_index), item_stack_count_range, TextInputType.INT_TUPLE))

                # Item slot priority
                loot_properties.add_widget(TextWidget("loot_item_slot_priority_text_" + str(item_index), "Item Slot Priority:"))
                loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
                loot_properties.add_widget(TextInputWidget("loot_item_slot_priority_" + str(item_index), item_slot_priority, TextInputType.INT, min_value=0, max_value=10))

                # Item once per instance
                loot_properties.add_widget(TextWidget("loot_item_once_per_instance_text_" + str(item_index), "Once Per Instance:"))
                loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
                loot_properties.add_widget(CheckboxWidget("loot_item_once_per_instance_" + str(item_index), checked=once_per_instance))

                loot_properties.add_widget(ButtonWidget("delete_item_" + str(item_index), "Remove Item"))

                loot_properties.add_widget(EndCollapseWidget())

        loot_properties.add_widget(EndCollapseWidget())

        # End item properties
        loot_properties.add_widget(EndCollapseWidget())

        # Coin properties
        loot_properties.add_widget(BeginCollapseWidget("loot_coin_properties", "Coin Properties", collapsed=self.coin_properties_collapsed))

        # Coin spawn range
        loot_properties.add_widget(TextWidget("loot_coin_spawn_range_text", "Coin Spawn Range:"))
        loot_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        loot_properties.add_widget(TextInputWidget("loot_coin_spawn_range", entity["@coin_spawn_range"], TextInputType.INT_TUPLE))

        loot_properties.add_widget(EndCollapseWidget())

        loot_properties.update(None)

    def get_default_item_list_entry(self):
        return "fg.item.dirt;100;0,0;1,1;0;0"

    def get_default_entity_dict(self):
        entity_dict = super().get_default_entity_dict()

        entity_dict["@name"] = "UNNAMED"
        entity_dict["@item_spawn_count_range"] = "0,0"
        entity_dict["@coin_spawn_range"] = "0,0"
        entity_dict["@item_list_data"] = self.get_default_item_list_entry()

        return entity_dict

    def remove_item_from_list(self, index):
        list_list_data_string = self.current_entity["@item_list_data"]
        items = list_list_data_string.split("|")
        items.pop(index)

        out_string = ""
        for item_index in range(len(items)):
            if item_index != 0:
                out_string += "|"
            out_string += items[item_index]

        self.current_entity["@item_list_data"] = out_string
        self.load_property_page_for_entity(self.current_entity)

    def add_item_to_list(self):
        if len(self.current_entity["@item_list_data"].split("|")) < 25:
            if len(self.current_entity["@item_list_data"]) > 0:
                self.current_entity["@item_list_data"] += "|"
            self.current_entity["@item_list_data"] += self.get_default_item_list_entry()

            self.load_property_page_for_entity(self.current_entity)

    def alter_item_list_property(self, item_index, property_index, new_str_value):
        list_list_data_string = self.current_entity["@item_list_data"]
        items = list_list_data_string.split("|")

        target_item = items[item_index]
        target_item_properties = target_item.split(";")

        target_item_properties[property_index] = new_str_value

        new_properties_string = ""
        for property_loop_index in range(len(target_item_properties)):
            if property_loop_index > 0:
                new_properties_string += ";"
            new_properties_string += target_item_properties[property_loop_index]

        items[item_index] = new_properties_string

        new_item_list_string = ""
        for item_loop_index in range(len(items)):
            if item_loop_index > 0:
                new_item_list_string += "|"
            new_item_list_string += items[item_loop_index]

        self.current_entity["@item_list_data"] = new_item_list_string

        self.load_property_page_for_entity(self.current_entity)

