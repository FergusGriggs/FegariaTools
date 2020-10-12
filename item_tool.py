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

        super().init()

        self.current_item = game_data.find_element_by_attribute(game_data.item_data["items"]["item"], "@id", "0")
        self.load_property_page_for_item(self.current_item)
        self.update_container("item_properties")
        self.find_container("item_list").find_widget("item_selector_0").selected = True

    def create_windows(self):
        super().create_windows()

        self.main_window.split_line_colour = self.light_accent_col

        window_main = self.find_container("window_main")
        window_main.draw_line = False

        window_main.add_split(SplitType.HORIZONTAL, 200, True, "item_list_section", "item_properties_section")

        item_list_section = self.find_container("item_list_section")
        item_list_section.add_split(SplitType.VERTICAL, 40, False, "item_list_title", "item_list_subsection")
        item_list_section.split_line_colour = self.dark_accent_col

        item_list_title = self.find_container("item_list_title")
        item_list_title.add_widget(TextWidget("item_list_title", "Item List", font=commons.font_30))
        item_list_title.background_colour = self.accent_col

        item_list_subsection = self.find_container("item_list_subsection")
        item_list_subsection.add_split(SplitType.VERTICAL, 60, False, "item_list_functions", "item_list")
        item_list_subsection.background_colour = (60, 60, 60)
        item_list_subsection.split_line_colour = (68, 68, 68)

        item_list_functions = self.find_container("item_list_functions")
        item_list_functions.background_colour = (60, 60, 60)
        item_list_functions.add_widget(ButtonWidget("add_new_item", "Add New"))
        item_list_functions.add_widget(SameLineWidget(10))
        item_list_functions.add_widget(ButtonWidget("delete_selected_item", "Delete"))
        # Add drop-down widget when it exists to change the list sort type

        item_list = self.find_container("item_list")
        item_list.background_colour = (60, 60, 60)

        item_properties_section = self.find_container("item_properties_section")
        item_properties_section.add_split(SplitType.VERTICAL, 40, False, "item_properties_title", "item_properties")
        item_properties_section.split_line_colour = self.dark_accent_col

        item_properties_title = self.find_container("item_properties_title")
        item_properties_title.add_widget(TextWidget("item_properties_title", "Item Properties", font=commons.font_30))
        item_properties_title.background_colour = self.accent_col

        self.update_item_list()

    def update_item_list(self):
        item_list = self.find_container("item_list")
        item_list.widgets.clear()

        for element in game_data.item_data["items"]["item"]:
            id_string = "%03d" % (int(element["@id"]),)
            item_list.add_widget(TextWidget(id_string, id_string, colour=(110, 110, 110)))
            item_list.add_widget(SameLineWidget(10))
            item_list.add_widget(TextWidget(element["@name"], element["@name"]))
            item_list.add_widget(LineSelectorWidget("item_selector_" + element["@id"]))

        item_list.update(None)

    def load_property_page_for_item(self, item):
        item_properties = self.find_container("item_properties")
        item_properties.widgets.clear()

        item_properties.add_widget(TextWidget("item_id", "Id: " + item["@id"]))
        item_properties.add_widget(SameLineWidget(110))
        item_properties.add_widget(ButtonWidget("move_item_up", "Move Up"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(ButtonWidget("move_item_down", "Move Down"))

        item_properties.add_widget(TextWidget("item_name", "Name:"))
        item_properties.add_widget(SameLineWidget(110))
        item_properties.add_widget(TextInputWidget("item_name_input", item["@name"], TextInputType.STRING))
        item_properties.add_widget(TextWidget("item_desc", "Description:"))
        item_properties.add_widget(SameLineWidget(40))
        item_properties.add_widget(TextInputWidget("item_desc_input", item["@desc"], TextInputType.STRING))
        item_properties.add_widget(TextWidget("item_tags", "Tags:"))
        item_properties.add_widget(SameLineWidget(110))
        item_properties.add_widget(TextInputWidget("item_tags_input", item["@tags"], TextInputType.STRING))
        item_properties.add_widget(TextWidget("image_filepath", "Image Filepath:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextInputWidget("image_file_path_input", item["@image_filepath"], TextInputType.STRING, max_length=45))
        item_properties.add_widget(TextWidget("image_text", "Item Image:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(ImageWidget("item_image", methods.safe_load_image(item["@image_filepath"]), image_scale=4.0))

        item_properties.add_widget(TextWidget("item_image_load_fail", "Item image failed to load", colour=(255, 128, 128)))
        item_image_widget = item_properties.find_widget("item_image")
        if item_image_widget.loaded:
            item_properties.find_widget("item_image_load_fail").hide()
        else:
            item_properties.find_widget("item_image_load_fail").show()

        item_properties.add_widget(TextWidget("item_image_back_checkbox_text", "Colourkey Active?"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(CheckboxWidget("item_image_back_checkbox"))

        item_properties.add_widget(TextWidget("image_scale", "Image Scale:"))
        item_properties.add_widget(SameLineWidget(10))
        item_properties.add_widget(TextInputWidget("image_scale_input", "4.0", TextInputType.FLOAT, min_value=0.0, max_value=16.0))

        item_properties.find_widget("item_image_back_checkbox").checked = True

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

        elif widget.type == WidgetType.LINE_SELECTOR:
            self.find_container("item_list").deselect_all()
            widget.selected = True
            self.current_item = game_data.find_element_by_attribute(game_data.item_data["items"]["item"], "@id", widget.widget_id.split("_")[2])
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
                item_properties_container.find_widget("item_image").update_image_scale(float(widget.text))
                item_properties_container.update(None)

        elif widget.type == WidgetType.CHECKBOX:
            if widget.widget_id == "item_image_back_checkbox":
                item_properties = self.find_container("item_properties")
                item_properties.find_widget("item_image").toggle_colourkey()
                item_properties.render_widget_surface()

        super().widget_altered(widget)

    def reselect_current_item(self):
        id_to_select = min(len(game_data.item_data["items"]["item"]) - 1, int(self.current_item["@id"]))
        self.current_item = game_data.item_data["items"]["item"][id_to_select]
        self.find_container("item_list").find_widget("item_selector_" + str(id_to_select)).selected = True
        self.load_property_page_for_item(self.current_item)

    def quit(self):
        super().quit()

        game_data.unload_item_data()
