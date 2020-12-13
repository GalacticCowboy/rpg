import arcade
import math
import projectile
import os

PATH = os.path.dirname(os.path.abspath(__file__))

class Melee(arcade.Sprite):
    def __init__(self, file_name, img_scale=1, damage=75, orientation=0,melee_range=10,speed=20, throw_range=90):
        super().__init__(file_name,img_scale)
        self.file_name = file_name
        self.img_scale = img_scale
        self.damage = damage
        self.angle_adjustment = orientation
        self.attack_speed = 10
        self.life_span = 0
        self.throw_range = throw_range

    def attack(self, player_sprite, dest_x, dest_y):

        weapon_x = player_sprite.view_position[0]
        weapon_y = player_sprite.view_position[1]
        self.position = player_sprite.position

        x_diff = dest_x - weapon_x
        y_diff = dest_y - weapon_y
        angle = math.atan2(y_diff,x_diff)

        size = max(player_sprite.width, player_sprite.height)

        self.center_x += size * math.cos(angle)
        self.center_y += size * math.sin(angle)

        self.angle = math.degrees(angle) - self.angle_adjustment

        return self

    # def throw(self, player_sprite, dest_x, dest_y):
    #     '''Creates an identical object compatible with projectile logic and throws it'''
    #     item = projectile.Projectile(file=self.file_name,scale=self.img_scale,angle=self.angle_adjustment,damage=self.damage,10,max_range=self.throw_range,min_range=self.throw_range,does_stick=True)
    #     return item.shoot(player_sprite,dest_x,dest_y)



class Sword(Melee):
    def __init__(self):
        super().__init__(PATH+'/resources/sword_normal.png',img_scale=.9,damage=12, orientation=45,throw_range=50)