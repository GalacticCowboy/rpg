# This code was stripped from the file "sprite_explosion_bitmapped.py"
#     from the Arcade website.

import random
import arcade
import os
import PIL
from arcade.draw_commands import Texture

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Explosion Example"

EXPLOSION_TEXTURE_COUNT = 60


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Pre-load the animation frames. We don't do this in the __init__
        # of the explosion sprite because it
        # takes too long and would cause the game to pause.
        self.explosion_texture_list = []

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = file_path + "\\resources\images\explosion.png"

        # Load the explosions from a sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

        # Load sounds. Sounds from kenney.nl
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/explosion2.wav")

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.explosions_list = arcade.SpriteList()

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_mouse_press(self, x, y, button, modifiers):
        # Make an explosion
        explosion = Explosion(self.explosion_texture_list)

        # Explosion sound
        arcade.sound.play_sound(self.hit_sound)

        # Move it to the location of the coin
        explosion.center_x = x
        explosion.center_y = y

        # Call update() because it sets which image we start on
        explosion.update()

        # Add to a list of sprites that are explosions
        self.explosions_list.append(explosion)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.explosions_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on explosion sprites
        self.explosions_list.update()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()