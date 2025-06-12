# CHARACTER MANAGEMENT SYSTEM

import pygame as pg

class Character:
    # Stores all the image file paths for character animations.
    CHARACTER_ANIMATIONS = {
        # Images for standing still, facing left.
        "idle_left": [
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji standing left/standing1 left.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji standing left/standing2 left.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji standing left/standing3 left.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji standing left/standing4 left.png"
        ],

        # Images for standing still, facing right.
        "idle_right": [
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji standing right/standing1.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji standing right/standing2.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji standing right/standing3.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji standing right/standing4.png"
        ],

        # Images for walking left.
        "left": [
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji walking left/walking1 left.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji walking left/walking2 left.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji walking left/walking3 left.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji walking left/walking4 left.png"
        ],

        # Images for walking right.
        "right": [
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji walking right/walking1.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji walking right/walking2.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji walking right/walking3.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji walking right/walking4.png"
        ],

        # Images for jumping left.
        "jump_left": [
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji jump left/jump1 left.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji jump left/jump2 left.png"
        ],

        # Images for jumping right.
        "jump_right": [
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji jump right/jump1.png",
            "GAME_DEV_FINAL/assets/sprite/shinji/shinji jump right/jump2.png"
        ]
    }

    def __init__(self, screen_width, screen_height, start_x, start_y, character_size):
        # Save the game screen's width and height.
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Save the character's size.
        self.character_size = character_size

        # Create a rectangle that represents the character's position and size.
        self.rect = pg.Rect(start_x, start_y, self.character_size, self.character_size)
        
        # Set the character's horizontal movement speed.
        self.speed = 20

        # Tracks if the character is currently jumping.
        self.is_jumping = False

        # The character's upward or downward speed during a jump.
        self.vertical_velocity = 0

        # Set the high jump for character (negative for moving up).
        self.jump_power = -45

        # Set the gravity that pulls the character down.
        self.gravity = 3

        # The y-coordinate where the character stands on the ground.
        self.initial_y = start_y

        # Hold all the loaded animation images for each direction.
        self.character_animations = {
            "idle_left": [], 
            "idle_right": [],
            "left": [], 
            "right": [],
            "jump_left": [], 
            "jump_right": []
        }
        
        # Remembers the last horizontal direction the character was facing.
        self._last_horizontal_direction = "right"

        # The name of the animation currently being shown. (The fixed animation in every levels after dialogue)
        self.current_direction = "idle_right"

        # The index of the current image within the active animation list.
        self.current_frame_index = 0

        # How many game frames pass before the animation image changes.
        self.animation_speed_frames = 5

        # Counts game frames to control animation speed.
        self.animation_frame_counter = 0

        # Loop through all animation directions and their image paths.
        for direction, paths in self.CHARACTER_ANIMATIONS.items():
            for path in paths:
                # Load the image from the file
                image = pg.image.load(path).convert_alpha()

                # Scale the image to the correct character size.
                image = pg.transform.scale(image, (self.character_size, self.character_size))

                # Add the loaded image to the correct animation list.
                self.character_animations[direction].append(image)
        
        # Set the character's first image to be displayed.
        self.image = self.character_animations[self.current_direction][self.current_frame_index]

    def update(self, keys):
        # This function updates the character's position, handles jumps, and changes animations.
        moving_horizontally = False
        
        # Check if 'A' key is pressed for left movement and 'D' is not.
        if keys[pg.K_a] and not keys[pg.K_d]:
            self.rect.x -= self.speed
            self._last_horizontal_direction = "left"
            moving_horizontally = True

        # Check if 'D' key is pressed for right movement and 'A' is not.
        elif keys[pg.K_d] and not keys[pg.K_a]:
            self.rect.x += self.speed
            self._last_horizontal_direction = "right"
            moving_horizontally = True
        
        # Stop the character from moving off the left or right side of the screen.
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.character_size))

        # Check if the character is currently jumping.
        if self.is_jumping:
            self.vertical_velocity += self.gravity
            # Move the character up or down based on vertical speed.
            self.rect.y += self.vertical_velocity
            
            # If the character hits or goes below the ground level:
            if self.rect.y >= self.initial_y:
                # Set character back to ground level.
                self.rect.y = self.initial_y
                self.is_jumping = False
                self.vertical_velocity = 0
        
        # Decide which animation name to use based on character's state.
        if self.is_jumping:
            # If jumping, use the jump animation for the last horizontal direction.
            target_direction = f"jump_{self._last_horizontal_direction}"
        elif moving_horizontally:
            # If moving horizontally, use the walking animation for that direction.
            target_direction = self._last_horizontal_direction
        else:
            # If not jumping or moving, use the idle animation for the last horizontal direction.
            target_direction = f"idle_{self._last_horizontal_direction}"

        # If the animation direction has changed:
        if target_direction != self.current_direction:
            # Set the new current animation direction.
            self.current_direction = target_direction

            self.current_frame_index = 0
            self.animation_frame_counter = 0

        # If character is jumping or moving horizontally:
        if self.is_jumping or moving_horizontally:
            self.animation_frame_counter += 1
        
            # If enough frames have passed to change the animation image:
            if self.animation_frame_counter >= self.animation_speed_frames:
                self.animation_frame_counter = 0

                # Get the list of images for the current animation.
                current_anim_set = self.character_animations.get(self.current_direction)
                
                # If there are images in this animation set:
                if current_anim_set:
                    # Move to the next image in the animation loop.
                    self.current_frame_index = (self.current_frame_index + 1) % len(current_anim_set)
                else:
                    self.current_frame_index = 0

        elif not self.is_jumping and not moving_horizontally:
            self.current_frame_index = 0
            self.animation_frame_counter = 0

        # Set the image to be shown on screen for the character.
        # It gets the image from the current animation set, using the current frame index.
        # If the current direction isn't found, it defaults to the first idle_right image.
        self.image = self.character_animations.get(self.current_direction, self.character_animations["idle_right"])[self.current_frame_index]

    def draw(self, screen):
        # Draws the character's current image onto the game screen at its position.
        screen.blit(self.image, self.rect)

    def jump(self):
        # Allows the character to jump if they are on the ground.
        if not self.is_jumping:
            self.is_jumping = True
            self.vertical_velocity = self.jump_power
