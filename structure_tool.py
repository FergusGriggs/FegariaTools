# Pygame imports
import pygame
from pygame.locals import *

# Project imports
import commons
from base_tool import Tool
from widget import *
import game_data
import methods

class StructureEditMode(Enum):
    TILES = 0
    WALLS = 1
    CONNECTIONS = 2
    INSPECT = 3


class StructureViewMode(Enum):
    TILES = 0
    WALLS = 1
    BOTH = 2
    CONNECTIONS = 3


class StructureCreatorWidget(Widget):
    def __init__(self, columns, rows, tile_data_str, tile_draw_id_str, wall_draw_id_str, connection_draw_type, connection_draw_orientation, chest_draw_loot_id, button_size=20, min_rows=1, min_columns=1, max_rows=20, max_columns=20, view_mode_str=None, edit_mode_str=None, tile_inspect_on=True):
        super().__init__("structure_creator")

        self.type = WidgetType.STRUCTURE_CREATOR

        self.hidden = False
        self.true_hidden = self.hidden

        self.min_rows = min_rows
        self.min_columns = min_columns
        self.max_rows = max_rows
        self.max_columns = max_columns

        self.tile_size = 24

        self.view_mode = StructureViewMode.BOTH
        self.edit_mode = StructureEditMode.TILES

        if view_mode_str is not None:
            self.set_view_mode(view_mode_str, update_surf=False)
        if edit_mode_str is not None:
            self.set_edit_mode(edit_mode_str)

        self.rows = max(self.min_rows, min(self.max_rows, rows))
        self.columns = max(self.min_columns, min(self.max_columns, columns))

        self.tile_draw_id_str = tile_draw_id_str
        self.wall_draw_id_str = wall_draw_id_str
        self.connection_draw_type = connection_draw_type
        self.connection_draw_orientation = connection_draw_orientation
        self.chest_draw_loot_id = chest_draw_loot_id

        self.tile_data = []
        self.load_from_str_data(tile_data_str)

        if len(self.tile_data) == 0:
            self.generate_fresh_tile_data()
        if not self.validate_tile_data():
            self.generate_fresh_tile_data()

        self.button_size = button_size

        self.surface = None

        self.tile_hovering = (-1, -1)
        self.prev_tile_hovering = (-1, -1)
        self.hovering_a_tile = False
        self.hovering_inspect_text = False

        self.tile_inspect_on = tile_inspect_on

        self.dragging_m1_on_self = False
        self.dragging_m2_on_self = False

        self.tile_m1_just_altered = (-1, -1)
        self.tile_m2_just_altered = (-1, -1)

        self.buttons = [[Rect(0, 0, 0, 0), False] for _ in range(8)]

        self.inspect_string_surfaces = []
        self.inspect_text_height = commons.font_20.size("A")[1]

        # 0 -> add row top
        # 1 -> remove row top
        # 2 -> add row bot
        # 3 -> remove row bot
        # 4 -> add column front
        # 5 -> remove column front
        # 6 -> add column back
        # 7 -> remove column back

        self.create_surface()

    def validate_tile_data(self):
        all_valid = False

        if len(self.tile_data) == self.columns:
            all_valid = True
            for column in self.tile_data:
                if len(column) != self.rows:
                    all_valid = False
                    break

        if not all_valid:
            print("FAILURE: StructureCreatorWidget with id: " + self.widget_id + " failed to validate it's tile data")
            return False
        else:
            return True

    def create_surface(self):
        self.rect = Rect(self.rect.x, self.rect.y, self.max_columns * self.tile_size + self.button_size * 2, self.max_rows * self.tile_size + self.button_size * 2)
        self.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.surface.fill(commons.border_col)
        pygame.draw.rect(self.surface, methods.modify_col(commons.back_col, 1.2), Rect(self.button_size, self.button_size, self.rect.w - self.button_size * 2, self.rect.h - self.button_size * 2), 0)

        # Render Vertical Buttons
        vertical_button_left_surf = pygame.Surface((self.button_size, self.button_size * 1.5))
        render_accents(vertical_button_left_surf, commons.back_col)
        vertical_button_right_surf = vertical_button_left_surf.copy()
        methods.draw_arrow(vertical_button_left_surf, (self.button_size * 0.5, self.button_size * 0.75), self.button_size * 0.5, -math.pi * 0.5)
        methods.draw_arrow(vertical_button_right_surf, (self.button_size * 0.5 - 2, self.button_size * 0.75), self.button_size * 0.5, math.pi * 0.5)

        # Render Horizontal Buttons
        horizontal_button_up_surf = pygame.Surface((self.button_size * 1.5, self.button_size))
        render_accents(horizontal_button_up_surf, commons.back_col)
        horizontal_button_down_surf = horizontal_button_up_surf.copy()
        methods.draw_arrow(horizontal_button_up_surf, (self.button_size * 0.75, self.button_size * 0.5), self.button_size * 0.5, 0)
        methods.draw_arrow(horizontal_button_down_surf, (self.button_size * 0.75, self.button_size * 0.5 - 2), self.button_size * 0.5, math.pi)

        # Create button rects
        self.buttons[0][0] = Rect(self.rect.w * 0.5 - self.button_size * 1.5 - 2, 0, self.button_size * 1.5, self.button_size)
        self.buttons[1][0] = Rect(self.rect.w * 0.5 + 2, 0, self.button_size * 1.5, self.button_size)
        self.buttons[2][0] = Rect(self.rect.w * 0.5 - self.button_size * 1.5 - 2, self.rect.h - self.button_size, self.button_size * 1.5, self.button_size)
        self.buttons[3][0] = Rect(self.rect.w * 0.5 + 2, self.rect.h - self.button_size, self.button_size * 1.5, self.button_size)
        self.buttons[4][0] = Rect(0, self.rect.h * 0.5 - self.button_size * 1.5 - 2, self.button_size, self.button_size * 1.5)
        self.buttons[5][0] = Rect(0, self.rect.h * 0.5 + 2, self.button_size, self.button_size * 1.5)
        self.buttons[6][0] = Rect(self.rect.w - self.button_size, self.rect.h * 0.5 - self.button_size * 1.5 - 2, self.button_size, self.button_size * 1.5)
        self.buttons[7][0] = Rect(self.rect.w - self.button_size, self.rect.h * 0.5 + 2, self.button_size, self.button_size * 1.5)

        # Draw buttons onto surface
        self.surface.blit(horizontal_button_up_surf, (self.buttons[0][0].x, self.buttons[0][0].y))
        self.surface.blit(horizontal_button_down_surf, (self.buttons[1][0].x, self.buttons[1][0].y))

        self.surface.blit(horizontal_button_up_surf, (self.buttons[2][0].x, self.buttons[2][0].y))
        self.surface.blit(horizontal_button_down_surf, (self.buttons[3][0].x, self.buttons[3][0].y))

        self.surface.blit(vertical_button_left_surf, (self.buttons[4][0].x, self.buttons[4][0].y))
        self.surface.blit(vertical_button_right_surf, (self.buttons[5][0].x, self.buttons[5][0].y))

        self.surface.blit(vertical_button_left_surf, (self.buttons[6][0].x, self.buttons[6][0].y))
        self.surface.blit(vertical_button_right_surf, (self.buttons[7][0].x, self.buttons[7][0].y))

        self.redraw_all_tiles()

    def redraw_all_tiles(self):
        # Draw each tile
        for column_index in range(len(self.tile_data)):
            for row_index in range(len(self.tile_data[column_index])):
                self.redraw_tile_at_pos(column_index, row_index)

    def frame_update(self, altered_widgets, relative_mouse_pos):
        if not self.hidden:
            # Resize buttons
            for button_index in range(8):
                ui_container_button_rect = Rect(self.buttons[button_index][0].x + self.rect.x,
                                                self.buttons[button_index][0].y + self.rect.y,
                                                self.buttons[button_index][0].w,
                                                self.buttons[button_index][0].h)

                if commons.first_mouse_hover and ui_container_button_rect.collidepoint(*relative_mouse_pos):
                    commons.first_mouse_hover = False
                    self.buttons[button_index][1] = True
                    if commons.first_mouse_action and pygame.mouse.get_pressed()[0]:
                        commons.first_mouse_action = False
                        if button_index == 0:
                            self.modify_grid_structure(add=True, row=True, array_front=True)
                        elif button_index == 1:
                            self.modify_grid_structure(add=False, row=True, array_front=True)
                        elif button_index == 2:
                            self.modify_grid_structure(add=False, row=True, array_front=False)
                        elif button_index == 3:
                            self.modify_grid_structure(add=True, row=True, array_front=False)
                        elif button_index == 4:
                            self.modify_grid_structure(add=True, row=False, array_front=True)
                        elif button_index == 5:
                            self.modify_grid_structure(add=False, row=False, array_front=True)
                        elif button_index == 6:
                            self.modify_grid_structure(add=False, row=False, array_front=False)
                        elif button_index == 7:
                            self.modify_grid_structure(add=True, row=False, array_front=False)
                        altered_widgets.append(self)
                else:
                    self.buttons[button_index][1] = False

            # Tile Hovering
            mouse_pos_rel_to_grid = (int(relative_mouse_pos[0] - self.rect.x - self.button_size - (self.max_columns - self.columns) * self.tile_size * 0.5),
                                     int(relative_mouse_pos[1] - self.rect.y - self.button_size - (self.max_rows - self.rows) * self.tile_size * 0.5))

            self.tile_hovering = (mouse_pos_rel_to_grid[0] // self.tile_size, mouse_pos_rel_to_grid[1] // self.tile_size)

            self.hovering_a_tile = False
            if commons.first_mouse_hover:
                commons.first_mouse_hover = False

                if 0 <= self.tile_hovering[0] < self.columns:
                    if 0 <= self.tile_hovering[1] < self.rows:
                        self.hovering_a_tile = True

                        if self.prev_tile_hovering != self.tile_hovering:
                            inspect_strings = []
                            origin = (self.tile_hovering[0], self.tile_hovering[1])

                            multitile_offset = self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][1]
                            if multitile_offset is not None:
                                origin = (self.tile_hovering[0] + multitile_offset[0], self.tile_hovering[1] + multitile_offset[1])

                            tile_id = self.tile_data[origin[0]][origin[1]][0]

                            if tile_id is not None:
                                inspect_strings.append("Tile Override Id: " + tile_id)
                                multitile_origin_offset = self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][1]
                                if multitile_origin_offset is not None:
                                    inspect_strings.append("Multitile Origin Offset: (" + str(multitile_origin_offset[0]) + ", " + str(multitile_origin_offset[1]) + ")")
                                chest_loot_id = self.tile_data[origin[0]][origin[1]][2]
                                if chest_loot_id is not None:
                                    inspect_strings.append("Chest Loot Id: " + chest_loot_id)
                            wall_id = self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][3]
                            if wall_id is not None:
                                inspect_strings.append("Wall Override Id: " + wall_id)
                            connection_data = self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][4]
                            if connection_data is not None:
                                inspect_strings.append("Connection Type: " + connection_data[0])
                                inspect_strings.append("Connection Orientation: " + connection_data[1])

                            self.inspect_string_surfaces.clear()
                            for string in inspect_strings:
                                self.inspect_string_surfaces.append(commons.font_20.render(string, True, (20, 20, 20)))
                                self.inspect_string_surfaces.append(commons.font_20.render(string, True, commons.text_col))

                        self.prev_tile_hovering = tuple(self.tile_hovering)

                if self.prev_tile_hovering != self.tile_hovering:
                    self.prev_tile_hovering = tuple(self.tile_hovering)
                    self.inspect_string_surfaces.clear()

            # Hovering stats text
            if self.tile_inspect_on:
                self.hovering_inspect_text = False
                if relative_mouse_pos[1] < self.rect.y + self.button_size + self.inspect_text_height * len(self.inspect_string_surfaces) * 0.5 + self.tile_size * 0.5:
                    self.hovering_inspect_text = True

            # Tile editing
            if self.hovering_a_tile:
                if pygame.mouse.get_pressed()[0]:
                    if (commons.first_mouse_action or self.dragging_m1_on_self) and self.tile_hovering != self.tile_m1_just_altered:
                            commons.first_mouse_action = False
                            self.dragging_m1_on_self = True
                            self.tile_m1_just_altered = tuple(self.tile_hovering)
                            if self.edit_mode == StructureEditMode.TILES:
                                index = game_data.find_tile_index_by_id_str(self.tile_draw_id_str)
                                tile_dict = game_data.tile_data["tiles"]["tile"][index]
                                if "multitile" in tile_dict["@tags"]:
                                    str_dimensions = tile_dict["@multitile_dimensions"].split(",")
                                    dimensions = (int(str_dimensions[0]), int(str_dimensions[1]))

                                    if self.tile_hovering[0] + dimensions[0] <= self.columns and self.tile_hovering[1] + dimensions[1] <= self.rows:
                                        can_place_multitile = True
                                        for x_offset in range(dimensions[0]):
                                            for y_offset in range(dimensions[1]):
                                                if not (self.tile_data[self.tile_hovering[0] + x_offset][self.tile_hovering[1] + y_offset][0] is None or self.tile_data[self.tile_hovering[0] + x_offset][self.tile_hovering[1] + y_offset][0] == "fg.tile.air"):
                                                    can_place_multitile = False

                                        if can_place_multitile:
                                            for x_offset in range(dimensions[0]):
                                                for y_offset in range(dimensions[1]):
                                                    if x_offset == 0 and y_offset == 0:
                                                        self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][0] = self.tile_draw_id_str
                                                    else:
                                                        self.tile_data[self.tile_hovering[0] + x_offset][self.tile_hovering[1] + y_offset][0] = None
                                                    self.tile_data[self.tile_hovering[0] + x_offset][self.tile_hovering[1] + y_offset][1] = (-x_offset, -y_offset)
                                                    self.redraw_tile_at_pos(self.tile_hovering[0] + x_offset, self.tile_hovering[1] + y_offset)

                                            if "chest" in tile_dict["@tags"]:
                                                self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][2] = self.chest_draw_loot_id
                                else:
                                    multitile_offset = self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][1]
                                    if multitile_offset is None:
                                        self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][0] = self.tile_draw_id_str

                            elif self.edit_mode == StructureEditMode.WALLS:
                                self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][3] = self.wall_draw_id_str
                            elif self.edit_mode == StructureEditMode.CONNECTIONS:
                                if self.connection_draw_type != "":
                                    self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][4] = [self.connection_draw_type, self.connection_draw_orientation]
                            self.redraw_tile_at_pos(self.tile_hovering[0], self.tile_hovering[1])
                            self.set_ui_container_redraw_flag(True)
                            altered_widgets.append(self)

                if pygame.mouse.get_pressed()[2] and self.tile_hovering != self.tile_m2_just_altered:
                    if (commons.first_mouse_action or self.dragging_m2_on_self) and self.tile_hovering != self.tile_m2_just_altered:
                        commons.first_mouse_action = False
                        self.dragging_m2_on_self = True
                        self.tile_m2_just_altered = tuple(self.tile_hovering)

                        if self.edit_mode == StructureEditMode.TILES:
                            tile_id_str = self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][0]
                            multitile_offset = self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][1]

                            if tile_id_str is not None or multitile_offset is not None:
                                if multitile_offset is not None:
                                    origin = (self.tile_hovering[0] + multitile_offset[0], self.tile_hovering[1] + multitile_offset[1])
                                    tile_id_str = self.tile_data[origin[0]][origin[1]][0]

                                index = game_data.find_tile_index_by_id_str(tile_id_str)
                                tile_dict = game_data.tile_data["tiles"]["tile"][index]
                                if "multitile" in tile_dict["@tags"]:
                                    multitile_relative_origin = self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][1]
                                    origin = (self.tile_hovering[0] + multitile_relative_origin[0], self.tile_hovering[1] + multitile_relative_origin[1])

                                    str_dimensions = tile_dict["@multitile_dimensions"].split(",")
                                    dimensions = (int(str_dimensions[0]), int(str_dimensions[1]))

                                    for x_offset in range(dimensions[0]):
                                        for y_offset in range(dimensions[1]):
                                            self.tile_data[origin[0] + x_offset][origin[1] + y_offset][0] = None
                                            self.tile_data[origin[0] + x_offset][origin[1] + y_offset][1] = None
                                            self.redraw_tile_at_pos(origin[0] + x_offset, origin[1] + y_offset)
                                else:
                                    self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][0] = None

                        elif self.edit_mode == StructureEditMode.WALLS:
                            self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][3] = None

                        elif self.edit_mode == StructureEditMode.CONNECTIONS:
                            self.tile_data[self.tile_hovering[0]][self.tile_hovering[1]][4] = None

                        self.redraw_tile_at_pos(self.tile_hovering[0], self.tile_hovering[1])
                        self.set_ui_container_redraw_flag(True)
                        altered_widgets.append(self)

            if not pygame.mouse.get_pressed()[0]:
                self.dragging_m1_on_self = False
                self.tile_m1_just_altered = (-1, -1)

            if not pygame.mouse.get_pressed()[2]:
                self.dragging_m2_on_self = False
                self.tile_m2_just_altered = (-1, -1)

    def draw(self, relative_position, scroll_offset, container_rect):
        if not self.hidden:
            # Resize buttons
            for button_index in range(8):
                if self.buttons[button_index][1]:
                    methods.draw_rect_clipped(commons.window, commons.hover_border_col,
                                              Rect(relative_position[0] - scroll_offset[0] + self.buttons[button_index][0].x + self.rect.x,
                                                   relative_position[1] - scroll_offset[1] + self.buttons[button_index][0].y + self.rect.y,
                                                   self.buttons[button_index][0].w, self.buttons[button_index][0].h), 2,
                                              Rect(relative_position[0],
                                                   relative_position[1],
                                                   container_rect.w, container_rect.h))
            # Tile hovering
            if self.hovering_a_tile:
                tile_pos = (self.rect.w * 0.5 - self.columns * self.tile_size * 0.5 + self.tile_hovering[0] * self.tile_size, self.rect.h * 0.5 - self.rows * self.tile_size * 0.5 + self.tile_hovering[1] * self.tile_size)
                methods.draw_rect_clipped(commons.window, (0, 0, 0),
                                          Rect(relative_position[0] - scroll_offset[0] + tile_pos[0] + self.rect.x,
                                               relative_position[1] - scroll_offset[1] + tile_pos[1] + self.rect.y,
                                               self.tile_size, self.tile_size), 2,
                                          Rect(relative_position[0],
                                               relative_position[1],
                                               container_rect.w, container_rect.h))

            # Inspect text
            if self.tile_inspect_on:
                mouse_intersect_y_offset = 0
                if self.hovering_inspect_text:
                    mouse_intersect_y_offset = self.inspect_text_height * len(self.inspect_string_surfaces) * 0.5 + self.tile_size

                for inspect_string_index in range(len(self.inspect_string_surfaces)):
                    if inspect_string_index % 2 == 0:
                        offset = (1, self.inspect_text_height * (inspect_string_index // 2) + 2 + mouse_intersect_y_offset)
                    else:
                        offset = (0, self.inspect_text_height * (inspect_string_index // 2) + mouse_intersect_y_offset)

                    commons.window.blit(self.inspect_string_surfaces[inspect_string_index], (relative_position[0] - scroll_offset[0] + self.rect.x + self.button_size + offset[0],
                                                                                             relative_position[1] - scroll_offset[1] + self.rect.y + self.button_size + offset[1]))

    def redraw_tile_at_pos(self, x, y):
        pos = (self.rect.w * 0.5 - self.columns * self.tile_size * 0.5 + x * self.tile_size, self.rect.h * 0.5 - self.rows * self.tile_size * 0.5 + y * self.tile_size)
        pygame.draw.rect(self.surface, (128, 204, 234), Rect(pos[0], pos[1], self.tile_size, self.tile_size), 0)

        if self.view_mode != StructureViewMode.TILES:
            if self.tile_data[x][y][3] is not None:
                image = pygame.Surface((8, 8))
                wall_index = game_data.find_wall_index_by_id_str(self.tile_data[x][y][3])
                if wall_index != -1:
                    image = methods.safe_load_image(game_data.wall_data["walls"]["wall"][wall_index]["@image_path"]).convert()
            else:
                image = commons.structure_tool_existing_wall.copy()

            has_multitile = self.tile_data[x][y][0] is None and self.tile_data[x][y][1] is not None
            has_tile = self.tile_data[x][y][0] is not None

            if (self.view_mode == StructureViewMode.BOTH or self.view_mode == StructureViewMode.CONNECTIONS) and not (has_tile or has_multitile):
                image.blit(commons.structure_tool_wall_transparency, (0, 0))

            image.set_colorkey((255, 0, 255))
            self.surface.blit(pygame.transform.scale(image, (self.tile_size, self.tile_size)), pos)

        if self.view_mode != StructureViewMode.WALLS:
            if self.tile_data[x][y][0] is not None or self.tile_data[x][y][1] is not None:
                image = pygame.Surface((8, 8))
                id_str = self.tile_data[x][y][0]

                if self.tile_data[x][y][1] is not None:
                    origin = (x + self.tile_data[x][y][1][0], y + self.tile_data[x][y][1][1])
                    id_str = self.tile_data[origin[0]][origin[1]][0]

                tile_index = game_data.find_tile_index_by_id_str(id_str)
                if tile_index != -1:
                    tile_dict = game_data.tile_data["tiles"]["tile"][tile_index]
                    if "multitile" in tile_dict["@tags"]:
                        full_image = methods.safe_load_image(tile_dict["@multitile_image_path"]).convert()
                        image.blit(full_image, (self.tile_data[x][y][1][0] * 8, self.tile_data[x][y][1][1] * 8))
                    else:
                        image = methods.safe_load_image(tile_dict["@image_path"]).convert()
            else:
                image = commons.structure_tool_existing_tile.copy()

            if self.view_mode == StructureViewMode.BOTH or self.view_mode == StructureViewMode.CONNECTIONS:
                image.blit(commons.structure_tool_tile_transparency, (0, 0))

            image.set_colorkey((255, 0, 255))
            self.surface.blit(pygame.transform.scale(image, (self.tile_size, self.tile_size)), pos)

        if self.view_mode == StructureViewMode.CONNECTIONS:
            if self.tile_data[x][y][4] is not None:
                connection_surf = commons.structure_tool_connection.copy()
                angle = 0
                if self.tile_data[x][y][4][1] == "Right":
                    angle = -90
                elif self.tile_data[x][y][4][1] == "Down":
                    angle = 180
                elif self.tile_data[x][y][4][1] == "Left":
                    angle = 90

                connection_surf = pygame.transform.rotate(connection_surf, angle)
                self.surface.blit(pygame.transform.scale(connection_surf, (self.tile_size, self.tile_size)), pos)

    def get_default_tile_data(self):
        #    Tile Id, Multitile offset, Chest Loot Id, Wall Id, Connection Data
        return [None,             None,          None,    None, None]

    def generate_fresh_tile_data(self):
        self.rows = self.min_rows
        self.columns = self.min_columns

        self.tile_data = [[self.get_default_tile_data() for _ in range(self.rows)] for _ in range(self.columns)]

    def modify_grid_structure(self, add=True, row=True, array_front=True):
        if row:
            if array_front:
                if add:
                    if self.rows < self.max_rows:
                        for tile_index in range(len(self.tile_data)):
                            self.tile_data[tile_index].insert(0, self.get_default_tile_data())
                        self.rows += 1
                else:
                    if self.rows > self.min_rows:
                        for tile_index in range(len(self.tile_data)):
                            del self.tile_data[tile_index][0]
                        self.rows -= 1
            else:
                if add:
                    if self.rows < self.max_rows:
                        for tile_index in range(len(self.tile_data)):
                            self.tile_data[tile_index].append(self.get_default_tile_data())
                        self.rows += 1
                else:
                    if self.rows > self.min_rows:
                        for tile_index in range(len(self.tile_data)):
                            del self.tile_data[tile_index][self.rows - 1]
                        self.rows -= 1
        else:
            if array_front:
                if add:
                    if self.columns < self.max_columns:
                        self.tile_data.insert(0, [self.get_default_tile_data() for _ in range(self.rows)])
                        self.columns += 1
                else:
                    if self.columns > self.min_columns:
                        del self.tile_data[0]
                        self.columns -= 1
            else:
                if add:
                    if self.columns < self.max_columns:
                        self.tile_data.append([self.get_default_tile_data() for _ in range(self.rows)])
                        self.columns += 1
                else:
                    if self.columns > self.min_columns:
                        del self.tile_data[self.columns - 1]
                        self.columns -= 1

        self.create_surface()
        self.set_ui_container_update_flag(True)

    def set_tile_draw_id_str(self, tile_draw_id_str):
        self.tile_draw_id_str = tile_draw_id_str

    def set_wall_draw_id_str(self, wall_draw_id_str):
        self.wall_draw_id_str = wall_draw_id_str

    def set_connection_draw_orientation(self, connection_draw_orientation):
        self.connection_draw_orientation = connection_draw_orientation

    def set_connection_draw_type(self, connection_draw_type):
        self.connection_draw_type = connection_draw_type

    def set_tile_inspect_on(self, tile_inspect_on):
        self.tile_inspect_on = tile_inspect_on

    def set_chest_draw_loot_id(self, chest_draw_loot_id):
        self.chest_draw_loot_id = chest_draw_loot_id

    def set_view_mode(self, view_mode_str, update_surf=True):
        if view_mode_str == "Tiles":
            self.view_mode = StructureViewMode.TILES
        elif view_mode_str == "Walls":
            self.view_mode = StructureViewMode.WALLS
        elif view_mode_str == "Tiles & Walls":
            self.view_mode = StructureViewMode.BOTH
        elif view_mode_str == "Tiles, Walls & Extras":
            self.view_mode = StructureViewMode.CONNECTIONS

        if update_surf:
            self.redraw_all_tiles()
            self.set_ui_container_redraw_flag(True)

    def set_edit_mode(self, edit_mode_str):
        if edit_mode_str == "Tiles":
            self.edit_mode = StructureEditMode.TILES
        elif edit_mode_str == "Walls":
            self.edit_mode = StructureEditMode.WALLS
        elif edit_mode_str == "Connections":
            self.edit_mode = StructureEditMode.CONNECTIONS

    def compute_str_data(self):
        out_string = ""
        for column_index in range(self.columns):
            for row_index in range(self.rows):
                if self.tile_data[column_index][row_index] == self.get_default_tile_data():
                    out_string += "-"
                else:
                    out_string += "["
                    tile_dat = self.tile_data[column_index][row_index]
                    for tile_index in range(len(tile_dat)):
                        if tile_dat[tile_index] is not None:
                            out_string += str(tile_index)
                            out_string += ":"
                            # Tile override
                            if tile_index == 0:
                                out_string += tile_dat[0]
                            # Multitile offset
                            elif tile_index == 1:
                                out_string += str(tile_dat[1][0]) + "," + str(tile_dat[1][1])
                            # Chest loot id
                            elif tile_index == 2:
                                out_string += tile_dat[2]
                            # Wall override
                            elif tile_index == 3:
                                out_string += tile_dat[3]
                            # Connection data
                            elif tile_index == 4:
                                out_string += tile_dat[4][0] + "," + tile_dat[4][1]
                            out_string += ";"
                    out_string = out_string[:-1]
                    out_string += "]"
            if column_index < self.columns - 1:
                out_string += "|"
        return out_string

    def load_from_str_data(self, str_data):
        if str_data is None or len(str_data) == 0:
            return
        self.tile_data.clear()
        columns = str_data.split("|")
        for column in columns:
            self.tile_data.append([])
            char_index = 0
            while char_index < len(column):
                self.tile_data[-1].append(self.get_default_tile_data())
                if column[char_index] != "-":
                    end_index = methods.find_next_char_in_string(column, "]", char_index)
                    if end_index != -1:
                        tile_data_string = column[char_index + 1:end_index]
                        char_index = end_index
                        data_strs = tile_data_string.split(";")
                        for data_str in data_strs:
                            data_str_split = data_str.split(":")
                            data_str_id = int(data_str_split[0])
                            if data_str_id == 0:
                                self.tile_data[-1][-1][data_str_id] = data_str_split[1]
                            elif data_str_id == 2:
                                self.tile_data[-1][-1][data_str_id] = data_str_split[1]
                            elif data_str_id == 3:
                                self.tile_data[-1][-1][data_str_id] =data_str_split[1]
                            if data_str_id == 1:
                                split_str = data_str_split[1].split(",")
                                self.tile_data[-1][-1][data_str_id] = (int(split_str[0]), int(split_str[1]))
                            if data_str_id == 4:
                                self.tile_data[-1][-1][data_str_id] = data_str_split[1].split(",")
                char_index += 1


class StructureTool(Tool):
    def __init__(self):
        super().__init__()

        self.name = "Structure Tool"
        self.entity_type = "Structure"
        self.xml_group_name = "structures"
        self.xml_type_name = "structure"

        self.set_xml_data_root()

        self.icon = commons.st_icon_small
        self.accent_col = commons.structure_tool_col

        self.basic_properties_collapsed = False
        self.structure_creation_collapsed = False

        self.current_edit_mode = "Tiles"
        self.current_tile = "fg.tile.stone"
        self.current_wall = "fg.wall.dirt"
        self.current_view_mode = "Tiles, Walls & Extras"
        self.current_connection_type = ""
        self.current_connection_orientation = "Up"
        self.current_chest_loot_id = "fg.loot.chest_wood"
        self.tile_inspect_on = True

        super().init()

    def set_xml_data_root(self):
        self.xml_data_root = game_data.structure_data

    def export_tool_data(self):
        game_data.save_structure_data()

    def reload_tool_data(self):
        game_data.load_structure_data()

    def widget_altered(self, widget):
        if widget.type == WidgetType.BEGIN_COLLAPSE:
            if widget.widget_id == "structure_basic_properties":
                self.basic_properties_collapsed = widget.collapsed

            elif widget.widget_id == "structure_creation_collapse":
                self.structure_creation_collapsed = widget.collapsed

        elif widget.type == WidgetType.DROP_DOWN:
            if widget.widget_id == "selected_tile":
                structure_creator = self.find_container("entity_properties").find_widget("structure_creator")
                structure_creator.set_tile_draw_id_str(widget.selected_string)
                self.current_tile = widget.selected_string
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id == "selected_wall":
                structure_creator = self.find_container("entity_properties").find_widget("structure_creator")
                structure_creator.set_wall_draw_id_str(widget.selected_string)
                self.current_wall = widget.selected_string

            elif widget.widget_id == "connection_orientation":
                structure_creator = self.find_container("entity_properties").find_widget("structure_creator")
                structure_creator.set_connection_draw_orientation(widget.selected_string)
                self.current_connection_orientation = widget.selected_string

            elif widget.widget_id == "view_mode":
                self.current_view_mode = widget.selected_string
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id == "edit_mode":
                self.current_edit_mode = widget.selected_string
                self.load_property_page_for_entity(self.current_entity)

            elif widget.widget_id == "chest_loot_id":
                structure_creator = self.find_container("entity_properties").find_widget("structure_creator")
                structure_creator.set_chest_draw_loot_id(widget.selected_string)
                self.current_chest_loot_id = widget.selected_string

        elif widget.type == WidgetType.TEXT_INPUT:
            if widget.widget_id == "structure_name":
                self.current_entity["@name"] = widget.text

            elif widget.widget_id == "structure_id_str":
                self.current_entity["@id_str"] = "fg.structure." + widget.text
                self.update_entity_list()
                self.reselect_current_entity()

            elif widget.widget_id == "structure_spawn_weight":
                self.current_entity["@spawn_weight"] = widget.text

            elif widget.widget_id == "connection_type":
                structure_creator = self.find_container("entity_properties").find_widget("structure_creator")
                structure_creator.set_connection_draw_type(widget.text)
                self.current_connection_type = widget.text

        elif widget.type == WidgetType.STRUCTURE_CREATOR:
            self.current_entity["@width"] = str(widget.columns)
            self.current_entity["@height"] = str(widget.rows)
            self.current_entity["@tile_data"] = widget.compute_str_data()

        elif widget.type == WidgetType.CHECKBOX:
            if widget.widget_id == "tile_inspect_on":
                structure_creator = self.find_container("entity_properties").find_widget("structure_creator")
                structure_creator.set_tile_inspect_on(widget.checked)
                self.tile_inspect_on = widget.checked

        super().widget_altered(widget)

    def load_property_page_for_entity(self, entity):
        structure_properties = self.find_container("entity_properties")
        structure_properties.widgets.clear()

        # Basic properties
        structure_properties.add_widget(BeginCollapseWidget("structure_basic_properties", "Basic Properties", collapsed=self.basic_properties_collapsed))

        # Numerical Id
        structure_properties.add_widget(TextWidget("structure_id", "Id: " + entity["@id"]))

        # Name
        structure_properties.add_widget(TextWidget("structure_name_text", "Name:"))
        structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        structure_properties.add_widget(TextInputWidget("structure_name", entity["@name"], TextInputType.STRING))

        # String Id
        structure_properties.add_widget(TextWidget("structure_id_str_text", "Id Str:"))

        structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset - commons.font_20.size("fg.structure.")[0]))
        structure_properties.add_widget(TextWidget("structure_id_str_text_pre", "fg.structure.", commons.selected_border_col))
        structure_properties.add_widget(SameLineWidget(0))
        structure_properties.add_widget(TextInputWidget("structure_id_str", entity["@id_str"].split(".")[-1], TextInputType.STRING))

        # Spawn Weight
        structure_properties.add_widget(TextWidget("structure_spawn_weight_text", "Spawn Weight:"))
        structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        structure_properties.add_widget(TextInputWidget("structure_spawn_weight", entity["@spawn_weight"], TextInputType.INT))

        structure_properties.add_widget(EndCollapseWidget())

        # Structure creation
        structure_properties.add_widget(BeginCollapseWidget("structure_creation_collapse", "Structure Creation", collapsed=self.structure_creation_collapsed))

        # View Mode
        structure_properties.add_widget(TextWidget("view_mode_text", "View Mode:"))
        structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        structure_properties.add_widget(DropDownWidget("view_mode", ["Tiles", "Walls", "Tiles & Walls", "Tiles, Walls & Extras"], DropDownType.SELECT, initial_string=self.current_view_mode))

        # Edit Mode
        structure_properties.add_widget(TextWidget("edit_mode_text", "Edit Mode:"))
        structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        structure_properties.add_widget(DropDownWidget("edit_mode", ["Tiles", "Walls", "Connections"], DropDownType.SELECT, initial_string=self.current_edit_mode))

        if self.current_edit_mode == "Tiles":
            # Selected Tile
            structure_properties.add_widget(TextWidget("selected_tile_text", "Selected Tile:"))
            structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            structure_properties.add_widget(DropDownWidget("selected_tile", game_data.tile_id_strs, DropDownType.SELECT, initial_string=self.current_tile))

        elif self.current_edit_mode == "Walls":
            # Selected Wall
            structure_properties.add_widget(TextWidget("selected_wall_text", "Selected Wall:"))
            structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            structure_properties.add_widget(DropDownWidget("selected_wall", game_data.wall_id_strs, DropDownType.SELECT, initial_string=self.current_wall))

        elif self.current_edit_mode == "Connections":
            # Connection Type
            structure_properties.add_widget(TextWidget("connection_type_text", "Connection Type:"))
            structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            structure_properties.add_widget(TextInputWidget("connection_type", self.current_connection_type, TextInputType.STRING))

            # Connection Orientation
            structure_properties.add_widget(TextWidget("connection_orientation_text", "Connection Orientation:"))
            structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            structure_properties.add_widget(DropDownWidget("connection_orientation", ["Up", "Right", "Down", "Left"], DropDownType.SELECT, initial_string=self.current_connection_orientation))

        tile_index = game_data.find_tile_index_by_id_str(self.current_tile)
        if self.current_edit_mode == "Tiles" and "chest" in game_data.tile_data["tiles"]["tile"][tile_index]["@tags"]:
            # Chest Loot Id
            structure_properties.add_widget(TextWidget("chest_loot_id_text", "Chest Loot Id Str:"))
            structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            structure_properties.add_widget(DropDownWidget("chest_loot_id", game_data.loot_id_strs, DropDownType.SELECT, initial_string=self.current_chest_loot_id))

        # Edit Mode
        structure_properties.add_widget(TextWidget("tile_inspect_on_text", "Tile inspect on:"))
        structure_properties.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
        structure_properties.add_widget(CheckboxWidget("tile_inspect_on", checked=self.tile_inspect_on))

        structure_properties.add_widget(StructureCreatorWidget(int(entity["@width"]), int(entity["@height"]), entity["@tile_data"], self.current_tile, self.current_wall, self.current_connection_type, self.current_connection_orientation, self.current_chest_loot_id, view_mode_str=self.current_view_mode, edit_mode_str=self.current_edit_mode, tile_inspect_on=self.tile_inspect_on))

        structure_properties.add_widget(EndCollapseWidget())

        structure_properties.update(None)

    def get_default_entity_dict(self):
        entity_dict = super().get_default_entity_dict()

        entity_dict["@name"] = "UNNAMED"
        entity_dict["@width"] = "4"
        entity_dict["@height"] = "4"
        entity_dict["@spawn_weight"] = "100"
        entity_dict["@tile_data"] = ""

        return entity_dict
