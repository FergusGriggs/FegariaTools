# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons

from enum import Enum


class WidgetType:
    BASE = 0
    IMAGE = 1
    TEXT = 2
    SAME_LINE = 3
    CHECKBOX = 4
    LINE_SELECTOR = 5
    BUTTON = 6
    TEXT_INPUT = 7


class OffsetData:
    def __init__(self):
        self.horizontal = 0
        self.vertical = 0
        self.line_height = 0
        self.new_line = False
        self.space_width = 0


class Widget:
    def __init__(self, widget_id):
        self.widget_id = widget_id
        self.type = WidgetType.BASE
        self.surface = None
        self.rect = None
        self.hidden = True

    def update_position(self, container_rect, offset_data):
        if not self.hidden:
            if offset_data.new_line:
                offset_data.horizontal = offset_data.space_width
                offset_data.vertical += offset_data.line_height
                offset_data.line_height = 0
            else:
                offset_data.new_line = True
                offset_data.horizontal += offset_data.space_width

            self.rect.x = container_rect.x + 5 + offset_data.horizontal
            self.rect.y = container_rect.y + 2 + offset_data.vertical

            offset_data.horizontal += self.rect.w
            offset_data.space_width = 0

            if self.rect.h > offset_data.line_height:
                offset_data.line_height = self.rect.h

        elif offset_data.new_line is False:
            offset_data.new_line = True
            offset_data.space_width = 0

    def frame_update(self, altered_widgets):
        pass

    def draw(self):
        if not self.hidden:
            commons.window.blit(self.surface, (self.rect.x, self.rect.y))

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def toggle_hidden(self):
        self.hidden = not self.hidden


class ImageWidget(Widget):
    def __init__(self, widget_id, image):
        super().__init__(widget_id)

        self.type = WidgetType.IMAGE
        self.surface = image
        self.rect = self.surface.get_rect()
        self.hidden = False


class TextWidget(Widget):
    def __init__(self, widget_id, text, colour=commons.text_col, font=None):
        super().__init__(widget_id)

        self.type = WidgetType.TEXT
        self.text = text
        self.font = font
        if self.font is None:
            self.font = commons.font_20
        self.colour = colour

        self.render_text()
        self.rect = self.surface.get_rect()

        self.hidden = False

    def set_text(self, new_text):
        self.text = new_text
        self.render_text()

    def render_text(self):
        self.surface = self.font.render(self.text, True, self.colour)


class SameLineWidget(Widget):
    def __init__(self, space_width):
        super().__init__("space")

        self.type = WidgetType.SAME_LINE
        self.space_width = space_width

    def update_position(self, container_rect, offset_data):
        offset_data.new_line = False
        offset_data.space_width = self.space_width


class CheckboxWidget(Widget):
    def __init__(self, widget_id, size=20, colour=commons.text_col):
        super().__init__(widget_id)

        self.type = WidgetType.CHECKBOX
        self.rect = Rect(0, 0, size, size)
        self.surface = pygame.Surface((size, size))

        self.size = size
        self.colour = colour
        self.checked = False
        self.hidden = False
        self.hovered = False

    def frame_update(self, altered_widgets):
        if not self.hidden:
            self.hovered = False
            if commons.first_mouse_hover and self.rect.collidepoint(*pygame.mouse.get_pos()):
                self.hovered = True
                commons.first_mouse_hover = False
                commons.current_cursor = commons.button_cursor
                if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                    commons.first_mouse_action = False
                    self.checked = not self.checked
                    altered_widgets.append(self)

    def draw(self):
        if not self.hidden:
            pygame.draw.circle(commons.window, self.colour, self.rect.center, int(self.size * 0.5), 2)
            if self.checked:
                pygame.draw.circle(commons.window, self.colour, self.rect.center, int(self.size * 0.2), 0)
            # pygame.draw.rect(commons.window, self.colour,
            #                 Rect(self.rect.x + 4, self.rect.y + 4, self.size - 8, self.size - 8), 0)


class LineSelectorWidget(Widget):
    def __init__(self, widget_id):
        super().__init__(widget_id)

        self.type = WidgetType.LINE_SELECTOR
        self.rect = Rect(0, 0, 0, 0)
        self.selected = False
        self.hovered = False

    def update_position(self, container_rect, offset_data):
        self.rect.x = container_rect.x
        self.rect.y = container_rect.y + offset_data.vertical
        self.rect.w = container_rect.w
        self.rect.h = offset_data.line_height

    def frame_update(self, altered_widgets):
        self.hovered = False
        if self.rect.collidepoint(*pygame.mouse.get_pos()) and commons.first_mouse_hover:
            commons.first_mouse_hover = False
            commons.current_cursor = commons.button_cursor
            self.hovered = True
            if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                commons.first_mouse_action = False
                altered_widgets.append(self)

    def draw(self):
        if self.selected:
            pygame.draw.rect(commons.window, (255, 255, 255), self.rect, 2)
        elif self.hovered:
            pygame.draw.rect(commons.window, (128, 128, 128), self.rect, 2)


class ButtonWidget(Widget):
    def __init__(self, widget_id, text, font=None, text_colour=commons.text_col,
                 back_colour=commons.back_col, border_colour=commons.border_col):
        super().__init__(widget_id)

        self.text = text
        self.font = font
        if self.font is None:
            self.font = commons.font_20
        self.text_colour = text_colour
        self.back_colour = back_colour
        self.border_colour = border_colour
        self.hidden = False
        self.hovered = False

        self.type = WidgetType.BUTTON

        self.render_surface()

    def render_surface(self):
        text_size = self.font.size(self.text)
        self.rect = Rect(0, 0, text_size[0] + 6, text_size[1] + 2)
        self.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.back_colour)
        pygame.draw.rect(self.surface, self.border_colour, self.rect, 2)
        self.surface.blit(self.font.render(self.text, True, self.text_colour), (4, 0))

    def set_text(self, text):
        self.text = text
        self.render_surface()

    def frame_update(self, altered_widgets):
        self.hovered = False
        if self.rect.collidepoint(*pygame.mouse.get_pos()) and commons.first_mouse_hover:
            commons.first_mouse_hover = False
            commons.current_cursor = commons.button_cursor
            self.hovered = True
            if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                commons.first_mouse_action = False
                altered_widgets.append(self)

    def draw(self):
        super().draw()

        if self.hovered:
            pygame.draw.rect(commons.window, (128, 128, 128), self.rect, 2)


class TextInputType(Enum):
    STRING = 0
    FLOAT = 1
    INT = 2


class TextInputWidget(Widget):
    def __init__(self, widget_id, initial_text, input_type, font=None, text_colour=commons.text_col,
                 back_colour=commons.back_col, border_colour=commons.border_col):
        super().__init__(widget_id)

        self.text = initial_text
        self.input_type = input_type
        self.font = font
        if self.font is None:
            self.font = commons.font_20
        self.text_colour = text_colour
        self.back_colour = back_colour
        self.border_colour = border_colour

        self.character_width = self.font.size("a")[0]

        self.hidden = False
        self.hovered = False
        self.selected = False

        self.type = WidgetType.TEXT_INPUT

        self.render_surface()

    def render_surface(self):
        text_size = self.font.size(self.text)
        self.rect = Rect(0, 0, text_size[0] + 6, text_size[1] + 2)
        self.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.back_colour)
        pygame.draw.rect(self.surface, self.border_colour, self.rect, 2)
        self.surface.blit(self.font.render(self.text, True, self.text_colour), (4, 0))

    def frame_update(self, altered_widgets):
        self.hovered = False
        if self.rect.collidepoint(*pygame.mouse.get_pos()) and commons.first_mouse_hover:
            commons.first_mouse_hover = False
            commons.current_cursor = commons.text_input_cursor
            self.hovered = True
            if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                commons.first_mouse_action = False
                altered_widgets.append(self)

    def draw(self):
        super().draw()

        if self.selected:
            pygame.draw.rect(commons.window, (255, 255, 255), Rect(), 0)
        if self.hovered:
            pygame.draw.rect(commons.window, (128, 128, 128), self.rect, 2)
