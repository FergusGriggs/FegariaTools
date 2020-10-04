# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from ui_container import UiContainer, SplitType
from widget import TextWidget, SameLineWidget, CheckboxWidget, ImageWidget
import game_data


class Tool:
    def __init__(self):
        self.name = "None"
        self.icon = None

        self.default_w = 800
        self.default_h = 600

        self.main_window = UiContainer(Rect(0, 0, self.default_w, self.default_h))

    def create_windows(self):
        main_splits = self.main_window.add_split(SplitType.VERTICAL, 45, True)
        main_splits[1].background_colour = (90, 90, 90)

        main_splits[0].add_widget(ImageWidget("tool_icon", self.icon))
        main_splits[0].add_widget(SameLineWidget(10))
        main_splits[0].add_widget(TextWidget("tool_title", self.name, font=commons.font_30))
        main_splits[0].add_widget(SameLineWidget(10))
        main_splits[0].add_widget(CheckboxWidget("test_checkbox_2", size=30))
        main_splits[0].find_widget("test_checkbox_2").hide()

    def init(self):
        pygame.display.set_caption(self.name)
        pygame.display.set_icon(self.icon)

        commons.screen_w = self.default_w
        commons.screen_h = self.default_h

        commons.window = pygame.display.set_mode((commons.screen_w, commons.screen_h), pygame.RESIZABLE)

        self.create_windows()

    def process_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            commons.screen_w = event.w
            commons.screen_h = event.h

            commons.window = pygame.display.set_mode((commons.screen_w, commons.screen_h), pygame.RESIZABLE)

            self.main_window.update(Rect(0, 0, commons.screen_w, commons.screen_h))

        elif event.type == pygame.QUIT:
            self.quit()

    def update(self):
        pass

    def frame_update(self):
        altered_widgets = []
        self.main_window.frame_update(altered_widgets)

        for widget in altered_widgets:
            self.widget_altered(widget)

    def draw(self):
        self.main_window.draw()

    def quit(self):
        pygame.display.set_caption("Tool Selector")
        commons.window = pygame.display.set_mode((600, 150))
        commons.current_tool = None

    def widget_altered(self, widget):
        pass
