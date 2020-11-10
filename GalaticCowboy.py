'''
This is my attempt at an outline for the Controller class. It seems like a lot, but 
most of it is simple methods and possible mechanics that we don't need, but I think
would be cool and not require much extra code. It also assumes that there's extra
information sitting in some other files (things like stats for races and the lines
for NPC's), but this is also low key meant to be a side-file that get referenced when
stuff happens. 
'''
import arcade

class Controller(arcade.Window):

    def __init__(self,  width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK)

        self.player_list = None
        self.player = None
        
        self.velocity = [0,0]               # list [x,y]
        self.position = [0,0]               # ^^ 
        self.hp = 100                       # int value
        self.race = ""                      # string (maybe just an int)
        #self.classType = classType          # ^^
        #self.affiliation = affiliation      # ^^
        self.visibility = 100               # int (maybe float if we're feelin frisky)
        #self.inventory = inventory          # list of items (data for items stored in a seperate object, maybe JSON)
        self.skills = []                    # list of ints i.e. [1,2,6,3] cooresponding to speed, strength, perceptions, etc

        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedTimeSprite()
        self.player.textures = []

        
        self.player.walk_down_textures = []
        self.player.walk_right_textures = []
        self.player.walk_left_textures = []

        x_pos = 0
        y_pos = 0
        

        for y in range(9):
            if y % 3 == 0:
                y_pos = 512
            else:
                y_pos = 512
            if y % 9 in [3, 6, 9]:
                x_pos += 64
            self.player.textures.append(arcade.load_texture("sprites/LPC_Sara/SaraFullSheet.png", x=x_pos, y=y_pos, width=64, height=64))

        self.player.center_x = 1280 // 2
        self.player.center_y = 720 //2

        self.player.scale = 3

        self.player_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.player_list.update_animation()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = 15
        elif key == arcade.key.DOWN:
            self.player.change_y = -15
        elif key == arcade.key.LEFT:
            self.player.change_x = -15
        elif key == arcade.key.RIGHT:
            self.player.change_x = 15

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0     



    def update_position(self):                      #Roberto
        """
        Pretty straight forward
        """
        pass

    def set_skills(self, perks):
        '''
        Takes the defined perks for certain races and classes and 
        computes the skill levels for the person (player, enemy, or NPC).
        Probably hp too. I just set hp at 100 as a general base so it was
        never at 0, because that would probably be bad.
        '''
        pass

    def use_item(self):
        """
        Index 0 in inventory list is their equipped item/weapon, and so all this
        thing does is excute the code for the item
        """
        pass

    def set_velocity(self):                     #Roberto
        '''
        Takes the input (from wherever it comes) and uses it to set the velocity 
        of the sprite, and probably multiplies it by the speed of the thing.
        '''
        pass

    def set_visibility(self):
        """
        Some stuff that decides how hard it is to see you
        """
        pass

    def set_inventory(self, newItem):
        """
        Appends an item to the inventory list. Also applies to NPC's and Enemies,
        so we could have a stealing mechanic that wouldn't be too hard to add. 
        """
        pass
    
    
    def set_hp(self, damage):
        """
        Changes hp. I don't want to call the death function here incase we
        want cool stuff when things die, like acid blood or special circumstances
        """
        self.hp -= damage

    def death(self):
        """
        Takes care of the minutia of dying like removing the sprite and whatnot
        """
        pass

class Player(Controller):

    def __init__(self):
        self.standing = []      # An array of int that express how much everyone likes them
        self.progression = {}  # A dictionary with story points as keys and bollean values


    def get_input(self):                        #Roberto
        """
        Ideally, the controller class has all the logical functions that 
        actually do stuff, and this one just calls the right ones at the 
        right times.
        """
        pass

    def show_UI(self):                          #Miseal
        """
        I honestly don't really know how to do this one.
        """
        pass

    def set_standing(self, group, adjustment, needMany):
        """
        Takes an int cooresponding to the index for the group whose 
        standing is being adjusted and how much the standing is changing,
        and changes it. As you would expect. Also called when character
        is created. needMany is a bool. If true, you can change many groups
        at once. You just pass in arrays instead for group and adjustment.
        """

        if needMany:
            for i in range(len(group)):
                self.standing[group[i]] += adjustment[i]
        else:
            self.standing[group] += adjustment

    def get_progression(self):
        """
        Just returns progression
        """
        pass


class Enemy(Controller):
    def __init__(self, dropChance):
        super.__init__()
        self.dropChance = dropChance    # How likely they are to drop stuff when they die, which could be nice to change for different enemies
        


class Bad_Guy(Enemy):
    '''
    Generic enemy subclass format
    '''
    def __init__(self):
        super.__init__(50)
        
    def descion_maker(self):
        """
        This one's going to be complex, and hopefully has some shortcuts in arcade.
        """
        pass

class NPC(Controller):
    '''
    NPC's are going to be essentially the same as enemies (by design), but we can
    strip whatever functionality we need to, like some don't move, only a few have 
    stuff to trade or steal, and so on. As we write the story, these are going to 
    end up being on of the most time consuming parts, as we'll probably have to add 
    dialog/ quests to each one. I figure we can have a dictionary in another file 
    with all the info for the specific NPC's, like we can have basic guards that 
    are just carbon copies of each other, and then we can have more integral 
    characters be more specific, including being able to have certian enemies 
    have more stuff, or something.
    '''
    def __init__(self, quest):
        super.__init__()
        # self.dialog = lines[Player.get_progression()]        or something like that
        self.quest = quest                                  # quests can also just have some Null value if they don't have a quest to give

    def show_trade_window(self, inventory):                 #Misael
        """
        Shows a UI thing that lets you buy stuff. Probably would iterate through 
        the two inventories and put them in some fancy table thing.
        """
        pass


    
Controller(1280, 720, "window")
arcade.run()