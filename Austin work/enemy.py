import arcade
import random
import os
import projectile
import melee
import math

PATH = os.path.dirname(os.path.abspath(__file__))

def get_enemy_spawns(index):
        """Get enemy spawns."""
        enemy_spawns = [None,(1850,1130),(1291,1100),(700,1090),None,None]
        return enemy_spawns[index]

class Enemy(arcade.Sprite):
    def __init__(self,x,y,image=PATH+'/resources/angry_peanut.png',size=.3):
        """Initializer for the enemy."""

        super().__init__(image,size)

        self.hp = 50
        self.drop_list = [1,1,1,2,2,2,2,3,3,4]
        self.damage = 10

        self.center_x = x
        self.center_y = y

        self.speed = 1.25
        self.path = None

        self.fire_rate = 2
        self.has_shot = True

        self.view_position = self.position
        self.type = "pion"

    def drop(self):
        '''Creates arrows to drop'''
        try:
            drop = self.drop_list[random.randint(0,20)]
            # drop = self.drop_list[1]
        except IndexError:
            drop = 0

        drop_list = []
        for each in range(drop):
            arrow = projectile.Arrow(position=self.position)
            drop_list.append(arrow)

        return drop_list

    def chase(self, dest_x, dest_y):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.
        """

        if self.center_y < dest_y:
            self.center_y += min(self.speed, dest_y - self.center_y)
        elif self.center_y > dest_y:
            self.center_y -= min(self.speed, self.center_y - dest_y)

        if self.center_x < dest_x:
            self.center_x += min(self.speed, dest_x - self.center_x)
        elif self.center_x > dest_x:
            self.center_x -= min(self.speed, self.center_x - dest_x)

    def shoot(self, target_sprite):
        self.view_position = self.position
        arrow = projectile.Arrow()
        arrow.max_range = random.randint(int(arrow.max_range*0.667),arrow.max_range)
        arrow.min_range = arrow.max_range
        return arrow.shoot(self, target_sprite.center_x,target_sprite.center_y)

class Boss(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y,image=PATH+'/resources/boss_slime.png',size=.2)
        self.hp = 1000
        self.damage = 25
        self.speed = 0.5

        self.fire_rate = 5
        self.type = 'boss'

    def spawn(self):
        '''Creates a new enemy to be appended into the bad guy list.'''

        dist = max(self.height,self.width)
        dist = dist * 1.5

        x = (dist * math.cos(random.randint(0,360))) + self.center_x
        y = (dist * math.sin(random.randint(0,360))) + self.center_y

        bad_guy = Enemy(x,y)
        return bad_guy