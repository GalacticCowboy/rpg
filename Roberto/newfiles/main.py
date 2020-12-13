import arcade
import math
import random
import os
import enemy
import projectile
import melee
import sara
import traceback
import time

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Galactic Cowboy"

CHARACTER_SCALING = 1
TILE_SCALING = 1.75
DOOR_SCALING = 0.5
SPRITE_PIXEL_SIZE = 16
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

# Constants used to track of Sara direction
UP_FACING = 0
LEFT_FACING = 1
DOWN_FACING = 2
RIGHT_FACING = 3

PLAYER_START_X = 700
PLAYER_START_Y = 75

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 50
RIGHT_VIEWPORT_MARGIN = 50
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 50

# music volume
MUSIC_VOLUME = 0.5



PATH = os.path.dirname(os.path.abspath(__file__))


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Set up the game and initialize the variables. """
        super().__init__(width, height, title)

        self.doors_progress_list = None
        self.doors_return_list = None
        self.wall_list = None
        self.npc_list = None
        self.boss_list = None
        self.enemies_shoot_list = None
        self.melee_list = None
        self.enemies_list = None
        self.locked_blocks_list = None
        self.breakable_blocks_list = None
        self.movable_blocks_list = None
        self.switch_blocks_list = None
        self.keys_list = None
        self.hearts_list = None
        self.pickup_list = None
        self.charge_list = None
        self.switches_list = None
        self.moving_plat_horizontal_list = None
        self.moving_plat_vertical_list = None
        self.bounce_moving_plat_horizontal_list = None
        self.bounce_moving_plat_vertical_list = None
        self.platforms_list = None
        self.dont_touch_list = None
        self.background_list = None
        self.player_list = None
        self.player = None
        self.physics_engine = None
        self.frame_count = 0

        # map change
        self.map_change = 4

        # Used to keep track of our scrolling
        self.view_bottom = 100
        self.view_left = 100

        # the game sounds load up
        self.arrow_sound = arcade.load_sound("music/arrow_sound.wav")
        self.sword_sound = arcade.load_sound("music/sword_sound.wav")
        self.switch_sound = arcade.load_sound("music/switch_sound.wav")
        self.angry_peanut_death_sound = arcade.load_sound("music/angry_peanut_death_sound.wav")
        self.boss_death_sound = arcade.load_sound("music/boss_death_sound.wav")
        self.player_death_sound = arcade.load_sound("music/player_death_sound.wav")
        self.damage_taken_player_sound = arcade.load_sound("music/damage_taken_player_sound.mp3")
        self.damage_taken_enemy_sound = arcade.load_sound("music/damage_taken_enemy_sound.mp3")
        self.door_key_sound = arcade.load_sound("music/door_key_sound.wav")
        self.wall_break_sound = arcade.load_sound("music/wall_break_sound.wav")
        self.background_sound = arcade.load_sound("music/background_music.mp3")
        self.heart_sound = arcade.load_sound("music/heart_sound.wav")


        # background
        arcade.play_sound(self.background_sound, MUSIC_VOLUME)

    def setup(self, map_change):
        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.door_list = arcade.SpriteList(use_spatial_hash=True)

        

        # Set up the player
        self.player = sara.Sara()

        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y

        self.player_list.append(self.player)

        # Set the background color
        arcade.set_background_color(arcade.color.DEEP_SKY_BLUE)

        # Layers setup
        walls_layer_name = "Walls"
        doors_progress_layer_name = "DoorsProgress"
        doors_return_layer_name = "DoorsReturn"
        npc_layer_name = "NPC"
        moving_plat_vertical_layer_name = "MovingPlatformsVertical"
        moving_plat_horizontal_layer_name = "MovingPlatformsHorizontal"
        bounce_moving_plat_vertical_layer_name = "MovingPlatformsBounceVertical"
        bounce_moving_plat_horizontal_layer_name = "MovingPlatformsBounceHorizontal"
        boss_layer_name = "Boss"
        enemies_shoot_layer_name = "EnemiesShoot"
        enemies_layer_name = "Enemies"
        locked_blocks_layer_name = "LockedBlocks"
        breakable_blocks_layer_name = "BreakableBlocks"
        movable_blocks_layer_name = "MovableBlocks"
        switch_blocks_layer_name = "SwitchBlocks"
        platforms_layer_name = "Platforms"
        keys_layer_name = "Keys"
        switches_layer_name = "Switches"
        hearts_layer_name = "Hearts"
        dont_touch_layer_name = "DontTouch"
        background_layer_name = "Background"

        # name of the map we will load
        map_name = PATH + f"/maps/game_map_{map_change}.tmx"

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

        # Lists setup
        self.doors_progress_list = arcade.tilemap.process_layer(my_map, doors_progress_layer_name, TILE_SCALING)
        self.doors_return_list = arcade.tilemap.process_layer(my_map, doors_return_layer_name, TILE_SCALING)
        self.npc_list = arcade.tilemap.process_layer(my_map, npc_layer_name, TILE_SCALING)
        self.boss_list = arcade.tilemap.process_layer(my_map, boss_layer_name, TILE_SCALING)
        self.enemies_list = arcade.tilemap.process_layer(my_map, enemies_layer_name, TILE_SCALING)
        self.enemies_shoot_list = arcade.tilemap.process_layer(my_map, enemies_shoot_layer_name, TILE_SCALING)
        self.locked_blocks_list = arcade.tilemap.process_layer(my_map, locked_blocks_layer_name, TILE_SCALING)
        self.breakable_blocks_list = arcade.tilemap.process_layer(my_map, breakable_blocks_layer_name, TILE_SCALING)
        self.movable_blocks_list = arcade.tilemap.process_layer(my_map, movable_blocks_layer_name, TILE_SCALING)
        self.switch_blocks_list = arcade.tilemap.process_layer(my_map, switch_blocks_layer_name, TILE_SCALING)
        self.keys_list = arcade.tilemap.process_layer(my_map, keys_layer_name, TILE_SCALING)
        self.hearts_list = arcade.tilemap.process_layer(my_map, hearts_layer_name, TILE_SCALING)
        self.switches_list = arcade.tilemap.process_layer(my_map, switches_layer_name, TILE_SCALING)
        self.bounce_moving_plat_horizontal_list = arcade.tilemap.process_layer(my_map, bounce_moving_plat_horizontal_layer_name, TILE_SCALING)
        self.bounce_moving_plat_vertical_list = arcade.tilemap.process_layer(my_map, bounce_moving_plat_vertical_layer_name, TILE_SCALING)
        self.moving_plat_horizontal_list = arcade.tilemap.process_layer(my_map, moving_plat_horizontal_layer_name, TILE_SCALING)
        self.moving_plat_vertical_list = arcade.tilemap.process_layer(my_map, moving_plat_vertical_layer_name, TILE_SCALING)
        # # Append moving platforms to walls list.
        # for sprite in self.moving_plat_vertical_list:
        #     self.background_list.append(sprite)
        self.platforms_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
        self.dont_touch_list = arcade.tilemap.process_layer(my_map, dont_touch_layer_name, TILE_SCALING)
        self.pickup_list = arcade.SpriteList()
        self.charge_list = arcade.SpriteList()
        self.melee_list = arcade.SpriteList()

        # Adding the other block sprites to the wall list
        for x in self.switch_blocks_list:
            self.wall_list.append(x)
        
        for x in self.breakable_blocks_list:
            self.wall_list.append(x)

        for x in self.locked_blocks_list:
            self.wall_list.append(x)

        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # simple for over head games
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

        # Controls enemy spawning
        spawns = enemy.get_enemy_spawns(self.map_change)
        if spawns != None:
            for each in spawns:
                self.enemies_list.append(enemy.Enemy(spawns[0],spawns[1]))
        if self.map_change == 5:
            self.enemies_list.append(enemy.Boss(800,700))

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.background_list.draw()
        self.dont_touch_list.draw()
        self.platforms_list.draw()
        self.wall_list.draw()
        self.doors_progress_list.draw()
        self.doors_return_list.draw()
        self.locked_blocks_list.draw()
        self.breakable_blocks_list.draw()
        self.movable_blocks_list.draw()
        self.switch_blocks_list.draw()
        self.bounce_moving_plat_horizontal_list.draw()
        self.bounce_moving_plat_vertical_list.draw()
        self.moving_plat_horizontal_list.draw()
        self.moving_plat_vertical_list.draw()
        self.keys_list.draw()
        self.hearts_list.draw()
        self.switches_list.draw()
        self.npc_list.draw()
        self.boss_list.draw()
        self.enemies_shoot_list.draw()
        self.enemies_list.draw()
        self.pickup_list.draw()
        self.melee_list.draw()
        try:
            self.player_list.draw()
        except:
            import traceback
            traceback.print_exc()

        # Putting game info on screen
        score_text = f"Arrows: {self.player.ammo}"
        if self.player.ammo == 0:
            score_color = arcade.csscolor.RED
        else:
            score_color = arcade.csscolor.WHITE

        health_text = f"Health: {self.player.hp}"
        if self.player.hp <= 35:
            health_color = arcade.csscolor.RED
        else:
            health_color = arcade.csscolor.WHITE
        # arcade.draw_text(health_text, 775, 540,
        # color, 18)

        # Draw our score on the screen, scrolling it with the viewport
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         score_color, 20)
        arcade.draw_text(health_text, 10 + self.view_left, 30 + self.view_bottom,
                         health_color, 20)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or \
           key == arcade.key.W or \
           key == arcade.key.DOWN or \
           key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.RIGHT or \
             key == arcade.key.D or \
             key == arcade.key.LEFT or \
             key == arcade.key.A:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # move the player with the physics engine
        self.physics_engine.update()

        # Move the player
        self.player_list.update()

        # Update walls, used with moving platforms
        self.moving_plat_vertical_list.update()

        # Update the players animation
        self.player_list.update_animation()

        # for view port
        changed = False
     

        # if the player dies
        if self.player.hp <= 0:
            self.setup(self.map_change)
            arcade.play_sound(self.player_death_sound)

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        # --- Manage Combat Stuff
        for item in self.enemies_shoot_list:
            if (len(item.collides_with_list(self.wall_list)) > 0) or (arcade.get_distance(item.position[0],item.position[1],item.start_pos[0],item.start_pos[1]) > item.min_range):
                if item.does_stick:
                    item.change_x = 0
                    item.change_y = 0
                    if random.randint(0,100) < 40:
                        self.pickup_list.append(item)
                        self.enemies_shoot_list.remove(item)
                    else:
                        item.kill()
                else:
                    item.kill()
            shot_list = arcade.check_for_collision_with_list(item,self.enemies_list)
            if arcade.check_for_collision(self.player,item):
                shot_list.append(self.player)
            for self.person in shot_list:
                arcade.play_sound(self.damage_taken_player_sound)
                self.person.hp -= item.damage
                item.kill()

        self.enemies_shoot_list.update()
        self.charge_list.update()

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
            item.center_x += self.player.change_x
            item.center_y += self.player.change_y
            item.life_span +=1
            if item.life_span > item.attack_speed:
                item.kill()

        for bad_guy in self.enemies_list:
            slap_list = arcade.check_for_collision_with_list(bad_guy, self.melee_list)
            for item in slap_list:
                arcade.play_sound(self.damage_taken_enemy_sound)
                bad_guy.hp -= item.damage
                # bad_guy.kill()
                item.damage = 0
            if bad_guy.hp <= 0:
                for drop in bad_guy.drop():
                    self.pickup_list.append(drop)
                arcade.play_sound(self.angry_peanut_death_sound)
                bad_guy.kill()
            # bad_guy.path = arcade.astar_calculate_path(bad_guy.position, self.player.position,self.barrier_list,False)
            bad_guy.chase(self.player.center_x,self.player.center_y)
            if arcade.check_for_collision(bad_guy,self.player):
                self.player.hp -= bad_guy.damage
                self.player.center_x += (self.player.center_x-bad_guy.center_x)
                self.player.center_y += (self.player.center_y-bad_guy.center_y)
            bump_list = arcade.check_for_collision_with_list(bad_guy, self.wall_list)
            if len(bump_list) > 0:
                bad_guy.center_x += (bad_guy.center_x-bump_list[0].center_x)
                bad_guy.center_y += (bad_guy.center_y-bump_list[0].center_y)

            self.frame_count += 1
            if (self.frame_count) % (bad_guy.fire_rate*60) == 0:
                if bad_guy.type == 'pion':
                    bad_guy.has_shot = True
                    if (bad_guy.has_shot == True):
                        if arcade.has_line_of_sight(self.player.position,bad_guy.position,self.wall_list,500):
                            self.enemies_shoot_list.append(bad_guy.shoot(self.player))
                            bad_guy.has_shot = False
                elif bad_guy.type == 'boss':
                    self.enemies_list.append(bad_guy.spawn())

        pickup_hit_list = arcade.check_for_collision_with_list(self.player, self.pickup_list)

        for thing in pickup_hit_list:
            thing.kill()
            self.player.ammo += 1

        # --- Logic for moving platforms ---
        for sprite in self.moving_plat_vertical_list:

            if sprite.boundary_top and sprite.top > sprite.boundary_top and sprite.change_y > 0:
                sprite.change_y *= -1
            if sprite.boundary_bottom and sprite.bottom < sprite.boundary_bottom and sprite.change_y < 0:
                sprite.change_y *= -1

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

        for sprite in self.moving_plat_vertical_list:
            if arcade.check_for_collision(self.player, sprite) and \
            self.player.change_y == 0:
                self.player.center_y = sprite.center_y
            
        # see if we touch any doors
        door_progress_hit_list = arcade.check_for_collision_with_list(self.player,
        self.doors_progress_list)

        if len(door_progress_hit_list) > 0:
            if self.map_change < 5:
                self.map_change += 1
            else:
                self.map_change = 1
            self.setup(self.map_change)
            self.view_left = 0
            self.view_bottom = 0
            changed = True

        # see if we touch any return doors
        door_return_hit_list = arcade.check_for_collision_with_list(self.player,
        self.doors_return_list)

        if len(door_return_hit_list) > 0:
            self.map_change -= 1
            self.setup(self.map_change)
            self.view_left = 0
            self.view_bottom = 0
            changed = True

        # switches
        switch_hit_list = arcade.check_for_collision_with_list(self.player,
        self.switches_list)

        if len(switch_hit_list) > 0:
            for x in self.switch_blocks_list:
                x.remove_from_sprite_lists()
                arcade.play_sound(self.switch_sound)
                
        
        # keys and locked doors
        key_hit_list = arcade.check_for_collision_with_list(self.player,
        self.keys_list)

        if len(key_hit_list) > 0:
            arcade.play_sound(self.door_key_sound)
            for x in key_hit_list:
                x.kill()
                if len(self.locked_blocks_list) > 0:
                    for y in self.locked_blocks_list:
                        y.kill()
                    for y in self.locked_blocks_list:
                        y.kill()
                    for y in self.locked_blocks_list:
                        y.kill()
                    for y in self.locked_blocks_list:
                        y.kill()

        # hearts
        heart_hit_list = arcade.check_for_collision_with_list(self.player,
        self.hearts_list)

        if len(heart_hit_list) > 0:
            for x in heart_hit_list:
                arcade.play_sound(self.heart_sound)
                x.kill()
                self.player.hp += 10

        # breakable blocks
        # for block in self.breakable_blocks_list:
            # breakable_blocks_hit_list = arcade.check_for_collision_with_list(block,
            # self.melee_list)
            
            # for broken_block in breakable_blocks_hit_list:
            #     broken_block.kill()
        for y in self.breakable_blocks_list:
            breakable_blocks_hit_list = arcade.check_for_collision_with_list(y,
            self.melee_list)
        
            if len(breakable_blocks_hit_list):
                arcade.play_sound(self.wall_break_sound)
                y.kill()


        # dont touch
        dont_touch_hit_list = arcade.check_for_collision_with_list(self.player,
        self.dont_touch_list)

        if len(dont_touch_hit_list) > 0 and \
        len(arcade.check_for_collision_with_list(self.player, self.moving_plat_vertical_list)) <= 0:
            arcade.play_sound(self.player_death_sound)
            self.setup(self.map_change)

        # Aiming
        self.player.view_position = [(self.player.center_x - self.view_left),(self.player.center_y-self.view_bottom)]
        

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.play_sound(self.sword_sound)
            if len(self.melee_list) == 0:
                sword = melee.Sword()
                self.melee_list.append(sword.attack(self.player,self._mouse_x, self._mouse_y))

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if self.player.ammo > 0:
                arrow = projectile.Arrow()
                self.charge_list.append(arrow)


    def on_mouse_release(self,x,y,button,modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            arrow = self.charge_list.pop()
            arrow.min_range = max(int(arrow.max_range * (arrow.power/100)), arrow.min_range)
            self.enemies_shoot_list.append(arrow.shoot(self.player,self._mouse_x,self._mouse_y))
            self.player.ammo -= 1
            if self.player.ammo >= 0:
                arcade.play_sound(self.arrow_sound)

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup(window.map_change)
    arcade.run()


if __name__ == "__main__":
    main()