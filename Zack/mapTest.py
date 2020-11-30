import arcade
import math
import random
import projectile

#Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "PLATFORMER"

# MAX_SPREAD = .05  # +/- in degrees

#Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 16
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

#movement
PLAYER_MOVEMENT_SPEED = 5

#scrolling
LEFT_VIEWPORT_MARGIN = 50
RIGHT_VIEWPORT_MARGIN = 50
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 50

class MyGame(arcade.Window):


    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        # self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.background_list = None

        #Separate variable that holds the player sprite
        self.player_sprite = None


        #physics engine
        self.physics_engine = None

        #Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        #keeping track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        #keep track of the score
        self.score = 0

        #load sounds
        # self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.firing = False
        self.frame_count = 0



    def setup(self):
        #set up the game here. Call this function to restart the game.
        #create the sprite lists

        self.view_bottom = 0
        self.view_left = 0

        #Keep track of the score
        self.score = 0

        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        # self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.projectile_list = arcade.SpriteList()

        image_source = "Hat_man1.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        self.player_sprite.scale = 0.3




        #create the ground
        #this shows using a loop to place multiple sprites horizontally

        # for x in range(0, 1250, 64):
        #     wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
        #     wall.center_x = x
        #     wall.center_y = 32
        #     self.wall_list.append(wall)

        # #Put some crates on the ground
        # #This shows using a coordinate list to place sprites

        # coordinate_list = [[512, 96],
        # [256, 96],
        # [768, 96]]

        # for coordinate in coordinate_list:
        #     #add a crate on the ground
        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
        #     wall.position = coordinate
        #     self.wall_list.append(wall)

        # #loop to place coins
        # for x in range(128, 1250, 256):
        #     coin = arcade.Sprite(":resources:images/items/coinGold.png", COIN_SCALING)
        #     coin.center_x = x
        #     coin.center_y = 96
        #     self.coin_list.append(coin)


        #load in map from the tiled editor

        #Name of map file to load
        map_name = "test.tmx"
        #name of the layer the will act as like walls
        platforms_layer_name = "Platforms"
        #name of the layer that are for pick ups
        # coins_layer_name = "Coins"
        #background
        background_layer_name = "Background"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        #background
        self.background_list = arcade.tilemap.process_layer(my_map,
        background_layer_name,TILE_SCALING)


        #platforms
        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
        layer_name=platforms_layer_name,
        scaling=TILE_SCALING,
        use_spatial_hash=True)

        #coins
        # self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, scaling=TILE_SCALING, use_spatial_hash=True)


        #otherstuff
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)


        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        #simple for overhead games

    def on_draw(self):
        #render to the screen

        #clear the screen to the background color
        arcade.start_render()

        #draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.wall_list.draw()
        # self.coin_list.draw()
        self.player_list.draw()


        #Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
        arcade.csscolor.WHITE, 18)

        self.projectile_list.draw()

    def on_update(self, delta_time):
        #move the player with the physics engine
        self.physics_engine.update()
        self.projectile_list.update()
        for item in self.projectile_list:
            if len(item.collides_with_list(self.wall_list)) > 0:
                if item.does_stick:
                    item.change_x = 0
                    item.change_y = 0
                else:
                    item.kill()

        if self.firing == True:
            arrow = projectile.Arrow()
            if self.frame_count > (arrow.fire_rate * arrow.burst_size):
                self.firing = False
                self.frame_count = 0
            elif self.frame_count % arrow.fire_rate == 0:
                self.projectile_list.append(arrow.shoot(player_sprite=self.player_sprite,dest_x=self._mouse_x,dest_y=self._mouse_y))

            self.frame_count += 1

        #calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        #see if we hit any coins
        # coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
        # self.coin_list)

        #loop through each coin we hit (if any) and remove it
        # for coin in coin_hit_list:
        #     #Remove the coin
        #     coin.remove_from_sprite_lists()
        #     #play a sound
        #     arcade.play_sound(self.collect_coin_sound)
        #     #Add one to the score
        #     self.score += 1


        #Track if we need to change the viewport
        changed = False

        #Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        #Scroll right
        right_boundary = self.view_left + 250 - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        #Scroll UP
        top_boundary = self.view_bottom + 250 - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        #Scroll Down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        changed = False
        if changed:
            #Only scroll to integers. OTHERwise we end up with pixels that
            #dont line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            #do the scrolling
            arcade.set_viewport(self.view_left,
            250 + self.view_left,
            self.view_bottom,
            250 + self.view_bottom)





    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    # def on_mouse_press(self, x, y, button, modifiers):
    # def on_mouse_scroll(self, x, y, button, modifiers):
    def on_mouse_motion(self, x, y, button, modifiers):
        self.firing = True
        # self.shoot(x,y)
        # arrow = projectile.Arrow()
        # self.projectile_list.append(arrow.shoot(player_sprite=self.player_sprite,dest_x=self._mouse_x,dest_y=self._mouse_y))



    # def shoot(self, dest_x, dest_y, projectile_type='arrow'):
    #     if projectile_type == 'arrow':
    #         arrow = projectile.Arrow()
    #     elif projectile_type == 'burst':
    #         pass

    #     arrow_y = self.player_sprite.center_y
    #     arrow_x = self.player_sprite.center_x
    #     arrow.position = self.player_sprite.position

    #     # dest_x = (250/SCREEN_WIDTH)
    #     # dest_y = 250/SCREEN_HEIGHT

    #     x_diff = dest_x - arrow_x
    #     y_diff = dest_y - arrow_y
    #     angle = math.atan2(y_diff, x_diff)

    #     size = max(self.player_sprite.width, self.player_sprite.height) / 2

    #     arrow.center_x += size * math.cos(angle)
    #     arrow.center_y += size * math.sin(angle)

    #     arrow.change_x = math.cos(angle) * ARROW_SPEED
    #     arrow.change_y = math.sin(angle) * ARROW_SPEED

    #     arrow.angle = math.degrees(angle) - 90

    #     self.projectile_list.append(arrow)

    #     # print(f'({x},{y})')
    #     # print(f'({arrow_x},{arrow_y})')


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()