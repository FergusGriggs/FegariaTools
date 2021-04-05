from widget import *
from ui_container import UiContainer, SplitType, SortType
import commons
import webbrowser
import game_data

class WidgetTest:
    def __init__(self):
        self.test_type = "text"

        self.main_window = UiContainer("window", Rect(0, 0, commons.screen_w, commons.screen_h), None)

        self.main_window.add_split(SplitType.HORIZONTAL, 10, True, "left_container", "right_container")

        right_container = self.main_window.find_container("right_container")
        right_container.set_padding(left=20, top=20, right=20, bot=20)
        right_container.set_padding_shadow(left=True, top=True, right=True, bot=True)
        right_container.make_scrollable(x=True, y=True)

        left_container = self.main_window.find_container("left_container")
        left_container.set_padding(left=10, top=10, right=10, bot=10)
        left_container.set_padding_shadow(left=True, top=True, bot=True)
        left_container.make_scrollable(x=True, y=True)

        # CheckBox + Button = 0
        # Text input        = 1
        # Drop Down         = 2
        # Text              = 3
        # Collapse          = 4

        showcase = 2

        if showcase == 0:
            for index in range(20):
                left_container.add_widget(CheckboxWidget("checkbox_" + str(index) + "_0"))
                left_container.add_widget(SameLineWidget(5))
                left_container.add_widget(CheckboxWidget("checkbox_" + str(index) + "_1"))
                left_container.add_widget(SameLineWidget(5))
                left_container.add_widget(CheckboxWidget("checkbox_" + str(index) + "_2"))
                left_container.add_widget(SameLineWidget(5))
                left_container.add_widget(CheckboxWidget("checkbox_" + str(index) + "_3"))

            right_container.add_widget(TextWidget("title_text", "Row selection toggle buttons"))

            right_container.add_widget(ButtonWidget("row_select_0", "Toggle row 0"))
            right_container.add_widget(ButtonWidget("row_select_1", "Toggle row 1"))
            right_container.add_widget(ButtonWidget("row_select_2", "Toggle row 2"))
            right_container.add_widget(ButtonWidget("row_select_3", "Toggle row 3"))

            right_container.add_widget(ButtonWidget("lol_button", "Give user £1,000,000"))

            right_container.add_widget(TextWidget("line_selector_test_text", "This line is clickable"))
            right_container.add_widget(LineSelectorWidget("line_selector_test"))

            right_container.add_widget(ImageWidget("test_image", methods.safe_load_image("res/images/tool_ui/widget_test/ainsley 1.jpg")))

            right_container.add_widget(ButtonWidget("hide_ainsley", "Hide/Show Ainsley Harriot"))

        elif showcase == 1:
            right_container.add_widget(TextWidget("text_0", "String input"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(TextInputWidget("text_input_0", "", TextInputType.STRING))

            right_container.add_widget(TextWidget("text_1", "String input"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(TextInputWidget("text_input_1", "This one has initial text", TextInputType.STRING))

            right_container.add_widget(TextWidget("text_2", "Int input"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(TextInputWidget("text_input_2", "1337", TextInputType.INT))

            right_container.add_widget(TextWidget("text_3", "Float input"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(TextInputWidget("text_input_3", "3.141592", TextInputType.FLOAT))

            right_container.add_widget(TextWidget("text_4", "Int tuple input"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(TextInputWidget("text_input_4", "69,420", TextInputType.INT_TUPLE))

            right_container.add_widget(TextWidget("text_5", "Float tuple input"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(TextInputWidget("text_input_5", "3.14,2.78", TextInputType.FLOAT_TUPLE))

            left_container.add_widget(ButtonWidget("lol_button", "Ignore this pls"))

        elif showcase == 2:
            right_container.add_widget(TextWidget("text_0", "Item instance select:"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(DropDownWidget("drop_down_0", game_data.item_id_strs, drop_down_type=DropDownType.SELECT, initial_string="fg.item.dirt"))

            right_container.add_widget(TextWidget("text_1", "Item instance multi-select:"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(DropDownWidget("drop_down_1", game_data.item_id_strs, drop_down_type=DropDownType.MULTISELECT, initial_strings=["fg.item.dirt"]))

            right_container.add_widget(TextWidget("text_2", "Drop down menu:"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(DropDownWidget("drop_down_2", ["Menu Option 1", "Menu Option 2", "Menu Option 3", "Menu Option 4"], drop_down_type=DropDownType.MENU, initial_string="Menu Example", min_widget_length=0, element_icons=[commons.new_icon, commons.save_icon, commons.copy_icon, commons.load_icon]))

            right_container.add_widget(TextWidget("text_3", "Ainsley Picture Select"))
            right_container.add_widget(SameLineFillToLineWidget(commons.property_value_pixel_offset))
            right_container.add_widget(DropDownWidget("drop_down_3", ["Ainsley Picture 1", "Ainsley Picture 2", "Ainsley Picture 3", "Mystery Image"], drop_down_type=DropDownType.SELECT, initial_string="Ainsley Picture 1", min_widget_length=0, element_icons=[commons.image_icon, commons.image_icon, commons.image_icon, commons.question_icon]))

            right_container.add_widget(ImageWidget("ainsley", methods.safe_load_image("res/images/tool_ui/widget_test/ainsley 1.jpg")))

        elif showcase == 3:
            for index in range(100):
                left_container.add_widget(TextWidget("test_widget_" + str(index), "list item " + str(index)))

            right_container.add_widget(TextWidget("test_widget_0", "Big White Text", font=commons.font_50))
            right_container.add_widget(TextWidget("test_widget_1", "Medium Red Text", colour=(200, 50, 50), font=commons.font_30))
            right_container.add_widget(TextWidget("test_widget_2", "Small Green Text", colour=(50, 200, 50)))

            right_container.add_widget(ImageWidget("test_image", methods.safe_load_image("res/images/tool_ui/widget_test/ainsley 1.jpg")))

            long_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
            long_text_2 = "There is a lot of text in this box and it will wrap when the ui container it is in gets to small to display it on one line. Wow! Look at it jump around, trying to fit into this box. Blah, Blah, Blah, Blah, Blah, Blah, Blah, Blah, Blah, Blah, Blah, Blah."

            right_container.add_widget(WrappedTextWidget("wrapped_test_widget", long_text_2))

        elif showcase == 4:
            right_container.add_widget(BeginCollapseWidget("collapse_0", "Important collection"))

            right_container.add_widget(BeginCollapseWidget("collapse_1", "Important Thing 1"))
            right_container.add_widget(TextWidget("chicken_text_0", "Picture of a chicken (for Colosson)"))
            right_container.add_widget(ImageWidget("picture_of_a_chicken", methods.safe_load_image("res/images/tool_ui/widget_test/picture_of_a_chicken.jpg")))
            right_container.add_widget(EndCollapseWidget())

            right_container.add_widget(BeginCollapseWidget("collapse_2", "Important Thing 2"))
            right_container.add_widget(TextWidget("chicken_text_1", "Backup picture of a chicken (also for Colosson)"))
            right_container.add_widget(ImageWidget("second_picture_of_a_chicken", methods.safe_load_image("res/images/tool_ui/widget_test/second_picture_of_a_chicken.jpg")))
            right_container.add_widget(EndCollapseWidget())

            right_container.add_widget(BeginCollapseWidget("collapse_3", "Important Thing 3"))
            right_container.add_widget(BeginCollapseWidget("collapse_4", "Homework"))
            right_container.add_widget(BeginCollapseWidget("collapse_5", "Definitely Homework, please leave"))
            right_container.add_widget(BeginCollapseWidget("collapse_6", "D O  N O T  O P E N"))
            right_container.add_widget(ButtonWidget("lol_button", "D O  N O T  C L I C K"))
            right_container.add_widget(EndCollapseWidget())
            right_container.add_widget(EndCollapseWidget())
            right_container.add_widget(EndCollapseWidget())
            right_container.add_widget(EndCollapseWidget())

            right_container.add_widget(BeginCollapseWidget("collapse_7", "Important Thing 4"))
            right_container.add_widget(TextWidget("chicken_text_2", "Backup backup picture of a chicken (Safety first)"))
            right_container.add_widget(ImageWidget("third_picture_of_a_chicken", methods.safe_load_image("res/images/tool_ui/widget_test/third_picture_of_a_chicken.jpg")))
            right_container.add_widget(EndCollapseWidget())

            right_container.add_widget(EndCollapseWidget())

        self.main_window.update(None)

    def draw(self):
        self.main_window.draw((0, 0))

        if commons.global_widget is not None:
            commons.global_widget.global_draw()

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

    def frame_update(self):
        altered_widgets = []
        if commons.global_widget is not None:
            commons.global_widget.global_frame_update(altered_widgets, pygame.mouse.get_pos())

        self.main_window.frame_update(altered_widgets, pygame.mouse.get_pos())

        for widget in altered_widgets:
            self.widget_altered(widget)

    def quit(self):
        commons.current_tool = None

    def widget_altered(self, widget):
        if widget.type == WidgetType.BUTTON:
            if widget.widget_id == "hide_ainsley":
                right_container = self.main_window.find_container("right_container")
                right_container.find_widget("test_image").toggle_hidden()
                right_container.update(None)

            elif widget.widget_id == "lol_button":
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

            elif widget.widget_id[:11] == "row_select_":
                left_container = self.main_window.find_container("left_container")
                for index in range(4):
                    left_container.find_widget("checkbox_" + widget.widget_id[-1] + "_" + str(index)).toggle_checked()

        elif widget.type == WidgetType.DROP_DOWN:
            if widget.widget_id == "drop_down_3":
                right_container = self.main_window.find_container("right_container")
                if widget.selected_string == "Mystery Image":
                    ainsley_image = methods.safe_load_image("res/images/tool_ui/widget_test/ainsley 4.jpg")
                    right_container.find_widget("ainsley").set_image(ainsley_image)
                else:
                    ainsley_number = widget.selected_string[-1]
                    ainsley_image = methods.safe_load_image("res/images/tool_ui/widget_test/ainsley " + ainsley_number + ".jpg")
                    right_container.find_widget("ainsley").set_image(ainsley_image)
                right_container.update(None)

