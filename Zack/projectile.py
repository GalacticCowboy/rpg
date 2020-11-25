import arcade
# import Sprite_lists


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
    # def update(self):
    #     self.position += self.velocity
        # hit_list = arcade.check_for_collision_with_list(self.sprite, Sprite_lists.wall_list)
        # if len(hit_list) != 0:
        #     self.kill()
        # kill the object
        # for each in hit_list:
        #     each.set_hp(self.damage)


class Arrow(Projectile):
    '''Arrow preset'''
    def __init__(self, damage=25, speed=20):
        super().__init__('arrow.png',.2, 90,damage,speed,does_stick=True)



# class Laser(Projectile):
#     def __init__(self, damage = 30, speed = 30):
#         super.__init__()
#         self.damage = damage
#         self.speed = speed
