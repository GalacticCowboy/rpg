import arcade
import random
import os
import projectile
import melee

class Enemy(arcade.Sprite):
    def __init__(self,x,y):
        """Initializer for the enemy."""
        super().__init__('Sprites\\Hat_man1.png',.3)

        self.hp = 50
        self.drop_list = [1,1,1,2,2,2,2,3,3,4]
        self.damage = 1

        self.center_x = x
        self.center_y = y

        self.speed = 1.25
        self.path = None

        self.fire_rate = 2
        self.has_shot = True
    def drop(self):
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
        arrow = projectile.Arrow()
        arrow.max_range = random.randint(int(arrow.max_range*0.667),arrow.max_range)
        arrow.min_range = arrow.max_range
        return arrow.shoot(self, target_sprite.center_x,target_sprite.center_y)
