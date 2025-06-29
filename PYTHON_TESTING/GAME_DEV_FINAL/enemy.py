# Enemy Management System

import pygame as pg
import random

class Enemy:
    # Stores paths to animation images for each enemy type by level and direction.
    ENEMY_ANIMATION_PATHS = {
        1: { # Level 1 enemies (Slimes)
            'left': [f"GAME_DEV_FINAL/assets/sprite/slime/{i}.png" for i in range(1, 7)], 
            'right': [f"GAME_DEV_FINAL/assets/sprite/slime/{i}.png" for i in range(1, 7)] 
            },

        2: { # Level 2 enemies (Goblins)
            'left': [f"GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_left/{i}.png" for i in range(1, 5)],
            'right': [f"GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_right/{i}.png" for i in range(1, 5)]
            },

        3: { # Level 3 enemies (Ogres)
            'left': [f"GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_left/{i}.png" for i in range(1, 7)],
            'right': [f"GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_right/{i}.png" for i in range(1, 7)]
            }
    }

    # Defines the image size (width, height) for each enemy type.
    ENEMY_SIZES = {
        1: (180, 180),
        2: (155, 155),
        3: (210, 210)
    }

    def __init__(self, screen_width, screen_height, max_level):
        # Stores the game screen's width and height.
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Stores the highest level number in the game.
        self.max_level = max_level

        # Defines the enemy's starting position in the game for different levels.
        self.enemy_initial_positions = {
            1: [(self.screen_width * 3 // 4 - 75, self.screen_height - 260)],

            2: [(self.screen_width * 1 // 5, self.screen_height - 251),
                (self.screen_width // 2 - 50, self.screen_height - 251),
                (self.screen_width * 3 // 4 - 90, self.screen_height - 251)],
                
            3: [(self.screen_width * 1 // 1 - 5, self.screen_height - 330),
                (self.screen_width * 2 // 7 - 110, self.screen_height - 330),
                (self.screen_width * 3 // 4 - 230, self.screen_height - 330)]
        }

        # This dictionary will store all the enemy information, grouped by level.
        self.level_enemies_data = {} 
        
        # Calls this method to set up all enemy data when the game starts.
        self.initialize_all_enemies_data() 

    def initialize_all_enemies_data(self):
        # Loops through each game level to set up enemies for it.
        for level in range(1, self.max_level + 1):
            # Gets the image size for enemies in specific level
            enemy_size = self.ENEMY_SIZES.get(level, (80, 80))

            # Create an empty dictionary to hold loaded animation images.
            loaded_animations = {} 

            # Loops through 'left' and 'right' directions to load animations for each.
            for direction in ['left', 'right']:
                # Gets the list of image paths for the current level and direction.
                # Use .get() with empty dicts/lists to handle missing data.
                direction_paths = self.ENEMY_ANIMATION_PATHS.get(level, {}).get(direction, [])

                # Create a list to store loaded images for this direction.
                loaded_images_for_direction = [] 

                # Load and scale the image from the path. Then add the scaled image to the list.
                for path in direction_paths:
                    image = pg.image.load(path).convert_alpha()    
                    scaled_image = pg.transform.scale(image, enemy_size) 
                    loaded_images_for_direction.append(scaled_image)
                
                # Store the list of loaded and scaled images under the current direction.
                loaded_animations[direction] = loaded_images_for_direction

            # Creates an empty list to store individual enemy data for the current level.
            self.level_enemies_data[level] = [] 

            # Goes through each predefined starting position for enemies at this level.
            for i, (enemy_x, enemy_y) in enumerate(self.enemy_initial_positions.get(level, [])):
                # Randomly decides if the enemy starts moving left (-1) or right (1).
                initial_direction = random.choice([-1, 1]) 

                # Sets the starting animation ('left' or 'right') based on the initial direction. (Using ternary)
                initial_animation_set = 'right' if initial_direction == 1 else 'left'


                enemy_data = {
                    # Defines how fast this specific enemy moves, varying by level and index.
                    'speed': (3 + (level * 0.5)) + (i * 0.2), 

                    # Stores all loaded animation images for this enemy type.
                    'animations': loaded_animations,

                    # Creates the enemy's position and size rectangle.
                    'rect': pg.Rect(enemy_x, enemy_y, *enemy_size),

                    # Stores the enemy's current movement direction (-1 for left, 1 for right).
                    'direction': initial_direction,

                    # Flag to control whether the enemy is allowed to move.       
                    'can_move': False,  

                    # Stores the original starting X position for resets.                     
                    'initial_x': enemy_x,        
                    
                    # Stores the original starting Y position for resets.            
                    'initial_y': enemy_y, 

                    # The index of the current image frame in its animation.                   
                    'current_frame_index': 0,      

                    # Counts game frames to control animation speed.          
                    'animation_frame_counter': 0,            

                    # How many game frames pass before the animation changes to the next image.
                    'animation_speed_frames': 5,  

                    # Which set of animations (left or right) is currently active.          
                    'current_animation_set': initial_animation_set 
                }

                # Sets the enemy's displayed image to the first frame of its starting animation.
                enemy_data['image'] = enemy_data['animations'][initial_animation_set][0]

                # Adds this enemy's complete data to the level's list.
                self.level_enemies_data[level].append(enemy_data) 

    def update(self, current_level, character_rect):
        # Updates all enemies in the current level, handling their movement and animation.

        # If no enemies are defined for the current level, stop.
        if current_level not in self.level_enemies_data: 
            return 

        # Loops through each enemy that belongs to the current level.
        for enemy_data in self.level_enemies_data[current_level]:

            if enemy_data['can_move']:
                # Changes the enemy's horizontal position based on its speed and direction.
                enemy_data['rect'].x += enemy_data['speed'] * enemy_data['direction']

                # Checks if the enemy hits the right screen edge. Makes the enemy move to left with animation that faces left.
                if enemy_data['rect'].right >= self.screen_width - 10:
                    enemy_data['direction'] = -1
                    enemy_data['current_animation_set'] = 'left'
                
                # Checks if the enemy hits the left screen edge. Makes the enemy move to right with animation that faces right.
                elif enemy_data['rect'].left <= 10:
                    enemy_data['direction'] = 1
                    enemy_data['current_animation_set'] = 'right'
                
                # Increments the counter for animation frames.
                enemy_data['animation_frame_counter'] += 1 
                
                # If enough frames have passed, switch to the next animation image and resets the counter.
                if enemy_data['animation_frame_counter'] >= enemy_data['animation_speed_frames']:
                    enemy_data['animation_frame_counter'] = 0

                    # Gets the list of images for the current animation direction (left or right).
                    current_anim_set = enemy_data['animations'][enemy_data['current_animation_set']]

                    # Moves to the next animation frame, cycling back to the start if it reaches the end.
                    enemy_data['current_frame_index'] = (enemy_data['current_frame_index'] + 1) % len(current_anim_set)

                # Sets the enemy's displayed image to the current frame of its active animation.
                enemy_data['image'] = enemy_data['animations'][enemy_data['current_animation_set']][enemy_data['current_frame_index']]

    def draw(self, screen, current_level):
        # Draws all active enemies for the given level onto the game screen.

        # Do nothing if no enemies are set up for this level.
        if current_level not in self.level_enemies_data: 
            return 
        
        # Draws the enemy's current image at its position.
        for enemy_data in self.level_enemies_data[current_level]:
            screen.blit(enemy_data['image'], enemy_data['rect']) 

    def reset_for_level(self, level):
        # Resets all enemies in a specific level to their original starting states.
        if level in self.level_enemies_data:
            for enemy_data in self.level_enemies_data[level]:
                
                # Moves enemy back to its initial starting X and Y position.
                enemy_data['rect'].topleft = (enemy_data['initial_x'], enemy_data['initial_y'])

                # Randomly sets a new starting movement direction.
                enemy_data['direction'] = random.choice([-1, 1]) 

                # Updates the animation set based on the new random direction. (Using ternary)
                enemy_data['current_animation_set'] = 'right' if enemy_data['direction'] == 1 else 'left'
                
                # Stops the enemy from moving.
                enemy_data['can_move'] = False 

                # Resets the animation to the first frame.
                enemy_data['current_frame_index'] = 0

                # Resets the animation counter.
                enemy_data['animation_frame_counter'] = 0

                # Sets the enemy's image to the first frame of its newly determined animation set.
                enemy_data['image'] = enemy_data['animations'][enemy_data['current_animation_set']][0]

    def reset_all_enemies(self):
        # Resets all enemies across all levels to their starting positions and states.
        for level in self.level_enemies_data:
            self.reset_for_level(level) 

    def start_movement_for_level(self, level):
        # Enables movement for all enemies in a specific level.
        if level in self.level_enemies_data:

            # Sets the 'can_move' flag to True, allowing the enemy to start moving.
            for enemy_data in self.level_enemies_data[level]:
                enemy_data['can_move'] = True

    def get_current_enemy_rects(self, current_level):
        # Returns a list of the current positions for all enemies in the given level.
        # This list is typically used to check for collisions with other game objects.
        # Uses .get() with an empty list as default to safely handle levels without enemies.
        return [enemy_data['rect'] for enemy_data in self.level_enemies_data.get(current_level, [])]
