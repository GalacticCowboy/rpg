import arcade
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move with a Sprite Animation Example"

COIN_SCALE = 0.5
COIN_COUNT = 15
CHARACTER_SCALING = 1

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

# Constants used to track of Sara direction
UP_FACING = 0
LEFT_FACING = 1
DOWN_FACING = 2
RIGHT_FACING = 3


def get_texture(filename, x, y):
    """
    Load a texture from the sprite sheet.

    Up: y = 8, Left: y = 9, Down: y = 10, Right: y = 11.
    Cycle through x from 0 to 8.
    """
    return arcade.load_texture(filename, x * 64, y * 64, width=64, height=64)


class Sara(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = UP_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Path to Sara sprite sheet
        self.file_path = os.path.dirname(os.path.abspath(__file__)) + \
        "\\resources\images\SaraFullSheet.png"

        # Load textures
        self.textures = []
        direction_set = []
        for y in range(8, 12):
            direction_set = []
            for x in range(9):
                direction_set.append(get_texture(self.file_path, x, y))
            self.textures.append(direction_set)

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to change direction
        if self.change_y < 0 and self.character_face_direction != DOWN_FACING:
            self.character_face_direction = DOWN_FACING
        elif self.change_y > 0 and self.character_face_direction != UP_FACING:
            self.character_face_direction = UP_FACING
        elif self.change_x < 0 and self.character_face_direction != LEFT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction != RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        # print(self.textures[0][0])
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.textures[0][0]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 8 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.textures[direction][frame]


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Set up the game and initialize the variables. """
        super().__init__(width, height, title)

        # Sprite lists
        self.player_list = None
        self.coin_list = None

        # Set up the player
        self.score = 0
        self.player = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player = Sara()

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        # self.player.scale = 0.8 # This seems redundant...

        self.player_list.append(self.player)

        for i in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/gold_1.png",
                                 scale=0.5)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.coin_list.draw()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        self.player_list.update()

        # Update the players animation
        self.player_list.update_animation()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()