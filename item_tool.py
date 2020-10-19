# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from ui_container import SplitType
from base_tool import Tool
from widget import *
import game_data

# Other imports
import collections


class ItemTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Item Tool"
        self.icon = commons.it_icon_small
        self.accent_col = commons.item_tool_col

        game_data.load_item_data()

        self.item_image_scale = 6.0
        self.item_image_colourkey_active = True

        self.basic_properties_collapsed = False

        self.tags_collapsed = True
        self.basic_tags_collapsed = False
        self.weapon_tags_collapsed = True
        self.tool_tags_collapsed = True
        self.block_tags_collapsed = True
        self.misc_tags_collapsed = True

        self.image_properties_collapsed = False
        self.block_properties_collapsed = True
        self.melee_properties_collapsed = True
        self.ranged_properties_collapsed = True
        self.magical_properties_collapsed = True
        self.projectile_properties_collapsed = True

        super().init()

        self.current_item = game_data.find_element_by_attribute(game_data.item_data["items"]["item"], "@id", "0")
        self.load_property_page_for_item(self.current_item)
        self.update_container("item_properties")
        self.find_container("item_list").find_widget("itemselector_0").selected = True

    def create_windows(self):
        super().create_windows()

        self.main_window.split_line_colour = self.light_accent_col

        window_main = self.find_container("window_main")
        window_main.draw_line = False

        window_main.add_split(SplitType.HORIZONTAL, 225, True, "item_list_section", "item_properties_section")

        item_list_section = self.find_container("item_list_section")
        item_list_section.add_split(SplitType.VERTICAL, 40, False, "item_list_title", "item_list_subsection")
        item_list_section.split_line_colour = self.dark_accent_col

        item_list_title = self.find_container("item_list_title")
        item_list_title.add_widget(TextWidget("item_list_title", "Item List", font=commons.font_30))
        item_list_title.background_colour = self.accent_col

        item_list_subsection = self.find_container("item_list_subsection")
        item_list_subsection.add_split(SplitType.VERTICAL, 35, False, "item_list_functions", "item_list")
        item_list_subsection.background_colour = (60, 60, 60)
        item_list_subsection.split_line_colour = (68, 68, 68)

        item_list_functions = self.find_container("item_list_functions")
        item_list_functions.background_colour = (60, 60, 60)
        item_list_functions.add_widget(ButtonWidget("add_new_item", "Add New"))
        item_list_functions.add_widget(SameLineWidget(10))
        item_list_functions.add_widget(ButtonWidget("delete_selected_item", "Delete"))
        item_list_functions.set_widget_align_type(WidgetAlignType.CENTRE)
        # Add drop-down widget when it exists to change the list sort type

        item_list = self.find_container("item_list")
        item_list.background_colour = (60, 60, 60)
        item_list.make_scrollable()

        item_properties_section = self.find_container("item_properties_section")
        item_properties_section.add_split(SplitType.VERTICAL, 40, False, "item_properties_title", "item_properties")
        item_properties_section.split_line_colour = self.dark_accent_col

        item_properties_title = self.find_container("item_properties_title")
        item_properties_title.add_widget(TextWidget("item_properties_title", "Item Properties", font=commons.font_30))
        item_properties_title.background_colour = self.accent_col

        item_properties = self.find_container("item_properties")
        item_properties.make_scrollable()

        self.update_item_list()

    def update_item_list(self):
        item_list = self.find_container("item_list")
        item_list.widgets.clear()

        for element in game_data.item_data["items"]["item"]:
            id_string = "%03d" % (int(element["@id"]),)
            item_list.add_widget(TextWidget(id_string, id_string, colour=(110, 110, 110)))
            item_list.add_widget(SameLineWidget(10))
            item_list.add_widget(TextWidget(element["@name"], element["@name"]))
            item_list.add_widget(LineSelectorWidget("itemselector_" + element["@id"]))

        item_list.update(None)

    def load_property_page_for_item(self, item):
        item_properties = self.find_container("item_properties")
        item_properties.widgets.clear()

        # Basic properties
        item_properties.add_widget(BeginCollapseWidget("item_basic_properties", "Basic Properties", collapsed=self.basic_properties_collapsed))

        # Numerical Id
        item_properties.add_widget(TextWidget("item_id", "Id: " + item["@id"]))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(ButtonWidget("move_item_up", "Move Up"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(ButtonWidget("move_item_down", "Move Down"))

        # Name
        item_properties.add_widget(TextWidget("item_name", "Name:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextInputWidget("item_name_input", item["@name"], TextInputType.STRING))

        # String Id
        item_properties.add_widget(TextWidget("item_id_str_text", "Id Str:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextInputWidget("item_id_str", item["@id_str"], TextInputType.STRING))

        # Description
        item_properties.add_widget(TextWidget("item_desc", "Description:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextInputWidget("item_desc_input", item["@desc"], TextInputType.STRING))

        item_properties.add_widget(EndCollapseWidget())

        # Item tags
        item_properties.add_widget(BeginCollapseWidget("item_tags", "Tags [" + item["@tags"] + "]", collapsed=self.tags_collapsed))

        item_properties.add_widget(TextWidget("item_tags_intro", "Select any tags that apply to the item (Additional menus may appear at the bottom)"))

        tags = methods.get_item_tags(item)

        item_properties.add_widget(BeginCollapseWidget("item_tags_basic", "Basic", collapsed=self.basic_tags_collapsed))

        item_properties.add_widget(CheckboxWidget("itemtag_block", checked=("block" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("block_tag_text", "block"))

        item_properties.add_widget(CheckboxWidget("itemtag_material", checked=("material" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("material_tag_text", "material"))

        item_properties.add_widget(CheckboxWidget("itemtag_weapon", checked=("weapon" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("weapon_tag_text", "weapon"))

        item_properties.add_widget(CheckboxWidget("itemtag_tool", checked=("tool" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("tool_tag_text", "tool"))

        item_properties.add_widget(EndCollapseWidget())

        item_properties.add_widget(BeginCollapseWidget("item_tags_weapon", "Weapon", collapsed=self.weapon_tags_collapsed))

        item_properties.add_widget(CheckboxWidget("itemtag_melee", checked=("melee" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("melee_tag_text", "melee"))

        item_properties.add_widget(CheckboxWidget("itemtag_ranged", checked=("ranged" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("ranged_tag_text", "ranged"))

        item_properties.add_widget(CheckboxWidget("itemtag_magical", checked=("magical" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("magical_tag_text", "magical"))

        item_properties.add_widget(CheckboxWidget("itemtag_projectile", checked=("projectile" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("projectile_tag_text", "projectile"))
        
        item_properties.add_widget(EndCollapseWidget())

        item_properties.add_widget(BeginCollapseWidget("item_tags_tool", "Tool", collapsed=self.tool_tags_collapsed))

        item_properties.add_widget(CheckboxWidget("itemtag_pickaxe", checked=("pickaxe" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("pickaxe_tag_text", "pickaxe"))

        item_properties.add_widget(CheckboxWidget("itemtag_axe", checked=("axe" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("axe_tag_text", "axe"))

        item_properties.add_widget(CheckboxWidget("itemtag_hammer", checked=("hammer" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("hammer_tag_text", "hammer"))

        item_properties.add_widget(CheckboxWidget("itemtag_grapple", checked=("grapple" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("grapple_tag_text", "grapple"))
        
        item_properties.add_widget(EndCollapseWidget())

        item_properties.add_widget(BeginCollapseWidget("item_tags_block", "Block", collapsed=self.block_tags_collapsed))

        item_properties.add_widget(CheckboxWidget("itemtag_nowall", checked=("nowall" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("nowall_tag_text", "nowall"))

        item_properties.add_widget(CheckboxWidget("itemtag_multitile", checked=("multitile" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("multitile_tag_text", "multitile"))

        item_properties.add_widget(CheckboxWidget("itemtag_interactable", checked=("interactable" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("interactable_tag_text", "interactable"))
        
        item_properties.add_widget(CheckboxWidget("itemtag_door", checked=("door" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("door_tag_text", "door"))

        item_properties.add_widget(CheckboxWidget("itemtag_chest", checked=("chest" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("chest_tag_text", "chest"))

        item_properties.add_widget(EndCollapseWidget())

        item_properties.add_widget(BeginCollapseWidget("item_tags_misc", "Misc", collapsed=self.misc_tags_collapsed))

        item_properties.add_widget(CheckboxWidget("itemtag_coin", checked=("coin" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("coin_tag_text", "coin"))

        item_properties.add_widget(EndCollapseWidget())

        item_properties.add_widget(TextWidget("item_tags_text", "Item Tags: [" + item["@tags"] + "]"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(ButtonWidget("clear_item_tags", "Clear Tags"))

        item_properties.add_widget(EndCollapseWidget())

        # Image properties
        item_properties.add_widget(BeginCollapseWidget("item_image_properties", "Image Properties", collapsed=self.image_properties_collapsed))

        item_properties.add_widget(TextWidget("image_filepath", "Image Filepath:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextInputWidget("image_file_path_input", item["@image_filepath"], TextInputType.STRING))
        item_properties.add_widget(TextWidget("image_text", "Item Image:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(ImageWidget("item_image", methods.safe_load_image(item["@image_filepath"]), image_scale=self.item_image_scale))
        if not self.item_image_colourkey_active:
            item_properties.find_widget("item_image").toggle_colourkey()

        item_properties.add_widget(TextWidget("item_image_load_fail", "Item image failed to load", colour=(255, 128, 128)))
        item_image_widget = item_properties.find_widget("item_image")
        if item_image_widget.loaded:
            item_properties.find_widget("item_image_load_fail").hide()
        else:
            item_properties.find_widget("item_image_load_fail").show()

        item_properties.add_widget(TextWidget("item_image_back_checkbox_text", "Colourkey Active?"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(CheckboxWidget("item_image_back_checkbox"))
        item_properties.find_widget("item_image_back_checkbox").checked = self.item_image_colourkey_active

        item_properties.add_widget(TextWidget("image_scale", "Image Scale:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextInputWidget("image_scale_input", str(self.item_image_scale), TextInputType.FLOAT, min_value=0.0, max_value=16.0))

        item_properties.add_widget(EndCollapseWidget())

        item_tags = methods.get_item_tags(self.current_item)

        # Block Properties
        if "block" in item_tags:
            item_properties.add_widget(BeginCollapseWidget("item_block_properties", "Block Properties", collapsed=self.block_properties_collapsed))

            item_properties.add_widget(TextWidget("item_tile_id_text", "Tile Id:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("item_tile_id", "0", TextInputType.INT))

            item_properties.add_widget(EndCollapseWidget())

        # Melee Properties
        if "melee" in item_tags:
            item_properties.add_widget(BeginCollapseWidget("item_melee_properties", "Melee Properties", collapsed=self.melee_properties_collapsed))

            item_properties.add_widget(TextWidget("item_attack_speed_text", "Attack Speed:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("item_attack_speed", "0", TextInputType.INT))

            item_properties.add_widget(TextWidget("item_attack_damage_text", "Attack Damage:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("item_attack_damage", "0", TextInputType.INT))

            item_properties.add_widget(TextWidget("item_knockback_text", "Knockback:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("item_knockback", "0", TextInputType.INT))

            item_properties.add_widget(EndCollapseWidget())

        # Ranged Properties
        if "ranged" in item_tags:
            item_properties.add_widget(BeginCollapseWidget("item_ranged_properties", "Ranged Properties", collapsed=self.ranged_properties_collapsed))

            item_properties.add_widget(TextWidget("item_ammo_type_text", "Ammo Type:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("item_ammo_type", "", TextInputType.STRING))

            item_properties.add_widget(TextWidget("item_projectile_speed_text", "Projectile Speed:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("item_projectile_speed", "", TextInputType.FLOAT))

            item_properties.add_widget(EndCollapseWidget())

        # Magical Properties
        if "magical" in item_tags:
            item_properties.add_widget(BeginCollapseWidget("item_magical_properties", "Magical Properties", collapsed=self.magical_properties_collapsed))

            item_properties.add_widget(TextWidget("item_mana_cost_text", "Mana Cost:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("item_mana_cost", "0", TextInputType.INT))

            item_properties.add_widget(EndCollapseWidget())

        # Projectile Properties
        if "projectile" in item_tags:
            item_properties.add_widget(BeginCollapseWidget("item_projectile_properties", "Projectile Properties", collapsed=self.projectile_properties_collapsed))

            item_properties.add_widget(TextWidget("projectile_type_text", "Projectile Type:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("projectile_type", "", TextInputType.STRING))

            item_properties.add_widget(TextWidget("projectile_damage_text", "Projectile Damage:"))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextInputWidget("projectile_damage", "0", TextInputType.INT))

            item_properties.add_widget(EndCollapseWidget())

        item_properties.update(None)

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "reload_item_data":
                game_data.load_item_data()
                self.update_item_list()

            elif widget.widget_id == "export_data":
                game_data.save_item_data()

            elif widget.widget_id == "load_data":
                game_data.load_item_data()
                self.update_item_list()

                self.reselect_current_item()

            elif widget.widget_id == "add_new_item":
                index_to_add_at = int(self.current_item["@id"]) + 1
                item_dict = collections.OrderedDict()
                item_dict["@id"] = str(index_to_add_at)
                item_dict["@name"] = "UNNAMED"
                item_dict["@desc"] = ""
                item_dict["@tags"] = ""
                item_dict["@image_filepath"] = "res/images/items/"
                game_data.item_data["items"]["item"].insert(index_to_add_at, item_dict)

                game_data.reassign_element_ids(game_data.item_data["items"]["item"])

                self.update_item_list()
                self.reselect_current_item()

            elif widget.widget_id == "move_item_up":
                if int(self.current_item["@id"]) > 0:
                    game_data.item_data["items"]["item"].remove(self.current_item)

                    self.current_item["@id"] = str(int(self.current_item["@id"]) - 1)

                    game_data.item_data["items"]["item"].insert(int(self.current_item["@id"]), self.current_item)

                    game_data.reassign_element_ids(game_data.item_data["items"]["item"])
                    self.update_item_list()
                    self.reselect_current_item()

            elif widget.widget_id == "move_item_down":
                if int(self.current_item["@id"]) < len(game_data.item_data["items"]["item"]):
                    game_data.item_data["items"]["item"].remove(self.current_item)

                    self.current_item["@id"] = str(int(self.current_item["@id"]) + 1)

                    game_data.item_data["items"]["item"].insert(int(self.current_item["@id"]), self.current_item)

                    game_data.reassign_element_ids(game_data.item_data["items"]["item"])
                    self.update_item_list()
                    self.reselect_current_item()

            elif widget.widget_id == "delete_selected_item":
                if len(game_data.item_data["items"]["item"]) > 1:
                    game_data.remove_element_by_attribute(game_data.item_data["items"]["item"], "@id", self.current_item["@id"])
                    game_data.reassign_element_ids(game_data.item_data["items"]["item"])

                    self.update_item_list()

                    self.reselect_current_item()

            elif widget.widget_id == "clear_item_tags":
                tags = methods.get_item_tags(self.current_item)
                tags.clear()
                self.current_item["@tags"] = methods.make_comma_seperated_string(tags)
                self.load_property_page_for_item(self.current_item)

        elif widget.type == WidgetType.LINE_SELECTOR:
            split_id = widget.widget_id.split("_")
            if len(split_id) > 0 and split_id[0] == "itemselector":
                self.find_container("item_list").deselect_all()
                widget.selected = True
                self.current_item = game_data.find_element_by_attribute(game_data.item_data["items"]["item"], "@id", split_id[1])
                self.load_property_page_for_item(self.current_item)

        elif widget.type == WidgetType.TEXT_INPUT:
            if widget.widget_id == "item_name_input":
                self.current_item["@name"] = widget.text
                self.update_item_list()
                self.reselect_current_item()

            elif widget.widget_id == "item_desc_input":
                self.current_item["@desc"] = widget.text

            elif widget.widget_id == "item_tags_input":
                self.current_item["@tags"] = widget.text

            elif widget.widget_id == "image_file_path_input":
                self.current_item["@image_filepath"] = widget.text

                item_image_widget = self.find_container("item_properties").find_widget("item_image")
                image_scale = float(self.find_container("item_properties").find_widget("image_scale_input").text)
                item_image_widget.set_image(methods.safe_load_image(widget.text), image_scale=image_scale)
                if item_image_widget.loaded:
                    self.find_container("item_properties").find_widget("item_image_load_fail").hide()
                else:
                    self.find_container("item_properties").find_widget("item_image_load_fail").show()
                self.update_container("item_properties")

                self.find_container("item_properties").find_widget("item_image_back_checkbox").checked = True

            elif widget.widget_id == "image_scale_input":
                item_properties_container = self.find_container("item_properties")
                self.item_image_scale = float(widget.text)
                item_properties_container.find_widget("item_image").update_image_scale(self.item_image_scale)
                item_properties_container.update(None)

        elif widget.type == WidgetType.CHECKBOX:
            split_id = widget.widget_id.split("_")
            if len(split_id) > 0 and split_id[0] == "itemtag":
                self.modify_item_tags(split_id[1], widget.checked)
                self.load_property_page_for_item(self.current_item)
            else:
                if widget.widget_id == "item_image_back_checkbox":
                    item_properties = self.find_container("item_properties")
                    item_properties.find_widget("item_image").toggle_colourkey()
                    item_properties.render_widget_surface()
                    self.item_image_colourkey_active = not self.item_image_colourkey_active

        elif widget.type == WidgetType.BEGIN_COLLAPSE:
            if widget.widget_id == "item_basic_properties":
                self.basic_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags":
                self.tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_basic":
                self.basic_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_weapon":
                self.weapon_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_tool":
                self.tool_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_block":
                self.block_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_misc":
                self.misc_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_image_properties":
                self.image_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_block_properties":
                self.block_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_melee_properties":
                self.melee_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_magical_properties":
                self.magical_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_projectile_properties":
                self.projectile_properties_collapsed = widget.collapsed

        super().widget_altered(widget)

    def reselect_current_item(self):
        id_to_select = min(len(game_data.item_data["items"]["item"]) - 1, int(self.current_item["@id"]))
        self.current_item = game_data.item_data["items"]["item"][id_to_select]
        self.find_container("item_list").find_widget("itemselector_" + str(id_to_select)).selected = True
        self.load_property_page_for_item(self.current_item)

    def quit(self):
        super().quit()

        game_data.unload_item_data()

    def modify_item_tags(self, tag_name, adding):
        tags = methods.get_item_tags(self.current_item)
        if adding:
            if tag_name not in tags:
                tags.append(tag_name)
                self.current_item["@tags"] = methods.make_comma_seperated_string(tags)
        else:
            tags.remove(tag_name)
            self.current_item["@tags"] = methods.make_comma_seperated_string(tags)
