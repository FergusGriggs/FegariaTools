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


class ItemTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Item Tool"
        self.entity_type = "Item"
        self.xml_data_root = game_data.item_data
        self.xml_group_name = "items"
        self.xml_type_name = "item"

        self.icon = commons.it_icon_small
        self.accent_col = commons.item_tool_col

        self.item_list_sort_type = SortType.BY_ID

        self.item_image_scale = 3.0
        self.item_image_colourkey_active = True

        self.basic_properties_collapsed = False
        self.misc_properties_collapsed = True

        self.tags_collapsed = True
        self.basic_tags_collapsed = False
        self.weapon_tags_collapsed = True
        self.tool_tags_collapsed = True
        self.misc_tags_collapsed = True

        self.prefix_properties_collapsed = True
        self.image_properties_collapsed = False
        self.block_properties_collapsed = True
        self.weapon_properties_collapsed = True
        self.ranged_properties_collapsed = True
        self.magical_properties_collapsed = True
        self.ammo_properties_collapsed = True
        self.pickaxe_properties_collapsed = True
        self.axe_properties_collapsed = True
        self.hammer_properties_collapsed = True
        self.grapple_properties_collapsed = True

        super().init()

    def load_property_page_for_entity(self, entity):
        item_properties = self.find_container("entity_properties")
        item_properties.widgets.clear()

        # Basic properties
        item_properties.add_widget(BeginCollapseWidget("item_basic_properties", "Basic Properties", collapsed=self.basic_properties_collapsed))

        # Numerical Id
        item_properties.add_widget(TextWidget("item_id", "Id: " + entity["@id"]))

        # Name
        item_properties.add_widget(TextWidget("item_name", "Name:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(TextInputWidget("item_name_input", entity["@name"], TextInputType.STRING))

        # String Id
        item_properties.add_widget(TextWidget("item_id_str_text", "Id Str:"))
        item_properties.add_widget(SameLineFillToLineWidget(170))
        item_properties.add_widget(TextWidget("item_id_str_text", "fg.item.", commons.selected_border_col))
        item_properties.add_widget(SameLineWidget(0))
        item_properties.add_widget(TextInputWidget("item_id_str", entity["@id_str"][8:], TextInputType.STRING))

        # Description
        item_properties.add_widget(TextWidget("item_desc", "Description:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(TextInputWidget("item_desc_input", entity["@desc"], TextInputType.STRING))

        item_properties.add_widget(EndCollapseWidget())

        # Misc properties
        item_properties.add_widget(BeginCollapseWidget("item_misc_properties", "Misc Properties", collapsed=self.misc_properties_collapsed))

        # Tier
        item_properties.add_widget(TextWidget("item_tier_text", "Tier:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(TextInputWidget("item_tier", entity["@tier"], TextInputType.INT, min_value=0, max_value=10))

        # Max Stack
        item_properties.add_widget(TextWidget("item_max_stack_text", "Max Stack:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(TextInputWidget("item_max_stack", entity["@max_stack"], TextInputType.INT, min_value=1, max_value=999))

        # Buy Price
        item_properties.add_widget(TextWidget("item_buy_price_text", "Buy Price:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(TextInputWidget("item_buy_price", entity["@buy_price"], TextInputType.INT, min_value=0))

        # Sell Price
        item_properties.add_widget(TextWidget("item_sell_price_text", "Sell Price:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(TextInputWidget("item_sell_price", entity["@sell_price"], TextInputType.INT, min_value=0))

        item_properties.add_widget(EndCollapseWidget())

        # Item tags
        item_properties.add_widget(BeginCollapseWidget("item_tags", "Tags [" + entity["@tags"] + "]", collapsed=self.tags_collapsed))

        item_properties.add_widget(TextWidget("item_tags_intro", "Select any tags that apply to the item (Additional menus may appear at the bottom)"))

        tags = methods.get_tags(entity)

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

        item_properties.add_widget(CheckboxWidget("itemtag_ammo", checked=("ammo" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("ammo_tag_text", "ammo"))
        
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

        item_properties.add_widget(BeginCollapseWidget("item_tags_misc", "Misc", collapsed=self.misc_tags_collapsed))

        item_properties.add_widget(CheckboxWidget("itemtag_coin", checked=("coin" in tags)))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextWidget("coin_tag_text", "coin"))

        item_properties.add_widget(EndCollapseWidget())

        item_properties.add_widget(TextWidget("item_tags_text", "Item Tags: [" + entity["@tags"] + "]"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(ButtonWidget("clear_item_tags", "Clear Tags"))

        item_properties.add_widget(EndCollapseWidget())

        # Prefixes
        if "weapon" in tags:
            prefixes = methods.get_item_prefixes(entity)

            item_properties.add_widget(BeginCollapseWidget("prefix_properties", "Prefix Groups [" + entity["@prefixes"] + "]", collapsed=self.prefix_properties_collapsed))

            item_properties.add_widget(CheckboxWidget("itemprefix_universal", checked=("universal" in prefixes)))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextWidget("universal_prefix_text", "universal"))

            item_properties.add_widget(CheckboxWidget("itemprefix_common", checked=("common" in prefixes)))
            item_properties.add_widget(SameLineWidget(10))
            item_properties.add_widget(TextWidget("common_prefix_text", "common"))

            if "melee" in tags:
                item_properties.add_widget(CheckboxWidget("itemprefix_melee", checked=("melee" in prefixes)))
                item_properties.add_widget(SameLineWidget(10))
                item_properties.add_widget(TextWidget("melee_prefix_text", "melee"))

            if "ranged" in tags:
                item_properties.add_widget(CheckboxWidget("itemprefix_ranged", checked=("ranged" in prefixes)))
                item_properties.add_widget(SameLineWidget(10))
                item_properties.add_widget(TextWidget("ranged_prefix_text", "ranged"))

            if "magical" in tags:
                item_properties.add_widget(CheckboxWidget("itemprefix_magical", checked=("magical" in prefixes)))
                item_properties.add_widget(SameLineWidget(10))
                item_properties.add_widget(TextWidget("magical_prefix_text", "magical"))

            item_properties.add_widget(EndCollapseWidget())

        # Image properties
        item_properties.add_widget(BeginCollapseWidget("item_image_properties", "Image Properties", collapsed=self.image_properties_collapsed))

        item_properties.add_widget(TextWidget("image_path", "Image Path:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(TextInputWidget("image_file_path_input", entity["@image_path"], TextInputType.STRING))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(ButtonWidget("open_item_image_folder", "Open Folder"))

        item_properties.add_widget(TextWidget("image_text", "Item Image:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(ImageWidget("item_image", methods.safe_load_image(entity["@image_path"]), image_scale=self.item_image_scale))
        if not self.item_image_colourkey_active:
            item_properties.find_widget("item_image").toggle_colourkey()

        item_properties.add_widget(TextWidget("item_image_load_fail", "Item image failed to load", colour=(255, 128, 128)))
        item_image_widget = item_properties.find_widget("item_image")
        if item_image_widget.loaded:
            item_properties.find_widget("item_image_load_fail").hide()
        else:
            item_properties.find_widget("item_image_load_fail").show()

        item_properties.add_widget(TextWidget("item_image_back_checkbox_text", "Colourkey Active?"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(CheckboxWidget("item_image_back_checkbox"))
        item_properties.find_widget("item_image_back_checkbox").checked = self.item_image_colourkey_active

        item_properties.add_widget(TextWidget("image_scale", "Image Scale:"))
        item_properties.add_widget(SameLineFillToLineWidget(250))
        item_properties.add_widget(TextInputWidget("image_scale_input", str(self.item_image_scale), TextInputType.FLOAT, min_value=0.0, max_value=16.0))

        item_properties.add_widget(EndCollapseWidget())

        # Block Properties
        if "block" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_block_properties", "Block Properties", collapsed=self.block_properties_collapsed))

            item_properties.add_widget(TextWidget("item_tile_id_str_text", "Tile Id Str:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(DropDownWidget("item_tile_id_str", game_data.tile_id_strs, DropDownType.SELECT, initial_string=entity["@tile_id_str"]))

            item_properties.add_widget(EndCollapseWidget())

        # Melee Properties
        if "weapon" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_weapon_properties", "Weapon Properties", collapsed=self.weapon_properties_collapsed))

            item_properties.add_widget(TextWidget("item_attack_speed_text", "Attack Speed:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_attack_speed", entity["@attack_speed"], TextInputType.INT))

            item_properties.add_widget(TextWidget("item_attack_damage_text", "Attack Damage:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_attack_damage", entity["@attack_damage"], TextInputType.INT))

            item_properties.add_widget(TextWidget("item_knockback_text", "Knockback:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_knockback", entity["@knockback"], TextInputType.INT))

            item_properties.add_widget(TextWidget("item_crit_chance_text", "Crit Chance:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_crit_chance", entity["@crit_chance"], TextInputType.FLOAT))

            item_properties.add_widget(TextWidget("item_hold_offset_text", "Hold Offset:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_hold_offset", entity["@hold_offset"], TextInputType.INT))

            item_properties.add_widget(TextWidget("item_world_override_image_path_text", "World Override Image path:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_world_override_image_path", entity["@world_override_image_path"], TextInputType.STRING))

            item_properties.add_widget(TextWidget("item_world_override_image_text", "World Override Image:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(ImageWidget("item_world_override_image", methods.safe_load_image(entity["@world_override_image_path"]), image_scale=self.item_image_scale))
            if not self.item_image_colourkey_active:
                item_properties.find_widget("item_world_override_image").toggle_colourkey()

            item_properties.add_widget(EndCollapseWidget())

        # Ranged Properties
        if "ranged" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_ranged_properties", "Ranged Properties", collapsed=self.ranged_properties_collapsed))

            item_properties.add_widget(TextWidget("item_ranged_projectile_id_str_text", "Proj Id Str:"))
            item_properties.add_widget(SameLineFillToLineWidget(170))
            item_properties.add_widget(TextWidget("item_ranged_projectile_id_str_pre", "fg.proj.", commons.selected_border_col))
            item_properties.add_widget(SameLineWidget(0))
            item_properties.add_widget(TextInputWidget("item_ranged_projectile_id_str", entity["@ranged_projectile_id_str"], TextInputType.STRING))

            item_properties.add_widget(TextWidget("item_ranged_ammo_type_text", "Ammo Type:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_ranged_ammo_type", entity["@ranged_ammo_type"], TextInputType.STRING))

            item_properties.add_widget(TextWidget("item_ranged_projectile_speed_text", "Launch Speed:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_ranged_projectile_speed", entity["@ranged_projectile_speed"], TextInputType.FLOAT))

            item_properties.add_widget(TextWidget("item_ranged_accuracy_text", "Accuracy:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_ranged_accuracy", entity["@ranged_accuracy"], TextInputType.STRING))

            item_properties.add_widget(TextWidget("item_num_projectiles_text", "Num Projectiles:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_num_projectiles", entity["@ranged_num_projectiles"], TextInputType.INT))

            item_properties.add_widget(EndCollapseWidget())

        # Magical Properties
        if "magical" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_magical_properties", "Magical Properties", collapsed=self.magical_properties_collapsed))

            item_properties.add_widget(TextWidget("item_mana_cost_text", "Mana Cost:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_mana_cost", entity["@mana_cost"], TextInputType.INT))

            item_properties.add_widget(EndCollapseWidget())

        # Projectile Properties
        if "ammo" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_ammo_properties", "Ammo Properties", collapsed=self.ammo_properties_collapsed))

            item_properties.add_widget(TextWidget("item_ammo_type_text", "Ammo Type:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_ammo_type", entity["@ammo_type"], TextInputType.STRING))

            item_properties.add_widget(TextWidget("item_ammo_damage_text", "Ammo Damage:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_ammo_damage", entity["@ammo_damage"], TextInputType.FLOAT))

            item_properties.add_widget(TextWidget("item_ammo_drag_text", "Ammo Drag:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_ammo_drag", entity["@ammo_drag"], TextInputType.FLOAT))

            item_properties.add_widget(TextWidget("item_ammo_gravity_mod_text", "Ammo Gravity Mod:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_ammo_gravity_mod", entity["@ammo_gravity_mod"], TextInputType.FLOAT))

            item_properties.add_widget(TextWidget("item_ammo_knockback_text", "Ammo Knockback:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_ammo_knockback", entity["@ammo_knockback"], TextInputType.FLOAT))

            item_properties.add_widget(EndCollapseWidget())

        # Pickaxe Properties
        if "pickaxe" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_pickaxe_properties", "Pickaxe Properties", collapsed=self.pickaxe_properties_collapsed))

            item_properties.add_widget(TextWidget("item_pickaxe_power_text", "Pickaxe Power:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_pickaxe_power", entity["@pickaxe_power"], TextInputType.FLOAT))

            item_properties.add_widget(EndCollapseWidget())

        # Axe Properties
        if "axe" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_axe_properties", "Axe Properties", collapsed=self.axe_properties_collapsed))

            item_properties.add_widget(TextWidget("item_axe_power_text", "Axe Power:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_axe_power", entity["@axe_power"], TextInputType.FLOAT))

            item_properties.add_widget(EndCollapseWidget())

        # Axe Properties
        if "hammer" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_hammer_properties", "Hammer Properties", collapsed=self.hammer_properties_collapsed))

            item_properties.add_widget(TextWidget("item_hammer_power_text", "Hammer Power:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_hammer_power",  entity["@hammer_power"], TextInputType.FLOAT))

            item_properties.add_widget(EndCollapseWidget())

        # Grapple Properties
        if "grapple" in tags:
            item_properties.add_widget(BeginCollapseWidget("item_grapple_properties", "Grapple Properties", collapsed=self.grapple_properties_collapsed))

            item_properties.add_widget(TextWidget("item_grapple_speed_text", "Grapple Speed:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_grapple_speed",  entity["@grapple_speed"], TextInputType.FLOAT))

            item_properties.add_widget(TextWidget("item_grapple_chain_length_text", "Chain Length:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_grapple_chain_length",  entity["@grapple_chain_length"], TextInputType.FLOAT))

            item_properties.add_widget(TextWidget("item_grapple_max_chains_text", "Max Chains:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_grapple_max_chains", entity["@grapple_max_chains"], TextInputType.INT))

            item_properties.add_widget(TextWidget("item_grapple_chain_image_path_text", "Chain Image Path:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_grapple_chain_image_path",  entity["@grapple_chain_image_path"], TextInputType.STRING))

            item_properties.add_widget(TextWidget("item_grapple_chain_image_text", "Chain Image:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(ImageWidget("item_grapple_chain_image", methods.safe_load_image(entity["@grapple_chain_image_path"]), image_scale=2.0))
            if not self.item_image_colourkey_active:
                item_properties.find_widget("item_grapple_chain_image").toggle_colourkey()

            item_properties.add_widget(TextWidget("item_grapple_claw_image_path_text", "Claw Image Path:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget(TextInputWidget("item_grapple_claw_image_path",  entity["@grapple_claw_image_path"], TextInputType.STRING))

            item_properties.add_widget(TextWidget("item_grapple_claw_image_text", "Claw Image:"))
            item_properties.add_widget(SameLineFillToLineWidget(250))
            item_properties.add_widget( ImageWidget("item_grapple_claw_image", methods.safe_load_image(entity["@grapple_claw_image_path"]), image_scale=2.0))
            if not self.item_image_colourkey_active:
                item_properties.find_widget("item_grapple_claw_image").toggle_colourkey()

            item_properties.add_widget(EndCollapseWidget())

        item_properties.update(None)

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "export_data":
                game_data.save_item_data()

            elif widget.widget_id == "load_data":
                game_data.load_item_data()
                self.update_entity_list()

                self.reselect_current_entity()
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id == "clear_item_tags":
                tags = methods.get_tags(self.current_entity)
                tags.clear()
                self.current_entity["@tags"] = methods.make_comma_seperated_string(tags)
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id == "open_item_image_folder":
                dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\res\\images\\items\\"
                subprocess.Popen(f'explorer "' + dir_path + '"')

        elif widget.type == WidgetType.TEXT_INPUT:
            if widget.widget_id == "item_name_input":
                self.current_entity["@name"] = widget.text

            elif widget.widget_id == "item_id_str":
                self.current_entity["@id_str"] = "fg.item." + widget.text
                self.update_entity_list()
                self.reselect_current_entity()

            elif widget.widget_id == "item_desc_input":
                self.current_entity["@desc"] = widget.text

            elif widget.widget_id == "item_tier":
                self.current_entity["@tier"] = widget.text

            elif widget.widget_id == "item_max_stack":
                self.current_entity["@max_stack"] = widget.text

            elif widget.widget_id == "item_buy_price":
                self.current_entity["@buy_price"] = widget.text

            elif widget.widget_id == "item_sell_price":
                self.current_entity["@sell_price"] = widget.text

            elif widget.widget_id == "image_file_path_input":
                self.current_entity["@image_path"] = widget.text

                item_image_widget = self.find_container("item_properties").find_widget("item_image")
                image_scale = float(self.find_container("item_properties").find_widget("image_scale_input").text)
                item_image_widget.set_image(methods.safe_load_image(widget.text), image_scale=image_scale, update_container=False)
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

            elif widget.widget_id == "item_attack_speed":
                self.current_entity["@attack_speed"] = widget.text

            elif widget.widget_id == "item_attack_damage":
                self.current_entity["@attack_damage"] = widget.text

            elif widget.widget_id == "item_knockback":
                self.current_entity["@knockback"] = widget.text

            elif widget.widget_id == "item_crit_chance":
                self.current_entity["@crit_chance"] = widget.text

            elif widget.widget_id == "item_hold_offset":
                self.current_entity["@hold_offset"] = widget.text

            elif widget.widget_id == "item_world_override_image_path":
                self.current_entity["@world_override_image_path"] = widget.text

            elif widget.widget_id == "item_ranged_projectile_id_str":
                self.current_entity["@ranged_projectile_id_str"] = widget.text

            elif widget.widget_id == "item_ranged_ammo_type":
                self.current_entity["@ranged_ammo_type"] = widget.text

            elif widget.widget_id == "item_ranged_projectile_speed":
                self.current_entity["@ranged_projectile_speed"] = widget.text

            elif widget.widget_id == "item_ranged_accuracy":
                self.current_entity["@ranged_accuracy"] = widget.text

            elif widget.widget_id == "item_mana_cost":
                self.current_entity["@mana_cost"] = widget.text

            elif widget.widget_id == "item_ammo_type":
                self.current_entity["@ammo_type"] = widget.text

            elif widget.widget_id == "item_ammo_damage":
                self.current_entity["@ammo_damage"] = widget.text

            elif widget.widget_id == "item_ammo_drag":
                self.current_entity["@ammo_drag"] = widget.text

            elif widget.widget_id == "item_ammo_gravity_mod":
                self.current_entity["@ammo_gravity_mod"] = widget.text

            elif widget.widget_id == "item_ammo_knockback":
                self.current_entity["@ammo_knockback"] = widget.text

            elif widget.widget_id == "item_pickaxe_power":
                self.current_entity["@pickaxe_power"] = widget.text

            elif widget.widget_id == "item_axe_power":
                self.current_entity["@axe_power"] = widget.text

            elif widget.widget_id == "item_item_hammer_power":
                self.current_entity["@item_hammer_power"] = widget.text

            elif widget.widget_id == "item_grapple_speed":
                self.current_entity["@grapple_speed"] = widget.text

            elif widget.widget_id == "item_grapple_chain_length":
                self.current_entity["@grapple_chain_length"] = widget.text

            elif widget.widget_id == "item_grapple_max_chains":
                self.current_entity["@grapple_max_chains"] = widget.text

            elif widget.widget_id == "item_grapple_chain_image_path":
                self.current_entity["@grapple_chain_image_path"] = widget.text

            elif widget.widget_id == "item_grapple_claw_image_path":
                self.current_entity["@grapple_claw_image_path"] = widget.text

        elif widget.type == WidgetType.DROP_DOWN:
            if widget.widget_id == "item_tile_id_str":
                self.current_entity["@tile_id_str"] = widget.selected_string

        elif widget.type == WidgetType.CHECKBOX:
            split_id = widget.widget_id.split("_")
            if len(split_id) > 0:
                if split_id[0] == "itemtag":
                    self.modify_item_tags(split_id[1], widget.checked)
                    self.load_property_page_for_entity(self.current_entity)
                elif split_id[0] == "itemprefix":
                    self.modify_item_prefixes(split_id[1], widget.checked)
                    self.load_property_page_for_entity(self.current_entity)

            if widget.widget_id == "item_image_back_checkbox":
                item_properties = self.find_container("item_properties")
                item_properties.find_widget("item_image").toggle_colourkey()
                item_properties.render_widget_surface()
                self.item_image_colourkey_active = not self.item_image_colourkey_active

        elif widget.type == WidgetType.BEGIN_COLLAPSE:
            if widget.widget_id == "item_basic_properties":
                self.basic_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_misc_properties":
                self.misc_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags":
                self.tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_basic":
                self.basic_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_weapon":
                self.weapon_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_tool":
                self.tool_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_tags_misc":
                self.misc_tags_collapsed = widget.collapsed
            elif widget.widget_id == "item_image_properties":
                self.image_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_block_properties":
                self.block_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_weapon_properties":
                self.weapon_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_ranged_properties":
                self.ranged_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_magical_properties":
                self.magical_properties_collapsed = widget.collapsed
            elif widget.widget_id == "item_ammo_properties":
                self.ammo_properties_collapsed = widget.collapsed
            elif widget.widget_id == "prefix_properties":
                self.prefix_properties_collapsed = widget.collapsed

        super().widget_altered(widget)

    def quit(self):
        super().quit()

    def modify_item_prefixes(self, prefix_name, adding):
        prefixes = methods.get_item_prefixes(self.current_entity)
        if adding:
            if prefix_name not in prefixes:
                prefixes.append(prefix_name)
                self.current_entity["@prefixes"] = methods.make_comma_seperated_string(prefixes)
        else:
            prefixes.remove(prefix_name)
            self.current_entity["@prefixes"] = methods.make_comma_seperated_string(prefixes)

    def modify_item_tags(self, tag_name, adding):
        tags = methods.get_tags(self.current_entity)
        if adding:
            if tag_name not in tags:
                tags.append(tag_name)
                self.current_entity["@tags"] = methods.make_comma_seperated_string(tags)
        else:
            tags.remove(tag_name)
            self.current_entity["@tags"] = methods.make_comma_seperated_string(tags)

            prefixes = methods.get_item_prefixes(self.current_entity)
            if tag_name in prefixes:
                self.modify_item_prefixes(tag_name, False)

        if tag_name == "block":
            if adding:
                self.current_entity["@tile_id_str"] = ""
            else:
                del self.current_entity["@tile_id_str"]

    def get_default_entity_dict(self):
        entity_dict = super().get_default_entity_dict()

        entity_dict["@name"] = ""
        entity_dict["@desc"] = ""
        entity_dict["@tier"] = "0"
        entity_dict["@max_stack"] = "999"
        entity_dict["@buy_price"] = "0"
        entity_dict["@sell_price"] = "0"
        entity_dict["@tags"] = ""

        entity_dict["@image_path"] = "res/images/items/"

        return entity_dict
