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
        self.player = arcade.AnimatedTimeSprite()
        self.player.textures = []

       # for i in range(15):
       #     self.player.textures.append(arcade.load_texture("sprites/warrior_sprite_sheet.png", x=i*5, y=2, width=25,height=30))

        # x_pos = 0
        # y_pos = 0

        # for x in range(6): #frames
        #     if x % 2 == 0:
        #        x_pos = 0
        #     else:
        #         x_pos = 150
        #     if x % 6 in [2, 4, 6]:
        #         y_pos += 100
        #     self.player.textures.append(arcade.load_texture("sprites/warrior_sprite_sheet.png", x=x_pos, y=y_pos, width=20, height=30)


        self.player.textures.append(arcade.load_texture("sprites/warrior_sprite_sheet.png", x=0, y=0, width=25,height=30))
        self.player.textures.append(arcade.load_texture("sprites/warrior_sprite_sheet.png", x=100, y=0, width=25,height=30))
        self.player.textures.append(arcade.load_texture("sprites/warrior_sprite_sheet.png", x=200, y=0, width=25,height=30))
        self.player.textures.append(arcade.load_texture("sprites/warrior_sprite_sheet.png", x=225, y=0, width=25,height=30))
        self.player.textures.append(arcade.load_texture("sprites/warrior_sprite_sheet.png", x=250, y=0, width=25,height=30))
            
        self.player.center_x = 1280 // 2
        self.player.center_y = 720 // 2
        
        self.player.scale = 3

        self.player_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()


    def on_update(self, delta_time):
        self.player_list.update_animation()


MyGameWindow(1280, 720, 'This is the game window')
arcade.run()   