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
           
 # within the ondraw method
