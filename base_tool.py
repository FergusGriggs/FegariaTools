# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
import subprocess
import os
from ui_container import UiContainer, SplitType, SortType
from widget import *
import game_data
import collections
import ui_container

class Tool:
    def __init__(self):
        self.name = "None"
        self.entity_type = "None"
        self.xml_data_root = {}
        self.xml_group_name = "None"
        self.xml_type_name = "None"
        self.icon = None

        self.entity_list_sort_type = SortType.BY_ID
        self.current_entity = None

        self.accent_col = (128, 128, 128)
        self.light_accent_col = (0, 0, 0)
        self.dark_accent_col = (0, 0, 0)

        self.main_window = UiContainer("window", Rect(0, 0, commons.screen_w, commons.screen_h), None)

    def create_windows(self):
        self.main_window.add_split(SplitType.VERTICAL, 45, True, "window_top_bar", "window_main")

        window_top_bar = self.find_container("window_top_bar")
        window_top_bar.add_widget(ImageWidget("tool_icon", self.icon))
        window_top_bar.add_widget(SameLineWidget(10))
        window_top_bar.add_widget(TextWidget("tool_title", self.name, font=commons.font_30))
        window_top_bar.add_widget(SameLineWidget(10))
        window_top_bar.add_widget(CheckboxWidget("test_checkbox_2", size=30))
        window_top_bar.find_widget("test_checkbox_2").hide()
        window_top_bar.add_widget(SameLineWidget(10))
        window_top_bar.add_widget(ButtonWidget("export_data", "Export"))
        window_top_bar.add_widget(SameLineWidget(10))
        window_top_bar.add_widget(ButtonWidget("load_data", "Load"))
        window_top_bar.add_widget(SameLineWidget(10))
        window_top_bar.add_widget(ButtonWidget("open_data_folder", "Open Data Folder"))
        window_top_bar.add_widget(SameLineWidget(10))
        window_top_bar.add_widget(DropDownWidget("tool_switcher", ["Crafting Tool", "Entity Tool", "Item Tool", "Loot Tool", "Structure Tool", "Tile Tool", "AI Tool", "World Gen Tool", "Sound Tool"], DropDownType.SELECT, initial_string=self.name, min_widget_length=0))

        window_top_bar.set_padding(top=2, left=0)

        window_main = self.find_container("window_main")
        window_main.background_colour = (90, 90, 90)

        self.main_window.split_line_colour = self.light_accent_col

        window_main = self.find_container("window_main")
        window_main.draw_line = False

        window_main.add_split(SplitType.HORIZONTAL, 320, True, "entity_list_section", "entity_properties_section")

        entity_list_section = self.find_container("entity_list_section")
        entity_list_section.add_split(SplitType.VERTICAL, 40, False, "entity_list_title", "entity_list_subsection")
        entity_list_section.split_line_colour = self.dark_accent_col

        entity_list_title = self.find_container("entity_list_title")
        entity_list_title.add_widget(TextWidget("entity_list_title", self.entity_type + " List", font=commons.font_30))
        entity_list_title.background_colour = self.accent_col

        entity_list_subsection = self.find_container("entity_list_subsection")
        entity_list_subsection.add_split(SplitType.VERTICAL, 35, False, "entity_list_functions", "entity_list")
        entity_list_subsection.background_colour = (60, 60, 60)
        entity_list_subsection.split_line_colour = (68, 68, 68)

        entity_list_functions = self.find_container("entity_list_functions")
        entity_list_functions.background_colour = (60, 60, 60)

        entity_list_functions.add_widget(ButtonWidget("cycle_entity_list_sort_type", "Sort"))
        entity_list_functions.add_widget(SameLineWidget(10))
        entity_list_functions.add_widget(DropDownWidget("modify_list", ["Add New", "Duplicate", "Delete"], DropDownType.MENU, "Modify List", min_widget_length=0))
        entity_list_functions.add_widget(SameLineWidget(10))
        entity_list_functions.add_widget(ButtonWidget("move_entity_down", "Id+"))
        entity_list_functions.add_widget(SameLineWidget(10))
        entity_list_functions.add_widget(ButtonWidget("move_entity_up", "Id-"))

        entity_list_functions.set_widget_align_type(WidgetAlignType.CENTRE)
        # Add drop-down widget when it exists to change the list sort type

        entity_list = self.find_container("entity_list")
        entity_list.background_colour = (60, 60, 60)
        entity_list.make_scrollable()

        entity_properties_section = self.find_container("entity_properties_section")
        entity_properties_section.add_split(SplitType.VERTICAL, 40, False, "entity_properties_title", "entity_properties")
        entity_properties_section.split_line_colour = self.dark_accent_col

        entity_properties_title = self.find_container("entity_properties_title")
        entity_properties_title.add_widget(TextWidget("entity_properties_title", self.entity_type + " Properties", font=commons.font_30))
        entity_properties_title.background_colour = self.accent_col

        entity_properties = self.find_container("entity_properties")
        entity_properties.make_scrollable()

        self.update_entity_list()

    def init(self):
        pygame.display.set_caption(self.name)
        pygame.display.set_icon(pygame.transform.scale(self.icon, (32, 32)))

        self.update_alt_accent_colours()

        self.create_windows()

        self.current_entity = game_data.find_element_by_attribute(self.get_xml_entity_list(), "@id", "1")
        self.load_property_page_for_entity(self.current_entity)
        self.update_container("entity_properties")
        self.find_container("entity_list").find_widget("entityselector_1").select(alter_main_selection=False)

        self.main_window.update(None)

    def update_alt_accent_colours(self):
        self.light_accent_col = methods.modify_col(self.accent_col, 1.25)
        self.dark_accent_col = methods.modify_col(self.accent_col, 0.75)

    def process_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            commons.screen_w = event.w
            commons.screen_h = event.h

            commons.window = pygame.display.set_mode((commons.screen_w, commons.screen_h), pygame.RESIZABLE)

            self.main_window.update(Rect(0, 0, commons.screen_w, commons.screen_h))

        elif event.type == pygame.QUIT:
            self.quit()
            return

        self.main_window.process_event(event)

    def update(self):
        pass

    def frame_update(self):
        altered_widgets = []
        if commons.global_widget is not None:
            commons.global_widget.global_frame_update(altered_widgets, pygame.mouse.get_pos())

        self.main_window.frame_update(altered_widgets, pygame.mouse.get_pos())

        for widget in altered_widgets:
            self.widget_altered(widget)

    def draw(self):
        self.main_window.draw((0, 0))

        if commons.global_widget is not None:
            commons.global_widget.global_draw()

    def quit(self):
        commons.current_tool = None

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "open_data_folder":
                dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\res\\data\\"
                subprocess.Popen(f'explorer "' + dir_path + '"')

            elif widget.widget_id == "modify_list_add_new":
                index_to_add_at = int(self.current_entity["@id"]) + 1
                entity_dict = self.get_default_entity_dict()
                entity_dict["@id"] = str(index_to_add_at)

                self.get_xml_entity_list().insert(index_to_add_at, entity_dict)

                game_data.reassign_element_ids(self.get_xml_entity_list())

                self.update_entity_list()
                self.reselect_current_entity()

            elif widget.widget_id == "modify_list_duplicate":
                index_to_add_at = int(self.current_entity["@id"]) + 1
                dupe_dict = collections.OrderedDict(self.current_entity)
                dupe_dict["@id"] = str(index_to_add_at)
                dupe_dict["@id_str"] = self.current_entity["@id_str"] + "_2"

                self.get_xml_entity_list().insert(index_to_add_at, dupe_dict)

                game_data.reassign_element_ids(self.get_xml_entity_list())

                self.update_entity_list()
                self.reselect_current_entity()

            elif widget.widget_id == "move_entity_up":
                if int(self.current_entity["@id"]) > 0:
                    self.get_xml_entity_list().remove(self.current_entity)

                    self.current_entity["@id"] = str(int(self.current_entity["@id"]) - 1)

                    self.get_xml_entity_list().insert(int(self.current_entity["@id"]), self.current_entity)

                    game_data.reassign_element_ids(self.get_xml_entity_list())
                    self.update_entity_list()
                    self.reselect_current_entity()

            elif widget.widget_id == "move_entity_down":
                if int(self.current_entity["@id"]) < len(self.get_xml_entity_list()):
                    self.get_xml_entity_list().remove(self.current_entity)

                    self.current_entity["@id"] = str(int(self.current_entity["@id"]) + 1)

                    self.get_xml_entity_list().insert(int(self.current_entity["@id"]), self.current_entity)

                    game_data.reassign_element_ids(self.get_xml_entity_list())
                    self.update_entity_list()
                    self.reselect_current_entity()

            elif widget.widget_id == "cycle_entity_list_sort_type":
                self.entity_list_sort_type = ui_container.cycle_sort_type(self.entity_list_sort_type)
                self.update_entity_list()
                self.reselect_current_entity()

                entity_list_functions = self.find_container("entity_list_functions")
                entity_list_functions.widgets.clear()

                if self.entity_list_sort_type == SortType.BY_ID:
                    entity_list_functions.add_widget(ButtonWidget("cycle_entity_list_sort_type", "Sort"))
                    entity_list_functions.add_widget(SameLineWidget(10))
                    entity_list_functions.add_widget(DropDownWidget("modify_list", ["Add New", "Duplicate", "Delete"], DropDownType.MENU, initial_string="Modify List", min_widget_length=0))
                    entity_list_functions.add_widget(SameLineWidget(10))
                    entity_list_functions.add_widget(ButtonWidget("move_entity_down", "Id+"))
                    entity_list_functions.add_widget(SameLineWidget(10))
                    entity_list_functions.add_widget(ButtonWidget("move_entity_up", "Id-"))

                else:
                    entity_list_functions.add_widget(ButtonWidget("cycle_entity_list_sort_type", "Sort"))
                    entity_list_functions.add_widget(SameLineWidget(10))
                    entity_list_functions.add_widget(TextWidget("sort_type_text", ": " + self.entity_list_sort_type.name))

                entity_list_functions.update(None)

            elif widget.widget_id == "modify_list_delete":
                if len(self.get_xml_entity_list()) > 1:
                    game_data.remove_element_by_attribute(self.get_xml_entity_list(), "@id", self.current_entity["@id"])
                    game_data.reassign_element_ids(self.get_xml_entity_list())

                    self.update_entity_list()
                    self.reselect_current_entity()

        elif widget.type == WidgetType.LINE_SELECTOR:
            split_id = widget.widget_id.split("_")
            if len(split_id) > 0 and split_id[0] == "entityselector":
                self.find_container("entity_list").deselect_all()
                widget.select(alter_main_selection=False)
                self.current_entity = game_data.find_element_by_attribute(self.get_xml_entity_list(), "@id", split_id[1])
                self.load_property_page_for_entity(self.current_entity)

        elif widget.type == WidgetType.DROP_DOWN:
            if widget.widget_id == "tool_switcher":
                if widget.selected_string != self.name:
                    commons.next_tool = widget.selected_string
                    commons.global_widget = None
                    commons.deselect_selected_widget()
                    self.quit()

        print(widget.widget_id)

    def find_container(self, container_id):
        return self.main_window.find_container(container_id)

    def update_container(self, container_id):
        self.find_container(container_id).update(None)

    def update_entity_list(self):
        entity_list = self.find_container("entity_list")
        entity_list.widgets.clear()

        if self.entity_list_sort_type == SortType.BY_ID:
            self.xml_data_root[self.xml_group_name][self.xml_type_name] = sorted(self.get_xml_entity_list(), key=lambda x: int(x["@id"]))
        elif self.entity_list_sort_type == SortType.BY_ID_REVERSE:
            self.xml_data_root[self.xml_group_name][self.xml_type_name] = sorted(self.get_xml_entity_list(), key=lambda x: int(x["@id"]), reverse=True)
        elif self.entity_list_sort_type == SortType.ALPHABETICALLY:
            self.xml_data_root[self.xml_group_name][self.xml_type_name] = sorted(self.get_xml_entity_list(), key=lambda x: x["@id_str"])
        elif self.entity_list_sort_type == SortType.ALPHABETICALLY_REVERSE:
            self.xml_data_root[self.xml_group_name][self.xml_type_name] = sorted(self.get_xml_entity_list(), key=lambda x: x["@id_str"], reverse=True)

        for element in self.get_xml_entity_list():
            id_string = "%03d" % (int(element["@id"]),)
            entity_list.add_widget(TextWidget(id_string, id_string, colour=(110, 110, 110)))
            entity_list.add_widget(SameLineWidget(10))
            entity_list.add_widget(TextWidget(element["@id_str"], element["@id_str"].split(".")[-1]))
            entity_list.add_widget(LineSelectorWidget("entityselector_" + element["@id"]))

        entity_list.update(None)

    def reselect_current_entity(self):
        id_to_select = min(len(self.get_xml_entity_list()) - 1, int(self.current_entity["@id"]))
        for entity_index in range(len(self.get_xml_entity_list())):
            if self.get_xml_entity_list()[entity_index]["@id"] == self.current_entity["@id"]:
                id_to_select = entity_index
                break

        self.current_entity = self.get_xml_entity_list()[id_to_select]
        self.find_container("entity_list").find_widget("entityselector_" + self.current_entity["@id"]).select(alter_main_selection=False)

    def load_property_page_for_entity(self, entity):
        pass

    def get_default_entity_dict(self):
        entity_dict = collections.OrderedDict()
        entity_dict["@id_str"] = "fg." + self.xml_type_name + ".UNNAMED"
        entity_dict["@id"] = "0"

        return entity_dict

    def get_xml_entity_list(self):
        return self.xml_data_root[self.xml_group_name][self.xml_type_name]
