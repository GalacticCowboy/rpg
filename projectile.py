import arcade

class Projectile:
    def __init__(self, velocity, position):
        self.velocity = velocity
        self.position = position
        self.damage = 0
        self.sprite = None

    def update(self, delta_time):
        self.position[0,1] += self.velocity[0,1]
        hit_list = arcade.check_for_collision_with_list(self.sprite, controller_list)
        if len(hit_list) >= 1:
            pass
        # kill the object
        for each in hit_list:
            each.set_hp(self.damage)


class Arrow(Projectile):
    def __init__(self):
        super.__init__()
        self.damage = 25
        

class Laser(Projectile):
    def __init__(self):
        super.__init__()
        self.damage = 50
