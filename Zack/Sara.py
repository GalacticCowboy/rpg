import arcade
import os
UP_FACING = 0
LEFT_FACING = 1
DOWN_FACING = 2
RIGHT_FACING = 3
CHARACTER_SCALING = 0.5
UPDATES_PER_FRAME = 5

def get_texture(filename, x, y):
    """
    Load a texture from the sprite sheet.
    Up: y = 8, Left: y = 9, Down: y = 10, Right: y = 11.
    Cycle through x from 0 to 8.
    """
    return arcade.load_texture(filename, x * 64, y * 64, width=64, height=64)

class Sara(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = UP_FACING
        self.hp = 100
        self.ammo = 20
        self.view_position = self.position
        self.speed = 5

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Path to Sara sprite sheet
        self.file_path = os.path.dirname(os.path.abspath(__file__)) + \
        "/Sprites/SaraFullSheet.png"

        # Load textures
        self.textures = []
        direction_set = []
        for y in range(8, 12):
            direction_set = []
            for x in range(9):
                direction_set.append(get_texture(self.file_path, x, y))
            self.textures.append(direction_set)

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to change direction
        if self.change_y < 0 and self.character_face_direction != DOWN_FACING:
            self.character_face_direction = DOWN_FACING
        elif self.change_y > 0 and self.character_face_direction != UP_FACING:
            self.character_face_direction = UP_FACING
        elif self.change_x < 0 and self.character_face_direction != LEFT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction != RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        # print(self.textures[0][0])
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.textures[0][0]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 8 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.textures[direction][frame]
