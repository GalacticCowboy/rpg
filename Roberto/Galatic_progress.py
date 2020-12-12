import arcade
import random
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move with a Sprite Animation Example"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
DOOR_SCALING = 0.5

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

# Constants used to track of Sara direction
UP_FACING = 0
LEFT_FACING = 1
DOWN_FACING = 2
RIGHT_FACING = 3


PLAYER_START_X = 0
PLAYER_START_Y = 0

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
        "/sprites/LPC_Sara/SaraFullSheet.png"

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

        # door progress list
        self.doors_progress_list = None

        # door return list
        self.doors_return_list = None

        # wall list
        self.wall_list = None

        # npc list
        self.npc_list = None

        # boss list
        self.boss_list = None

        # EnemiesShoot
        self.enemies_shoot_list = None

        # Enemies
        self.enemies_list = None

        # locked blocks
        self.locked_blocks_list = None

        # breakable blocks
        self.breakable_blocks_list = None

        # Movable blocks
        self.movable_blocks_list = None

        # switch blocks
        self.switch_blocks_list = None

        # keys
        self.keys_list = None

        # hearts
        self.hearts_list = None

        # switches
        self.switches_list = None

        # moving platforms horizontal
        self.moving_plat_horizontal_list = None

        # moving platforms vertical
        self.moving_plat_vertical_list = None

        # bounce the platforms horizontal
        self.bounce_moving_plat_horizontal_list = None

        # bounce the platforms vertical
        self.bounce_moving_plat_vertical_list = None

        # platforms
        self.platforms_list = None

        # dont touch
        self.dont_touch_list = None

        # back ground list
        self.background_list = None

        # Sprite lists
        self.player_list = None

        # Set up the player
        self.player = None

        # physics engine
        self.physics_engine = None

        # map change
        self.map_change = 1

    def setup(self, map_change):
        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.door_list = arcade.SpriteList(use_spatial_hash=True)
        
        # Set up the player
        self.player = Sara()

        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y

        self.player_list.append(self.player)

        # Set the background color
        arcade.set_background_color(arcade.color.DEEP_SKY_BLUE)

        # layer for the walls
        walls_layer_name = "Walls"
        # layer for the doors to go on
        doors_progress_layer_name = "DoorsProgress"
        # layer for the dorrs to return
        doors_return_layer_name = "DoorsReturn"
        # layer for the npcs
        npc_layer_name = "NPC"
        # layer for moving platforms vertical
        moving_plat_vertical_layer_name = "MovingPlatformsVertical"
        # layer for moving platforms horizontal
        moving_plat_horizontal_layer_name = "MovingPlatformsHorizontal"
        # layer to change the direction of the vertical platforms
        bounce_moving_plat_vertical_layer_name = "MovingPlatformsBounceVertical"
        # layer to change the direction of the horizontal platforms
        bounce_moving_plat_horizontal_layer_name = "MovingPlatformsBounceHorizontal"
        # layer for the boss
        boss_layer_name = "Boss"
        # layer for enemies shoot
        enemies_shoot_layer_name = "EnemiesShoot"
        # layer for enemies
        enemies_layer_name = "Enemies"
        # layer for locked blocks
        locked_blocks_layer_name = "LockedBlocks"
        # layer for breakable blocks
        breakable_blocks_layer_name = "BreakableBlocks"
        # layer for movable blocks
        movable_blocks_layer_name = "MovableBlocks"
        # layer for switch blocks
        switch_blocks_layer_name = "SwitchBlocks"
        # layer for the platforms
        platforms_layer_name = "Platforms"
        # layer for the keys
        keys_layer_name = "Keys"
        # layer for the switches
        switches_layer_name = "Switches"
        # layer for the hearts
        hearts_layer_name = "Hearts"
        #layer for dont touch
        dont_touch_layer_name = "DontTouch"
        # layer for the background
        background_layer_name = "Background"

        # name of the map we will load
        map_name = f"levels/game_map_{map_change}.tmx"

        # reading the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # background
        self.background_list = arcade.tilemap.process_layer(my_map,
        background_layer_name, TILE_SCALING)

        # walls
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
        layer_name=walls_layer_name,
        scaling=TILE_SCALING,
        use_spatial_hash=True)

        # doors progress
        self.doors_progress_list = arcade.tilemap.process_layer(my_map, doors_progress_layer_name, TILE_SCALING)

        # doors return
        self.doors_return_list = arcade.tilemap.process_layer(my_map, doors_return_layer_name, TILE_SCALING)

        # npcs
        self.npc_list = arcade.tilemap.process_layer(my_map, npc_layer_name, TILE_SCALING)

        # boss
        self.boss_list = arcade.tilemap.process_layer(my_map, boss_layer_name, TILE_SCALING)

        # enemies
        self.enemies_list = arcade.tilemap.process_layer(my_map, enemies_layer_name, TILE_SCALING)

        # enemies shoot
        self.enemies_shoot_list = arcade.tilemap.process_layer(my_map, enemies_shoot_layer_name, TILE_SCALING)

        # locked blocks
        self.locked_blocks_list = arcade.tilemap.process_layer(my_map, locked_blocks_layer_name, TILE_SCALING)

        # breakable blocks
        self.breakable_blocks_list = arcade.tilemap.process_layer(my_map, breakable_blocks_layer_name, TILE_SCALING)

        # movable blocks
        self.movable_blocks_list = arcade.tilemap.process_layer(my_map, movable_blocks_layer_name, TILE_SCALING)

        # switch blocks
        self.switch_blocks_list = arcade.tilemap.process_layer(my_map, switch_blocks_layer_name, TILE_SCALING)

        #keys
        self.keys_list = arcade.tilemap.process_layer(my_map, keys_layer_name, TILE_SCALING)

        # hearts
        self.hearts_list = arcade.tilemap.process_layer(my_map, hearts_layer_name, TILE_SCALING)

        # switches
        self.switches_list = arcade.tilemap.process_layer(my_map, switches_layer_name, TILE_SCALING)

        # bounce the plats horizontal
        self.bounce_moving_plat_horizontal_list = arcade.tilemap.process_layer(my_map, bounce_moving_plat_horizontal_layer_name, TILE_SCALING)

        # bounce the plats vertical
        self.bounce_moving_plat_vertical_list = arcade.tilemap.process_layer(my_map, bounce_moving_plat_vertical_layer_name, TILE_SCALING)

        # the plats move horizontal
        self.moving_plat_horizontal_list = arcade.tilemap.process_layer(my_map, moving_plat_horizontal_layer_name, TILE_SCALING)

        # the plats move vertical
        self.moving_plat_vertical_list = arcade.tilemap.process_layer(my_map, moving_plat_vertical_layer_name, TILE_SCALING)

        # platforms
        self.platforms_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)

        # dont touch
        self.dont_touch_list = arcade.tilemap.process_layer(my_map, dont_touch_layer_name, TILE_SCALING)
    

        #simple for over head games
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)


    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.background_list.draw()
        self.wall_list.draw()
        self.doors_progress_list.draw()
        self.doors_return_list.draw()
        self.locked_blocks_list.draw()
        self.breakable_blocks_list.draw()
        self.movable_blocks_list.draw()
        self.switch_blocks_list.draw()
        self.platforms_list.draw()
        self.bounce_moving_plat_horizontal_list.draw()
        self.bounce_moving_plat_vertical_list.draw()
        self.moving_plat_horizontal_list.draw()
        self.moving_plat_vertical_list.draw()
        self.keys_list.draw()
        self.hearts_list.draw()
        self.switches_list.draw()
        self.dont_touch_list.draw()
        self.npc_list.draw()
        self.boss_list.draw()
        self.enemies_shoot_list.draw()
        self.enemies_list.draw()
        self.player_list.draw()

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

        # move the player with the physics engine
        self.physics_engine.update()

        # Move the player
        self.player_list.update()

        # Update the players animation
        self.player_list.update_animation()

        # see if we touch any doors
        door_hit_list = arcade.check_for_collision_with_list(self.player,
        self.door_list)

        if door_hit_list:
            self.map_change = 2
            self.setup(self.map_change)



def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup(window.map_change)
    arcade.run()


if __name__ == "__main__":
    main()