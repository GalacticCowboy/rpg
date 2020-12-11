import arcade
import math
import random
import projectile
import melee
import enemy
import os

#Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "PLATFORMER"

# MAX_SPREAD = .05  # +/- in degrees

#Constants used to scale our sprites from their original size
CHARACTER_SCALING = .6
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 16
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

#movement
MOVEMENT_SPEED = 3
ENEMY_COUNT = 2

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

# Constants used to track of Sara direction
UP_FACING = 0
LEFT_FACING = 1
DOWN_FACING = 2
RIGHT_FACING = 3

#scrolling
LEFT_VIEWPORT_MARGIN = 50
RIGHT_VIEWPORT_MARGIN = 50
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 50

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
        self.hp = 100

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        # self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Path to Sara sprite sheet
        self.file_path = os.path.dirname(os.path.abspath(__file__)) + \
        "\\Sprites\\SaraFullSheet.png"

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
            self.texture = self.textures[2][0]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 8 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.textures[direction][frame]

class MyGame(arcade.Window):


    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.pickup_list = None
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
        self.ammo = 0

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
        self.ammo = 5

        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.pickup_list = arcade.SpriteList(use_spatial_hash=True)
        self.projectile_list = arcade.SpriteList()
        self.charge_list = arcade.SpriteList()
        self.melee_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        example = enemy.Enemy(720,420)
        self.enemy_list.append(example)
        self.barrier_list = arcade.AStarBarrierList(example,self.wall_list,64*CHARACTER_SCALING,30,1000,30,700)
        # image_source = "Sprites/Hat_man1.png"
        self.player_sprite = Sara()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        self.player_sprite.scale = CHARACTER_SCALING



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
        #     self.pickup_list.append(coin)


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
        # self.pickup_list = arcade.tilemap.process_layer(my_map, coins_layer_name, scaling=TILE_SCALING, use_spatial_hash=True)


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
        self.pickup_list.draw()
        self.player_list.draw()
        self.melee_list.draw()
        self.enemy_list.draw()

        for bad_guy in self.enemy_list:
            if bad_guy.path:
                arcade.draw_line_strip(bad_guy.path, arcade.color.BLUE, 2)

        #Draw our score on the screen, scrolling it with the viewport
        score_text = f"Arrows: {self.ammo}"
        if self.ammo == 0:
            color = arcade.csscolor.RED
        else:
            color = arcade.csscolor.WHITE
        arcade.draw_text(score_text, 775, 590,
        color, 18)

        health_text = f"Health: {self.player_sprite.hp}"
        if self.player_sprite.hp <= 35:
            color = arcade.csscolor.RED
        else:
            color = arcade.csscolor.WHITE
        arcade.draw_text(health_text, 775, 540,
        color, 18)

        if len(self.charge_list) > 0:
            power = self.charge_list[0].power// 10
        else:
            power = 0
        indicator = '-' * power
        space = ' ' * (10 - power)
        if power == 10:
            charge_color = arcade.csscolor.RED
        else:
            charge_color = arcade.csscolor.WHITE
        charge_text = f"Charging: <{indicator}{space}>"
        arcade.draw_text(charge_text,775, 490,
        charge_color, 18)


        self.projectile_list.draw()

    def on_update(self, delta_time):
        #move the player with the physics engine
        self.frame_count += 1
        self.player_list.update_animation()
        self.enemy_list.update()
        self.physics_engine.update()
        self.projectile_list.update()
        self.charge_list.update()
        if len(self.enemy_list) < ENEMY_COUNT:
            self.enemy_list.append(enemy.Enemy(random.randint(30,500),random.randint(30,500)))

        for item in self.projectile_list:
            if (len(item.collides_with_list(self.wall_list)) > 0) or (arcade.get_distance(item.position[0],item.position[1],item.start_pos[0],item.start_pos[1]) > item.min_range):
                if item.does_stick:
                    item.change_x = 0
                    item.change_y = 0
                    if random.randint(0,100) < 40:
                        self.pickup_list.append(item)
                        self.projectile_list.remove(item)
                    else:
                        item.kill()
                else:
                    item.kill()
            shot_list = arcade.check_for_collision_with_list(item,self.enemy_list)
            if arcade.check_for_collision(self.player_sprite,item):
                shot_list.append(self.player_sprite)
            for person in shot_list:
                person.hp -= item.damage
                item.kill()

        if len(self.charge_list) == 0:
            MOVEMENT_SPEED = 5
        else:
            MOVEMENT_SPEED = 2
        for item in self.charge_list:
            if item.power <= 100:
                item.power += 3
            else:
                item.power = 100

        self.melee_list.update()
        for item in self.melee_list:
            item.center_x += self.player_sprite.change_x
            item.center_y += self.player_sprite.change_y
            item.life_span +=1
            if item.life_span > item.attack_speed:
                item.kill()
            if len(arcade.check_for_collision_with_list(item, self.wall_list)) > 0:
                item.kill()

        for bad_guy in self.enemy_list:
            slap_list = arcade.check_for_collision_with_list(bad_guy, self.melee_list)
            for item in slap_list:
                bad_guy.hp -= item.damage
                # bad_guy.kill()
                item.damage = 0
            if bad_guy.hp <= 0:
                for drop in bad_guy.drop():
                    self.pickup_list.append(drop)
                bad_guy.kill()
            bad_guy.path = arcade.astar_calculate_path(bad_guy.position, self.player_sprite.position,self.barrier_list,False)
            try:
                bad_guy.chase(bad_guy.path[0][0],bad_guy.path[0][1])
            except IndexError:
                self.player_sprite.hp -= bad_guy.damage
            except Exception as e:
                print(e)

            if (self.frame_count) % (bad_guy.fire_rate*60) == 0:
                bad_guy.has_shot = True
                if (bad_guy.has_shot == True):
                    if arcade.has_line_of_sight(self.player_sprite.position,bad_guy.position,self.wall_list,500):
                        self.projectile_list.append(bad_guy.shoot(self.player_sprite))
                        bad_guy.has_shot = False
            # print(bad_guy.path,"->", self.player_sprite.position)

        #calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        #see if we hit any coins
        pickup_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.pickup_list)

        #loop through each coin we hit (if any) and remove it
        for thing in pickup_hit_list:
        #     #Remove the coin
            thing.remove_from_sprite_lists()
        #     #play a sound
        #     arcade.play_sound(self.collect_coin_sound)
        #     #Add one to the score
            self.ammo += 1


        # #Track if we need to change the viewport
        # changed = False

        # #Scroll left
        # left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        # if self.player_sprite.left < left_boundary:
        #     self.view_left -= left_boundary - self.player_sprite.left
        #     changed = True

        # #Scroll right
        # right_boundary = self.view_left + 250 - RIGHT_VIEWPORT_MARGIN
        # if self.player_sprite.right > right_boundary:
        #     self.view_left += self.player_sprite.right - right_boundary
        #     changed = True

        # #Scroll UP
        # top_boundary = self.view_bottom + 250 - TOP_VIEWPORT_MARGIN
        # if self.player_sprite.top > top_boundary:
        #     self.view_bottom += self.player_sprite.top - top_boundary
        #     changed = True

        # #Scroll Down
        # bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        # if self.player_sprite.bottom < bottom_boundary:
        #     self.view_bottom -= bottom_boundary - self.player_sprite.bottom
        #     changed = True

        # changed = False
        # if changed:
        #     #Only scroll to integers. OTHERwise we end up with pixels that
        #     #dont line up on the screen
        #     self.view_bottom = int(self.view_bottom)
        #     self.view_left = int(self.view_left)

        #     #do the scrolling
        #     arcade.set_viewport(self.view_left,
        #     250 + self.view_left,
        #     self.view_bottom,
        #     250 + self.view_bottom)





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

    def on_mouse_press(self, x, y, button, modifiers):
    # def on_mouse_scroll(self, x, y, button, modifiers):
    # def on_mouse_motion(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if len(self.melee_list) == 0:
                sword = melee.Sword()
                # if modifiers == arcade.key.MOD_SHIFT:
                #     self.projectile_list.append(sword.throw(self.player_sprite,self._mouse_x,self._mouse_y))
                # else:
                self.melee_list.append(sword.attack(self.player_sprite,self._mouse_x,self._mouse_y))

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if self.ammo > 0:
                arrow = projectile.Arrow()
                self.charge_list.append(arrow)


    def on_mouse_release(self,x,y,button,modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            arrow = self.charge_list.pop()
            arrow.min_range = max(int(arrow.max_range * (arrow.power/100)), arrow.min_range)
            self.projectile_list.append(arrow.shoot(self.player_sprite,self._mouse_x,self._mouse_y))
            self.ammo -= 1
            print(arrow.min_range)

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()