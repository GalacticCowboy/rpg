#load sounds
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


        
# play sounds
arcade.play_sound(self.sword_sound)
arcade.play_sound(self.arrow_sound)
arcade.play_sound(self.switch_sound)
arcade.play_sound(self.angry_peanut_death_sound)
arcade.play_sound(self.boss_death_sound)
arcade.play_sound(self.player_death_sound)
arcade.play_sound(self.damage_taken_enemy_sound)
arcade.play_sound(self.door_key_sound)
arcade.play_sound(self.wall_break_sound)
arcade.play_sound(self.background_sound)



