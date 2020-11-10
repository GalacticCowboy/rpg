import arcade
class MyGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK)

        self.player_list = None
        self.player = None

        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()

        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("spritesheets/Hat_man1.png"))

        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("spritesheets/Hat_man1.png", mirrored=True))

        self.player.walk_right_textures = []
        self.player.walk_right_textures.append(arcade.load_texture("spritesheets/Hat_man1.png"))
        self.player.walk_right_textures.append(arcade.load_texture("spritesheets/Hat_man2.png"))
        self.player.walk_right_textures.append(arcade.load_texture("spritesheets/Hat_man3.png"))
        self.player.walk_right_textures.append(arcade.load_texture("spritesheets/Hat_man4.png"))

        self.player.walk_left_textures = []
        self.player.walk_left_textures.append(arcade.load_texture("spritesheets/Hat_man1.png", mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("spritesheets/Hat_man2.png", mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("spritesheets/Hat_man3.png", mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("spritesheets/Hat_man4.png", mirrored=True))

        self.player.scale = 3

        self.player.center_x = 1280 // 2
        self.player.center_y = 720 // 2

        self.player_list.append(self.player)

        
    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.player_list.update_animation()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = 15
        elif key == arcade.key.DOWN:
            self.player.change_y = -15
        elif key == arcade.key.LEFT:
            self.player.change_x = -15
        elif key == arcade.key.RIGHT:
            self.player.change_x = 15

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        




MyGameWindow(1280, 720, 'This is the game window')
arcade.run()