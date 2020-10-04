# Pygame imports
import pygame
from pygame.locals import *
from enum import Enum

import commons
from widget import OffsetData, WidgetType


class SplitType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class UiContainer:
    def __init__(self, container_id, parent_rect):
        self.container_id = container_id
        self.parent_rect = parent_rect

        if self.parent_rect is None:
            self.parent_rect = Rect(0, 0, commons.screen_w, commons.screen_h)

        self.has_split = False
        self.split_type = SplitType.HORIZONTAL
        self.split_offset = 40
        self.split_draggable = False
        self.dragging_split = False
        self.split_rects = (None, None)
        self.split_children = (None, None)
        self.split_line_colour = (90, 90, 90)
        self.split_line_rect = Rect(0, 0, 0, 0)
        self.split_line_hovering = False
        self.draw_line = True
        self.split_offset_min = self.split_offset

        self.widgets = []
        self.widget_surface = None
        self.background_colour = (68, 68, 68)

    def add_widget(self, widget):
        if not self.has_split:
            self.widgets.append(widget)

    def add_split(self, split_type, split_offset, split_draggable, container_id_1, container_id_2):
        if not self.has_split:
            self.has_split = True
            self.split_type = split_type
            self.split_offset = split_offset
            self.split_draggable = split_draggable
            self.split_offset_min = self.split_offset

            self.update_split_rects()
            self.update_split_line_rect()

            self.split_children = (UiContainer(container_id_1, self.split_rects[0]),
                                   UiContainer(container_id_2, self.split_rects[1]))

    def update(self, parent_rect):
        if parent_rect is not None:
            self.parent_rect = parent_rect

        if self.has_split:
            self.update_split_rects()
            self.update_split_line_rect()

            for split_index in range(2):
                self.split_children[split_index].update(self.split_rects[split_index])
        else:
            self.update_widget_positions()

    def frame_update(self, altered_widgets):
        if self.has_split:
            self.update_split_dragging()

            for split_index in range(2):
                self.split_children[split_index].frame_update(altered_widgets)
        else:
            for widget in self.widgets:
                widget.frame_update(altered_widgets)

    def update_split_rects(self):
        if self.split_type == SplitType.HORIZONTAL:
            self.split_rects = (Rect(self.parent_rect.x, self.parent_rect.y, self.split_offset, self.parent_rect.h),
                                Rect(self.parent_rect.x + self.split_offset, self.parent_rect.y,
                                     self.parent_rect.w - self.split_offset, self.parent_rect.h))
        else:
            self.split_rects = (Rect(self.parent_rect.x, self.parent_rect.y, self.parent_rect.w, self.split_offset),
                                Rect(self.parent_rect.x, self.parent_rect.y + self.split_offset,
                                     self.parent_rect.w, self.parent_rect.h - self.split_offset))

    def update_split_dragging(self):
        if self.split_draggable:
            if self.split_line_rect.collidepoint(pygame.mouse.get_pos()) and commons.first_mouse_hover:
                commons.first_mouse_hover = False
                self.split_line_hovering = True

                if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                    commons.first_mouse_action = False
                    self.dragging_split = True

            elif self.split_line_hovering:
                self.split_line_hovering = False

            if self.dragging_split:
                commons.first_mouse_action = False
                commons.first_mouse_hover = False
                self.split_line_hovering = True
                if self.split_type == SplitType.HORIZONTAL:
                    self.split_offset = pygame.mouse.get_pos()[0] - self.parent_rect.x
                else:
                    self.split_offset = pygame.mouse.get_pos()[1] - self.parent_rect.y
                self.clamp_split_offset()

                self.update_split_rects()
                self.update_split_line_rect()

                for split_index in range(2):
                    self.split_children[split_index].update(self.split_rects[split_index])

                if not pygame.mouse.get_pressed()[0]:
                    self.dragging_split = False

            if self.split_line_hovering or self.dragging_split:
                if self.split_type == SplitType.HORIZONTAL:
                    commons.current_cursor = commons.size_cursor_x
                else:
                    commons.current_cursor = commons.size_cursor_y

    def clamp_split_offset(self):
        if self.split_offset < self.split_offset_min:
            self.split_offset = self.split_offset_min

    def update_split_line_rect(self):
        if self.split_type == SplitType.HORIZONTAL:
            self.split_line_rect = Rect(self.parent_rect.x + self.split_offset - 2,
                                        self.parent_rect.y, 4, self.parent_rect.h)
        else:
            self.split_line_rect = Rect(self.parent_rect.x, self.parent_rect.y + self.split_offset - 2,
                                     self.parent_rect.w, 4)

    def update_widget_positions(self):
        offset_data = OffsetData()

        for widget in self.widgets:
            widget.update_position(self.parent_rect, offset_data)

    def draw(self):
        if self.has_split:
            for split_index in range(2):
                self.split_children[split_index].draw()
            self.draw_split_line()
        else:
            pygame.draw.rect(commons.window, self.background_colour, self.parent_rect, 0)

            for widget in self.widgets:
                widget.draw()

    def draw_split_line(self):
        if self.draw_line or self.split_line_hovering:
            if self.split_line_hovering:
                pygame.draw.rect(commons.window, (255, 255, 255), self.split_line_rect, 0)
            else:
                pygame.draw.rect(commons.window, self.split_line_colour, self.split_line_rect, 0)

    def get_widgets_of_type(self, widget_type, widget_list):
        if self.has_split:
            for split_index in range(2):
                self.split_children[split_index].get_widgets_of_type(widget_type, widget_list)
        else:
            for widget in self.widgets:
                if widget.type == widget_type:
                    widget_list.append(widget)

    def get_widgets_with_name(self, name, widget_list):
        if self.has_split:
            for split_index in range(2):
                self.split_children[split_index].get_widgets_with_name(name, widget_list)
        else:
            for widget in self.widgets:
                if widget.name == name:
                    widget_list.append(widget)

    def find_widget(self, widget_id):
        if self.has_split:
            for split_index in range(2):
                widget = self.split_children[split_index].find_widget(widget_id)
                if widget is not None:
                    return widget
        else:
            for widget in self.widgets:
                if widget.widget_id == widget_id:
                    return widget
        return None

    def find_container(self, container_id):
        if self.has_split:
            for split_index in range(2):
                container = self.split_children[split_index].find_container(container_id)
                if container is not None:
                    return container
        elif self.container_id == container_id:
            return self
        return None

    def deselect_all(self):
        if self.has_split:
            for split_index in range(2):
                self.split_children[split_index].deselect_all()
        else:
            for widget in self.widgets:
                if widget.type == WidgetType.LINE_SELECTOR:
                    widget.selected = False
