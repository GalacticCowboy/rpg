import arcade

import arcade.gui
from arcade.gui import UIManager


class MyFlatButton(arcade.gui.UIFlatButton):
    def on_click(self):
      
        print("Click flat button. ")

class MyTitleFlatButton(arcade.gui.UITitleFlatButton):

    def __init__(self, center_x, center_y, input_box):
        super().__init__(
            'Start Game',
            center_x=center_x,
            center_y=center_y,
            width=250,
            # height=20
        )
        self.input_box = input_box

    def on_click(self):
        print(f"Click Title flat button. {self.input_box.text}")


class MyView(arcade.View):
    """
    Main view. Really the only view in this example. """
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

    def on_draw(self):
        """ Draw this view. GUI elements are automatically drawn. """
        arcade.start_render()

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        """ Set up this view. """
        self.ui_manager.purge_ui_elements()

        y_slot = self.window.height // 4
        left_column_x = self.window.width // 4
        right_column_x = 3 * self.window.width // 4

        # left side elements
        self.ui_manager.add_ui_element(arcade.gui.UILabel(
            'UILabel',
            center_x=left_column_x,
            center_y=y_slot * 3,
        ))

        ui_input_box = arcade.gui.UIInputBox(
            center_x=left_column_x,
            center_y=y_slot * 2,
            width=300
        )
        ui_input_box.text = 'UIInputBox'
        ui_input_box.cursor_index = len(ui_input_box.text)
        self.ui_manager.add_ui_element(ui_input_box)

        button_normal = arcade.load_texture(':resources:gui_basic_assets/red_button_normal.png')
        hovered_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_hover.png')
        pressed_texture = arcade.load_texture(':resources:gui_basic_assets/red_button_press.png')
        button = arcade.gui.UIImageButton(
            center_x=left_column_x,
            center_y=y_slot * 1,
            normal_texture=button_normal,
            hover_texture=hovered_texture,
            press_texture=pressed_texture,
            text='UIImageButton'
        )
        self.ui_manager.add_ui_element(button)

        # right side elements
        button = MyFlatButton(
            'FlatButton',
            center_x=right_column_x,
            center_y=y_slot * 1,
            width=250,
            # height=20
        )
        self.ui_manager.add_ui_element(button)

        button = MyTitleFlatButton(
            center_x=right_column_x,
            center_y=y_slot * 2,
            input_box=ui_input_box
        )
        self.ui_manager.add_ui_element(button)


if __name__ == '__main__':
    window = arcade.Window(title='ARCADE_GUI')
    view = MyView()
    window.show_view(view)
    arcade.run()
