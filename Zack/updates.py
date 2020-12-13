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
# Boss stuff. At the bottom of the bad_guy loop. Line 380-ish


                    spawns = enemy.enemy_spawns[self.map_change]
        if spawns != None:
            for each in spawns:
                self.enemies_list.append(enemy.Enemy(spawns[0],spawns[1]))
        if self.map_change == 5:
            self.enemies_list.append(enemy.Boss(800,700))
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)
# Enemy spawns. Bottom of setup method

        self.player.view_position = [(self.player.center_x - self.view_left),(self.player.center_y-self.view_bottom)]
# Aiming. Bottom of update method