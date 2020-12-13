#load sounds
self.arrow_sound = arcade.load_sound("music/arrow_sound.wav")
self.sword_sound = arcade.load_sound("music/sword_sound.wav")
self.switch_sound = arcade.load_sound("music/switch_sound.wav")
        
# play sounds
arcade.play_sound(self.sword_sound)
arcade.play_sound(self.arrow_sound)
arcade.play_sound(self.switch_sound)
