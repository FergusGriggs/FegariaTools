# Pygame imports
import pygame
from pygame.locals import *
from enum import Enum

import commons
from widget import *


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

        self.padding_top = 5
        self.padding_left = 5
        self.padding_bot = 5
        self.padding_right = 5

        self.widgets = []
        self.widget_surface = None
        self.widget_surface_rect = Rect(0, 0, 0, 0)
        self.widget_align_type = WidgetAlignType.LEFT
        self.background_colour = (68, 68, 68)

        self.scrollable_x = False
        self.content_overflow_x = False
        self.content_size_x = 0
        self.scroll_x_offset = 0
        self.scroll_velocity_x = 0
        self.scroll_bar_x_size = 0
        self.scroll_bar_rect_x = None
        self.dragging_scroll_bar_x = False
        self.scroll_bar_grab_offset_x = 0
        self.scroll_bar_hover_x = False

        self.scrollable_y = False
        self.content_overflow_y = False
        self.content_size_y = 0
        self.scroll_y_offset = 0
        self.scroll_velocity_y = 0
        self.scroll_bar_y_size = 0
        self.scroll_bar_rect_y = None
        self.dragging_scroll_bar_y = False
        self.scroll_bar_grab_offset_y = 0
        self.scroll_bar_hover_y = False

        self.last_relative_mouse_pos = (0, 0)

    def add_widget(self, widget):
        if not self.has_split:
            self.widgets.append(widget)
            widget.ui_container = self

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
            self.render_widget_surface()

    def frame_update(self, altered_widgets, relative_mouse_pos):
        if self.has_split:
            self.update_split_dragging(relative_mouse_pos)

            for split_index in range(2):
                child_relative_mouse_pos = (relative_mouse_pos[0] - self.split_rects[split_index].x,
                                            relative_mouse_pos[1] - self.split_rects[split_index].y)

                self.split_children[split_index].frame_update(altered_widgets, child_relative_mouse_pos)
        else:
            self.last_relative_mouse_pos = relative_mouse_pos
            self.update_scroll_velocity()

            self.update_scroll_bars(relative_mouse_pos)

            scrolled_mouse_pos = (relative_mouse_pos[0] + self.scroll_x_offset, relative_mouse_pos[1] + self.scroll_y_offset)

            mouse_over_rect = Rect(0, 0, self.parent_rect.w, self.parent_rect.h).collidepoint(relative_mouse_pos)
            for widget in self.widgets:
                if mouse_over_rect:
                    widget.frame_update(altered_widgets, scrolled_mouse_pos)
                elif widget.type == WidgetType.BUTTON or widget.type == WidgetType.LINE_SELECTOR:
                    widget.hovered = False

    def update_scroll_bars(self, relative_mouse_pos):
        self.scroll_bar_hover_x = False
        self.scroll_bar_hover_y = False

        if self.content_overflow_y:
            pixel_offset = int((self.parent_rect.h - self.scroll_bar_y_size) * (
                        self.scroll_y_offset / (self.content_size_y - self.parent_rect.h)))
            self.scroll_bar_rect_y = Rect(self.parent_rect.w - commons.y_scroll_bar_width, pixel_offset,
                                          commons.y_scroll_bar_width, self.scroll_bar_y_size)
            if commons.first_mouse_hover and self.scroll_bar_rect_y.collidepoint(*relative_mouse_pos):
                commons.first_mouse_hover = False
                self.scroll_bar_hover_y = True
                if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                    commons.first_mouse_action = False
                    self.dragging_scroll_bar_y = True
                    self.scroll_bar_grab_offset_y = relative_mouse_pos[1] - pixel_offset
                    commons.dragging_object = True

        if self.content_overflow_x:
            pixel_offset = int((self.parent_rect.w - self.scroll_bar_x_size) * (
                        self.scroll_x_offset / (self.content_size_x - self.parent_rect.w)))
            self.scroll_bar_rect_x = Rect(pixel_offset, self.parent_rect.h - commons.x_scroll_bar_width,
                                          self.scroll_bar_x_size, commons.x_scroll_bar_width)
            if commons.first_mouse_hover and self.scroll_bar_rect_x.collidepoint(*relative_mouse_pos):
                commons.first_mouse_hover = False
                self.scroll_bar_hover_x = True
                if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                    commons.first_mouse_action = False
                    self.dragging_scroll_bar_x = True
                    self.scroll_bar_grab_offset_x = relative_mouse_pos[0] - pixel_offset
                    commons.dragging_object = True

        if self.dragging_scroll_bar_x:
            scroll_to_offset = int(((relative_mouse_pos[0] - self.scroll_bar_grab_offset_x) / (
                        self.parent_rect.w - self.scroll_bar_x_size)) * (self.content_size_x - self.parent_rect.w))
            self.scroll_container_to_value((scroll_to_offset, None))
        if self.dragging_scroll_bar_y:
            scroll_to_offset = int(((relative_mouse_pos[1] - self.scroll_bar_grab_offset_y) / (
                        self.parent_rect.h - self.scroll_bar_y_size)) * (self.content_size_y - self.parent_rect.h))
            self.scroll_container_to_value((None, scroll_to_offset))

        if not pygame.mouse.get_pressed()[0]:
            self.dragging_scroll_bar_x = False
            self.dragging_scroll_bar_y = False

    def update_split_rects(self):
        if self.split_type == SplitType.HORIZONTAL:
            self.split_rects = (Rect(0, 0, self.split_offset, self.parent_rect.h),
                                Rect(self.split_offset, 0, self.parent_rect.w - self.split_offset, self.parent_rect.h))
        else:
            self.split_rects = (Rect(0, 0, self.parent_rect.w, self.split_offset),
                                Rect(0, self.split_offset, self.parent_rect.w, self.parent_rect.h - self.split_offset))

    def update_split_dragging(self, relative_mouse_pos):
        if self.split_draggable:
            if self.split_line_rect.collidepoint(*relative_mouse_pos) and commons.first_mouse_hover:
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
                    self.split_offset = relative_mouse_pos[0] - self.parent_rect.x
                else:
                    self.split_offset = relative_mouse_pos[1] - self.parent_rect.y
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
            self.split_line_rect = Rect(self.split_offset - 1, 0, 3, self.parent_rect.h)
        else:
            self.split_line_rect = Rect(0, self.split_offset - 1, self.parent_rect.w, 3)

    def update_widget_positions(self):
        # Assign widgets to a line and calculate the extents of the line
        widget_lines = [WidgetLine()]
        current_line_index = 0

        for i in range(len(self.widgets)):
            # If it's the first widget of a new line
            if i > 0 and self.widgets[i].base_type == WidgetBaseType.OBJECT and self.widgets[i - 1].base_type != WidgetBaseType.SAME_LINE:
                widget_lines[current_line_index].create_extents()
                widget_lines.append(WidgetLine())
                current_line_index += 1

            widget_lines[current_line_index].widgets.append(self.widgets[i])

        # Create extents for last line
        if len(widget_lines[current_line_index].widgets) > 0:
            widget_lines[current_line_index].create_extents()

        # Update content size with widget extents
        self.content_size_x = 0
        self.content_size_y = 0

        for line in widget_lines:
            self.content_size_x = max(self.content_size_x, line.length)
            self.content_size_y += line.height

        # Add padding
        self.content_size_x += self.padding_left + self.padding_right
        self.content_size_y += self.padding_top + self.padding_bot

        # Check if the content is overflowing the boundaries
        self.update_overflow_data()

        # Extend surface to the size of the parent rect if it's too small
        self.content_size_x = max(self.content_size_x, self.parent_rect.w)
        self.content_size_y = max(self.content_size_y, self.parent_rect.h)

        # Place all the widgets
        y_offset_ref = ValueRef(self.padding_top)

        for line in widget_lines:
            self.arrange_widgets_on_line(line, y_offset_ref)

        # Update the surface rect
        self.widget_surface_rect.w = max(self.parent_rect.w, self.content_size_x)
        self.widget_surface_rect.h = max(self.parent_rect.h, self.content_size_y)

        # Apply any late widget updates that require the final position of lines, size of content etc
        for line in widget_lines:
            for widget in line.widgets:
                widget.late_position_update(line, self)

    def arrange_widgets_on_line(self, widget_line, y_offset_ref):
        # Place widgets based on align type
        x_start = self.padding_left

        right_offset = self.padding_right
        if self.content_overflow_y:
            right_offset += commons.y_scroll_bar_spacing

        if self.widget_align_type == WidgetAlignType.CENTRE:
            padded_width = self.content_size_x - self.padding_left - self.padding_right
            x_start = int(max(self.padding_left + padded_width * 0.5 - widget_line.length * 0.5, 0))
        elif self.widget_align_type == WidgetAlignType.RIGHT:
            x_start = int(max(self.content_size_x - right_offset - widget_line.length, 0))

        for widget in widget_line.widgets:
            if not widget.hidden or widget.type == WidgetType.SAME_LINE:
                widget.rect.x = x_start
                widget.rect.y = y_offset_ref.value + widget_line.height * 0.5 - widget.rect.h * 0.5

                x_start += widget.rect.w

        # Give the line it's final y position
        widget_line.y_pos = y_offset_ref.value

        # Move the line down by the line height
        y_offset_ref.value += widget_line.height

    def update_overflow_data(self):
        # Work out the final size of the content including any necessary scroll bars
        # and determine if content is overflowing in either axis
        if self.content_size_y > self.parent_rect.h:
            self.content_overflow_y = True
            self.content_size_x += commons.y_scroll_bar_spacing
        else:
            self.content_overflow_y = False

        if self.content_size_x > self.parent_rect.w:
            self.content_overflow_x = True
            self.content_size_y += commons.x_scroll_bar_spacing

            if not self.content_overflow_y and self.content_size_y > self.parent_rect.h:
                self.content_overflow_y = True
                self.content_size_x += commons.y_scroll_bar_spacing
        else:
            self.content_overflow_x = False

        if not self.scrollable_x:
            self.content_overflow_x = False
        if not self.scrollable_y:
            self.content_overflow_y = False

        # Work out the sizes of the scrollbars that are required
        if self.content_overflow_x and self.content_size_x > 0:
            self.scroll_bar_x_size = int(self.parent_rect.w * (self.parent_rect.w / self.content_size_x))
        else:
            self.scroll_x_offset = 0

        if self.content_overflow_y and self.content_size_y > 0:
            self.scroll_bar_y_size = int(self.parent_rect.h * (self.parent_rect.h / self.content_size_y))
        else:
            self.scroll_y_offset = 0

    def render_widget_surface(self):
        self.widget_surface = pygame.Surface((self.widget_surface_rect.w, self.widget_surface_rect.h))
        self.widget_surface.fill(self.background_colour)

        for widget in self.widgets:
            widget.render_to_surface(self.widget_surface)

    def draw(self, relative_position):
        if self.has_split:
            for split_index in range(2):
                new_relative_position = (relative_position[0] + self.split_rects[split_index].x,
                                         relative_position[1] + self.split_rects[split_index].y)
                self.split_children[split_index].draw(new_relative_position)
            self.draw_split_line(relative_position)
        else:
            commons.window.blit(self.widget_surface, relative_position, Rect(self.scroll_x_offset, self.scroll_y_offset,
                                                                             self.parent_rect.w, self.parent_rect.h))
            for widget in self.widgets:
                widget.draw(relative_position, (self.scroll_x_offset, self.scroll_y_offset), self.parent_rect)

            if self.content_overflow_x and self.scroll_bar_rect_x is not None:
                colour = commons.border_col
                if self.dragging_scroll_bar_x:
                    colour = commons.selected_border_col
                elif self.scroll_bar_hover_x:
                    colour = commons.hover_border_col
                pygame.draw.rect(commons.window, colour,
                                 Rect(relative_position[0] + self.scroll_bar_rect_x.x,
                                      relative_position[1] + self.scroll_bar_rect_x.y,
                                      self.scroll_bar_rect_x.w, self.scroll_bar_rect_x.h), 0)

            if self.content_overflow_y and self.scroll_bar_rect_y is not None:
                colour = commons.border_col
                if self.dragging_scroll_bar_y:
                    colour = commons.selected_border_col
                elif self.scroll_bar_hover_y:
                    colour = commons.hover_border_col
                pygame.draw.rect(commons.window, colour,
                                 Rect(relative_position[0] + self.scroll_bar_rect_y.x,
                                      relative_position[1] + self.scroll_bar_rect_y.y,
                                      self.scroll_bar_rect_y.w, self.scroll_bar_rect_y.h), 0)

    def process_event(self, event):
        if self.has_split:
            for split_index in range(2):
                self.split_children[split_index].process_event(event)
        else:
            if Rect(0, 0, self.parent_rect.w, self.parent_rect.h).collidepoint(self.last_relative_mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.add_scroll_vel((0, -1000))
                elif event.button == 5:
                    self.add_scroll_vel((0, 1000))
            should_update_widget_surface = False
            for widget in self.widgets:
                if widget.process_event(event):
                    should_update_widget_surface = True

            if should_update_widget_surface:
                self.render_widget_surface()

    def update_scroll_velocity(self):
        self.scroll_velocity_x *= 1.0 - commons.delta_time * 10.0
        self.scroll_velocity_y *= 1.0 - commons.delta_time * 10.0

        self.scroll_container((min(300, self.scroll_velocity_x * commons.delta_time), min(300, self.scroll_velocity_y * commons.delta_time)))

    def add_scroll_vel(self, diff):
        self.scroll_velocity_x += diff[0]
        self.scroll_velocity_y += diff[1]

    def scroll_container(self, diff):
        if self.content_overflow_x:
            self.scroll_x_offset += int(diff[0])
            if self.scroll_x_offset < 0:
                self.scroll_x_offset = 0
                self.scroll_velocity_x = 0.0

            elif self.scroll_x_offset > self.widget_surface_rect.w - self.parent_rect.w:
                self.scroll_x_offset = self.widget_surface_rect.w - self.parent_rect.w
                self.scroll_velocity_x = 0.0

        if self.content_overflow_y:
            self.scroll_y_offset += int(diff[1])
            if self.scroll_y_offset < 0:
                self.scroll_y_offset = 0
                self.scroll_velocity_y = 0.0

            elif self.scroll_y_offset > self.widget_surface_rect.h - self.parent_rect.h:
                self.scroll_y_offset = self.widget_surface_rect.h - self.parent_rect.h
                self.scroll_velocity_y = 0.0

    def scroll_container_to_value(self, offset_value):
        if self.content_overflow_x and offset_value[0] is not None:
            self.scroll_x_offset = min(self.widget_surface_rect.w - self.parent_rect.w, max(0, offset_value[0]))
        if self.content_overflow_y and offset_value[1] is not None:
            self.scroll_y_offset = min(self.widget_surface_rect.h - self.parent_rect.h, max(0, offset_value[1]))

    def draw_split_line(self, relative_position):
        if self.draw_line or self.split_line_hovering:
            if self.split_line_hovering:
                pygame.draw.rect(commons.window, (255, 255, 255),
                                 Rect(relative_position[0] + self.split_line_rect.x,
                                      relative_position[1] + self.split_line_rect.y,
                                      self.split_line_rect.w, self.split_line_rect.h), 0)
            else:
                pygame.draw.rect(commons.window, self.split_line_colour,
                                 Rect(relative_position[0] + self.split_line_rect.x,
                                      relative_position[1] + self.split_line_rect.y,
                                      self.split_line_rect.w, self.split_line_rect.h), 0)

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

    def make_scrollable(self, x=True, y=True):
        self.scrollable_x = x
        self.scrollable_y = y

    def set_padding(self, top=None, left=None, bot=None, right=None):
        if top is not None:
            self.padding_top = top
        if left is not None:
            self.padding_left = left
        if bot is not None:
            self.padding_bot = bot
        if right is not None:
            self.padding_right = right

    def set_widget_align_type(self, widget_align_type):
        self.widget_align_type = widget_align_type