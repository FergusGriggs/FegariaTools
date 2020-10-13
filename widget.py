# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
import methods

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
        self.max_horizontal = 0
        self.vertical = 0
        self.line_height = 0
        self.new_line = False
        self.space_width = 0


class Widget:
    def __init__(self, widget_id):
        self.widget_id = widget_id
        self.type = WidgetType.BASE
        self.surface = None
        self.rect = Rect(0, 0, 0, 0)
        self.hidden = True

    def update_position(self, container_rect, offset_data):
        if not self.hidden:
            if offset_data.new_line:
                if offset_data.horizontal > offset_data.max_horizontal:
                    offset_data.max_horizontal = offset_data.horizontal
                offset_data.horizontal = offset_data.space_width
                offset_data.vertical += offset_data.line_height + 2
                offset_data.line_height = 0
            else:
                offset_data.new_line = True
                offset_data.horizontal += offset_data.space_width

            self.rect.x = 5 + offset_data.horizontal
            self.rect.y = 2 + offset_data.vertical

            offset_data.horizontal += self.rect.w
            offset_data.space_width = 0

            if self.rect.h > offset_data.line_height:
                offset_data.line_height = self.rect.h

        elif offset_data.new_line is False:
            offset_data.new_line = True
            offset_data.space_width = 0

    def frame_update(self, altered_widgets, relative_mouse_pos):
        pass

    def draw(self, relative_position, scroll_offset, container_rect):
        pass

    def render_to_surface(self, surface):
        if not self.hidden:
            surface.blit(self.surface, (self.rect.x, self.rect.y))

    def process_event(self, event):
        return False

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def toggle_hidden(self):
        self.hidden = not self.hidden


class ImageWidget(Widget):
    def __init__(self, widget_id, image=commons.placeholder_image, colour_key=commons.colour_key_col,
                 image_scale=1.0):
        super().__init__(widget_id)

        self.type = WidgetType.IMAGE
        self.initial_surface = image
        self.surface = self.initial_surface
        self.image_scale = 1.0
        self.rect = self.surface.get_rect()
        self.hidden = False
        self.loaded = self.initial_surface != commons.placeholder_image
        self.colour_key = colour_key
        self.surface.set_colorkey(self.colour_key)
        self.update_image_scale(image_scale)

    def set_image(self, image, image_scale=1.0):
        self.initial_surface = image
        self.surface = self.initial_surface
        self.image_scale = 1.0
        self.loaded = self.initial_surface != commons.placeholder_image
        self.surface.set_colorkey(self.colour_key)
        self.update_image_scale(image_scale)

    def update_image_scale(self, image_scale):
        if not self.loaded:
            image_scale = 1.0

        if self.image_scale != image_scale:
            self.image_scale = image_scale
            self.surface = pygame.transform.scale(self.initial_surface, (int(self.image_scale * self.initial_surface.get_width()),
                                                                 int(self.image_scale * self.initial_surface.get_height())))
        self.rect.w = self.surface.get_width()
        self.rect.h = self.surface.get_height()

    def toggle_colourkey(self):
        if self.surface.get_colorkey() is None:
            self.surface.set_colorkey(self.colour_key)
        else:
            self.surface.set_colorkey(None)


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
    def __init__(self, widget_id, size=20):
        super().__init__(widget_id)

        self.type = WidgetType.CHECKBOX
        self.rect = Rect(0, 0, size, size)
        self.surface = pygame.Surface((size, size))
        self.surface.fill((255, 0, 255))
        self.surface.set_colorkey((255, 0, 255))

        self.size = size
        self.checked = False
        self.hidden = False
        self.hovered = False

    def frame_update(self, altered_widgets, relative_mouse_pos):
        if not self.hidden:
            self.hovered = False
            if commons.first_mouse_hover and self.rect.collidepoint(*relative_mouse_pos):
                self.hovered = True
                commons.first_mouse_hover = False
                commons.current_cursor = commons.long_boi_cursor
                if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                    commons.first_mouse_action = False
                    self.checked = not self.checked
                    altered_widgets.append(self)

    def draw(self, relative_position, scroll_offset, container_rect):
        if not self.hidden:
            colour = commons.text_col
            if self.hovered:
                colour = commons.selected_border_col
            # pygame.draw.circle(commons.window, colour,
            #                    (relative_position[0] + self.rect.centerx,
            #                    relative_position[1] + self.rect.centery + 4),
            #                    int(self.size * 0.5), 2)
            methods.draw_rect_clipped(commons.window, colour,
                                      Rect(relative_position[0] - scroll_offset[0] + self.rect.x,
                                           relative_position[1] - scroll_offset[1] + self.rect.y + 3,
                                           self.rect.w, self.rect.h), 2,
                                      Rect(relative_position[0],
                                           relative_position[1],
                                           container_rect.w, container_rect.h))
            if self.checked:
                # pygame.draw.circle(commons.window, colour,
                #                    (relative_position[0] + self.rect.centerx,
                #                     relative_position[1] + self.rect.centery + 4),
                #                    int(self.size * 0.2), 0)
                methods.draw_rect_clipped(commons.window, colour,
                                          Rect(relative_position[0] - scroll_offset[0] + self.rect.x + 5,
                                               relative_position[1] - scroll_offset[1] + self.rect.y + 5 + 3,
                                               self.rect.w - 9, self.rect.h - 10), 0,
                                          Rect(relative_position[0],
                                               relative_position[1],
                                               container_rect.w, container_rect.h))


class LineSelectorWidget(Widget):
    def __init__(self, widget_id):
        super().__init__(widget_id)

        self.type = WidgetType.LINE_SELECTOR
        self.rect = Rect(0, 0, 0, 0)
        self.selected = False
        self.hovered = False

    def update_position(self, container_rect, offset_data):
        self.rect = Rect(-5, offset_data.vertical, commons.screen_w, offset_data.line_height)

    def frame_update(self, altered_widgets, relative_mouse_pos):
        self.hovered = False
        if self.rect.collidepoint(*relative_mouse_pos) and commons.first_mouse_hover:
            commons.first_mouse_hover = False
            commons.current_cursor = commons.button_cursor
            self.hovered = True
            if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                commons.first_mouse_action = False
                altered_widgets.append(self)

    def draw(self, relative_position, scroll_offset, container_rect):
        if self.selected or self.hovered:
            colour = commons.hover_border_col
            if self.selected:
                colour = commons.selected_border_col
            methods.draw_rect_clipped(commons.window, colour,
                                      Rect(relative_position[0] - scroll_offset[0] + self.rect.x,
                                           relative_position[1] - scroll_offset[1] + self.rect.y,
                                           self.rect.w, self.rect.h), 2,
                                      Rect(relative_position[0],
                                           relative_position[1],
                                           container_rect.w, container_rect.h))


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

    def frame_update(self, altered_widgets, relative_mouse_pos):
        self.hovered = False
        if self.rect.collidepoint(*relative_mouse_pos) and commons.first_mouse_hover:
            commons.first_mouse_hover = False
            commons.current_cursor = commons.button_cursor
            self.hovered = True
            if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                commons.first_mouse_action = False
                altered_widgets.append(self)

    def draw(self, relative_position, scroll_offset, container_rect):
        if self.hovered:
            methods.draw_rect_clipped(commons.window, commons.hover_border_col,
                                      Rect(relative_position[0] - scroll_offset[0] + self.rect.x,
                                           relative_position[1] - scroll_offset[1] + self.rect.y,
                                           self.rect.w, self.rect.h), 2,
                                      Rect(relative_position[0],
                                           relative_position[1],
                                           container_rect.w, container_rect.h))


class TextInputType(Enum):
    STRING = 0
    FLOAT = 1
    INT = 2


class TextInputWidget(Widget):
    def __init__(self, widget_id, initial_text, input_type, font=None, text_colour=commons.text_col,
                 back_colour=commons.back_col, border_colour=commons.border_col, max_value=None, min_value=None,
                 max_length=None):
        super().__init__(widget_id)

        self.text = initial_text
        self.input_type = input_type
        self.font = font
        if self.font is None:
            self.font = commons.font_20
        self.text_colour = text_colour
        self.back_colour = back_colour
        self.border_colour = border_colour

        self.selected_char_index = 0
        self.selected_char_offset = 0

        self.max_length = max_length
        self.max_value = max_value
        self.min_value = min_value

        self.hidden = False
        self.hovered = False
        self.selected = False
        self.deselect_next_frame = False
        self.text_changed = False

        self.cursor_blink_progress = 0.0
        self.cursor_blink_delay = 0.5
        self.cursor_blinking = False

        self.type = WidgetType.TEXT_INPUT

        self.min_widget_size = 250
        if self.max_length is not None:
            self.min_widget_size = self.font.size("a")[0] * self.max_length + 6

        self.render_surface()

    def render_surface(self):
        text_size = self.font.size(self.text)
        self.rect.w = max(self.min_widget_size, text_size[0] + 6)
        self.rect.h = text_size[1] + 2
        self.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.surface.fill(self.back_colour)
        pygame.draw.rect(self.surface, self.border_colour, Rect(0, 0, self.rect.w, self.rect.h), 2)
        self.surface.blit(self.font.render(self.text, True, self.text_colour), (4, 0))

    def frame_update(self, altered_widgets, relative_mouse_pos):
        self.hovered = False
        should_deselect = False
        if self.rect.collidepoint(*relative_mouse_pos) and commons.first_mouse_hover:
            commons.first_mouse_hover = False
            commons.current_cursor = commons.text_input_cursor
            self.hovered = True
            if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                commons.first_mouse_action = False
                self.select(relative_mouse_pos)
        elif self.selected and pygame.mouse.get_pressed()[0]:
            should_deselect = True

        if self.deselect_next_frame or should_deselect:
            self.selected = False
            self.deselect_next_frame = False

            if self.text_changed:
                self.text_changed = False
                self.clean_text()
                self.render_surface()
                altered_widgets.append(self)

        if self.selected:
            self.cursor_blink_progress += commons.delta_time
            if self.cursor_blink_progress > self.cursor_blink_delay:
                self.cursor_blink_progress -= self.cursor_blink_delay
                self.cursor_blinking = not self.cursor_blinking

    def select(self, relative_mouse_pos):
        self.selected = True
        self.reset_cursor_blink()
        mouse_offset = relative_mouse_pos[0] - self.rect.x
        self.selected_char_index = methods.get_char_index(self.text, self.font, mouse_offset)
        self.selected_char_offset = methods.get_size_up_to_char_index(self.text, self.font, self.selected_char_index)

    def reset_cursor_blink(self):
        self.cursor_blinking = False
        self.cursor_blink_progress = -0.5

    def draw(self, relative_position, scroll_offset, container_rect):
        if self.selected and not self.cursor_blinking:
            methods.draw_rect_clipped(commons.window, (255, 255, 255),
                                      Rect(relative_position[0] - scroll_offset[0] + self.rect.x + self.selected_char_offset + 4,
                                           relative_position[1] - scroll_offset[1] + self.rect.y + 3, 2, self.rect.h - 6), 0,
                                      Rect(relative_position[0],
                                           relative_position[1],
                                           container_rect.w, container_rect.h))
        if self.hovered or self.selected:
            colour = commons.hover_border_col
            if self.selected:
                colour = commons.selected_border_col
            methods.draw_rect_clipped(commons.window, colour,
                                      Rect(relative_position[0] - scroll_offset[0] + self.rect.x,
                                           relative_position[1] - scroll_offset[1] + self.rect.y,
                                           self.rect.w, self.rect.h), 2,
                                      Rect(relative_position[0],
                                           relative_position[1],
                                           container_rect.w, container_rect.h))

    def clean_text(self):
        if self.input_type == TextInputType.FLOAT or self.input_type == TextInputType.INT:
            if len(self.text) == 0:
                self.text = "0"
        if self.input_type == TextInputType.FLOAT:
            float_val = float(self.text)
            float_val = self.clamp_numeric_value(float_val)
            self.text = str(float_val)
        elif self.input_type == TextInputType.INT:
            int_val = int(self.text)
            int_val = self.clamp_numeric_value(int_val)
            self.text = str(int_val)

    def clamp_numeric_value(self, value):
        if self.min_value is not None:
            value = max(self.min_value, value)
        if self.max_value is not None:
            value = min(self.max_value, value)
        return value

    def process_event(self, event):
        surface_needs_update = False
        if self.selected:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.selected_char_index > 0:
                        self.text = self.text[:self.selected_char_index - 1] + self.text[self.selected_char_index:]
                        self.selected_char_index -= 1
                        self.selected_char_offset = methods.get_size_up_to_char_index(self.text, self.font,
                                                                                      self.selected_char_index)
                        self.text_changed = True
                        self.render_surface()
                        surface_needs_update = True
                elif event.key == pygame.K_LEFT:
                    if self.selected_char_index > 0:
                        self.selected_char_index -= 1
                        self.selected_char_offset = methods.get_size_up_to_char_index(self.text, self.font,
                                                                                  self.selected_char_index)
                        self.reset_cursor_blink()
                elif event.key == pygame.K_RIGHT:
                    if self.selected_char_index < len(self.text):
                        self.selected_char_index += 1
                        self.selected_char_offset = methods.get_size_up_to_char_index(self.text, self.font,
                                                                                      self.selected_char_index)
                        self.reset_cursor_blink()
                elif event.key == pygame.K_RETURN:
                    self.deselect_next_frame = True
                else:
                    new_char = methods.str_from_key_event(event)
                    # Only allow minus at the start of numeric input
                    if self.input_type == TextInputType.FLOAT or self.input_type == TextInputType.INT:
                        if new_char == '-' and self.selected_char_index != 0:
                            new_char = None

                    # Remove if it's not a numeric char when necessary
                    if self.input_type == TextInputType.FLOAT:
                        new_char = methods.limit_to_numeric_chars(new_char, True)
                        if new_char == '.' and '.' in self.text:
                            new_char = None

                    elif self.input_type == TextInputType.INT:
                        new_char = methods.limit_to_numeric_chars(new_char, False)

                    # Check the string is not at max length
                    if self.max_length is not None and len(self.text) == self.max_length:
                        new_char = None

                    # Add the validated char
                    if new_char is not None:
                        self.text = self.text[:self.selected_char_index] + new_char + self.text[self.selected_char_index:]
                        self.selected_char_index += 1
                        self.selected_char_offset = methods.get_size_up_to_char_index(self.text, self.font,
                                                                                      self.selected_char_index)
                        self.text_changed = True
                        self.render_surface()
                        surface_needs_update = True

        return surface_needs_update
