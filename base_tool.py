# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from ui_container import UiContainer, SplitType
from widget import *
import game_data


class Tool:
    def __init__(self):
        self.name = "None"
        self.icon = None

        self.accent_col = (128, 128, 128)
        self.light_accent_col = None
        self.dark_accent_col = None

        self.default_w = 800
        self.default_h = 600

        self.main_window = UiContainer("window", Rect(0, 0, self.default_w, self.default_h))

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

        window_top_bar.set_padding(top=2, left=0)

        window_main = self.find_container("window_main")
        window_main.background_colour = (90, 90, 90)

    def init(self):
        pygame.display.set_caption(self.name)
        pygame.display.set_icon(pygame.transform.scale(self.icon, (32, 32)))

        self.update_alt_accent_colours()

        commons.screen_w = self.default_w
        commons.screen_h = self.default_h

        commons.window = pygame.display.set_mode((commons.screen_w, commons.screen_h), pygame.RESIZABLE)

        self.create_windows()

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

        self.main_window.process_event(event)

    def update(self):
        pass

    def frame_update(self):
        altered_widgets = []
        self.main_window.frame_update(altered_widgets, pygame.mouse.get_pos())

        for widget in altered_widgets:
            self.widget_altered(widget)

    def draw(self):
        self.main_window.draw((0, 0))

    def quit(self):
        pygame.display.set_caption("Tool Selector")
        commons.window = pygame.display.set_mode((600, 150))
        commons.current_tool = None

    def widget_altered(self, widget):
        print(widget.widget_id)

    def find_container(self, container_id):
        return self.main_window.find_container(container_id)

    def update_container(self, container_id):
        self.find_container(container_id).update(None)
