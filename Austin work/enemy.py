import arcade
import random
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Moveable Enemy"

# Path to working directory
MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

# Constants used to scale our sprites from their original size
ENEMY_SCALING = 1
TILE_SCALING = 1.9

# Enemy constants (replace later with parameters)
ENEMY_MOVEMENT_SPEED = 10
ENEMY_HEALTH = 100


PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = SCREEN_HEIGHT / 2


class Enemy(arcade.Sprite):
    def __init__(self):
        """Initializer for the enemy."""
        
        # Set up parent class
        super().__init__()

        # Attributes
        self.scale = None
        self.center_x = None
        self.center_y = None
        self.texture = None
        self.health = None
        self.movement_speed = None

        # Path to enemy sprite sheet
        self.file_path = MAIN_PATH + "\\resources\images\\rpgcritters2.png"

    def setup(self):
        """Set up the enemy."""

        self.scale = ENEMY_SCALING

        # Set the enemy starting point
        self.center_x = PLAYER_START_X
        self.center_y = PLAYER_START_Y

        # Load texture 
        self.texture = arcade.load_texture(self.file_path, x=0, y=0, 
                                           width=48, height=46)

        # Set enemy health
        self.health = ENEMY_HEALTH

        # Set enemy movement speed
        self.movement_speed = ENEMY_MOVEMENT_SPEED


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Set up the game and initialize the variables. """

        super().__init__(width, height, title)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.wall_list = None
        self.background_list = None
        self.enemy_list = None

        # Separate variable that holds the player sprite
        self.enemy = None

        # Our 'physics' engine
        self.physics_engine = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Create the Sprite lists
        self.wall_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the enemy, specifically placing it at these coordinates.
        self.enemy = Enemy()
        self.enemy.setup()
        self.enemy_list.append(self.enemy)

        # --- Load in a map from the tiled editor ---

        # Layer names
        walls_layer_name = 'Walls'
        background_layer_name = "Background"
        map_name = MAIN_PATH + "\\resources\\tmx_files\enemy_test_map.tmx"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Wall objects
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      walls_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        # Background objects
        self.background_list = arcade.tilemap.process_layer(my_map, background_layer_name, TILE_SCALING)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(self.enemy, self.wall_list)


    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.enemy_list.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.enemy.change_y = self.enemy.movement_speed
        elif key == arcade.key.DOWN:
            self.enemy.change_y = -self.enemy.movement_speed
        elif key == arcade.key.LEFT:
            self.enemy.change_x = -self.enemy.movement_speed
        elif key == arcade.key.RIGHT:
            self.enemy.change_x = self.enemy.movement_speed

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.enemy.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.enemy.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the enemy with the physics engine
        self.physics_engine.update()


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()