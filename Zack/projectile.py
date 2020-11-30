import arcade
import math
# import mapTest


class Projectile(arcade.Sprite):
    '''Generic projectile. Subclasses represent various
    presets, however specific or unique instances can be generated here.'''

    def __init__(self, file, scale=1, angle_adjustment=0, damage=10, speed=10, burst_size=1,fire_rate=2,does_stick=False):
        super().__init__(file,scale)
        self.damage = damage
        self.speed = speed
        self.burst_size = burst_size
        self.fire_rate = fire_rate
        self.does_stick = does_stick
        self.orientation_adjustment = angle_adjustment
    # def update(self):
    #     self.position += self.velocity
        # hit_list = arcade.check_for_collision_with_list(self.sprite, Sprite_lists.wall_list)
        # if len(hit_list) != 0:
        #     self.kill()
        # kill the object
        # for each in hit_list:
        #     each.set_hp(self.damage)

    def shoot(self, player_sprite, dest_x, dest_y):
        '''Returns a projectile object ready to be appended to projectile list'''
        # if projectile_type == 'arrow':
        #     arrow = Arrow()
        # elif projectile_type == 'burst':
        #     pass

        projectile_x = player_sprite.center_x
        projectile_y = player_sprite.center_y
        self.position = player_sprite.position

        # dest_x = x
        # dest_y = y

        x_diff = dest_x - projectile_x
        y_diff = dest_y - projectile_y
        angle = math.atan2(y_diff, x_diff)

        size = max(player_sprite.width, player_sprite.height) / 2

        self.center_x += size * math.cos(angle)
        self.center_y += size * math.sin(angle)

        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        self.angle = math.degrees(angle) - self.orientation_adjustment

        return self

class Arrow(Projectile):
    '''Arrow preset'''
    def __init__(self, damage=25, speed=20):
        super().__init__('arrow.png',.2, 90,damage,speed,does_stick=True)
        self.orientation_adjustment = 90



# class Laser(Projectile):
#     def __init__(self, damage = 30, speed = 30):
#         super.__init__()
#         self.damage = damage
#         self.speed = speed
