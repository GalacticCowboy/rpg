# Adding the other block sprites to the wall list
        for x in self.switch_blocks_list:
            self.wall_list.append(x)
        
        for x in self.breakable_blocks_list:
            self.wall_list.append(x)

        for x in self.locked_blocks_list:
            self.wall_list.append(x)
            
# this is within setup class
