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
                
        
        # keys and locked doors
        key_hit_list = arcade.check_for_collision_with_list(self.player,
        self.keys_list)

        if len(key_hit_list) > 0:
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
                x.kill()

        # breakable blocks
        
        for y in self.breakable_blocks_list:
            breakable_blocks_hit_list = arcade.check_for_collision_with_list(y,
            self.melee_list)
            
            if len(breakable_blocks_hit_list):
                y.kill()

        # dont touch
        dont_touch_hit_list = arcade.check_for_collision_with_list(self.player,
        self.dont_touch_list)

        if len(dont_touch_hit_list) > 0:
            pass
