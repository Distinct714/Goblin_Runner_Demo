# ENEMY MANAGEMENT SYSTEM

import pygame as pg
import random 

class Enemy:

    def __init__(self, screen_width, screen_height, max_level):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_level = max_level

        # Define custom sizes for each enemy types (width, height), where the keys are the levels.
        self.enemy_sizes = {
            1: (180, 180),
            2: (150, 150),
            3: (210, 210)
        }

        # Define custom initial positions for EACH enemy.
        self.enemy_initial_positions = {
            1: [(self.screen_width * 3 // 4 - 75, self.screen_height - 260)],
            2: [ # Three Goblins
                (self.screen_width * 1 // 5, self.screen_height - 240),
                (self.screen_width // 2 - 50, self.screen_height - 240),
                (self.screen_width * 3 // 4 - 90, self.screen_height - 240)
            ],
            3: [# Single Ogre
                (self.screen_width * 1 // 1 - 5, self.screen_height - 330),
                (self.screen_width * 2 // 7 - 110, self.screen_height - 330),
                (self.screen_width * 3 // 4 - 200, self.screen_height - 330)
            ] 
        }

        # --- Define Enemy Animation Image Paths ---
        # Each level/enemy type now has 'left' and 'right' animation lists
        self.enemy_animation_paths = {
            1: { # Slime
                'left': [
                    "GAME_DEV_FINAL/assets/sprite/slime/1.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/2.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/3.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/4.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/5.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/6.png"
                ],
                'right': [
                    "GAME_DEV_FINAL/assets/sprite/slime/1.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/2.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/3.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/4.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/5.png",
                    "GAME_DEV_FINAL/assets/sprite/slime/6.png"
                ]
            },
            2: { # Goblin
                'left': [
                    "GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_left/1.png",
                    "GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_left/2.png",
                    "GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_left/3.png",
                    "GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_left/4.png"
                ],
                'right': [
                    "GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_right/1.png",
                    "GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_right/2.png",
                    "GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_right/3.png",
                    "GAME_DEV_FINAL/assets/sprite/goblin/pixel-frame-goblin_right/4.png"
                ]
            },
            3: { # Ogre
                'left': [
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_left/1.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_left/2.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_left/3.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_left/4.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_left/5.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_left/6.png"
                ],
                'right': [
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_right/1.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_right/2.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_right/3.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_right/4.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_right/5.png",
                    "GAME_DEV_FINAL/assets/sprite/ogre/pixel-frame-ogre_right/6.png"
                ]
            }
        }

        # self.level_enemies_data will now store a LIST of enemy dicts for each level
        self.level_enemies_data = {} 
        self._initialize_all_enemies_data()

        # These are no longer needed to store the *current* enemy's image/rect
        # as update/draw will operate on the list of enemies directly.
        # self.image = None 
        # self.rect = pg.Rect(0, 0, 0, 0) 

    def _initialize_all_enemies_data(self):
        """
        Populates self.level_enemies_data with initial configurations for each level's enemy(ies),
        including loading their animation frames.
        """
        for level in range(1, self.max_level + 1):
            animation_paths_for_level = self.enemy_animation_paths.get(level)
            enemy_size = self.enemy_sizes.get(level, (80, 80)) # Get custom size or default
            initial_positions_for_level = self.enemy_initial_positions.get(level, [])

            # Load animation frames for left and right directions for this level's enemy type
            loaded_animations = {
                'left': [],
                'right': []
            }
            if animation_paths_for_level:
                for direction_key in ['left', 'right']:
                    paths = animation_paths_for_level.get(direction_key, [])
                    for path in paths:
                        original_img = pg.image.load(path).convert_alpha()
                        scaled_img = pg.transform.scale(original_img, enemy_size)
                        loaded_animations[direction_key].append(scaled_img)

            # Ensure there's at least one frame even if loading failed for all (critical for modulo)
            # This part serves as a fallback to prevent errors if image lists are empty.
            if not loaded_animations['left']:
                placeholder = pg.Surface(enemy_size)
                placeholder.fill((255, 0, 0))
                loaded_animations['left'].append(placeholder)
            if not loaded_animations['right']:
                placeholder = pg.Surface(enemy_size)
                placeholder.fill((255, 0, 0))
                loaded_animations['right'].append(placeholder)

            # Create enemy data for each enemy in this level
            self.level_enemies_data[level] = [] # Initialize as a list
            for i, (enemy_x, enemy_y) in enumerate(initial_positions_for_level):
                enemy_speed = (3 + (level * 0.5)) + (i * 0.2) # Slightly vary speed if multiple enemies
                initial_direction = random.choice([-1, 1]) # -1 for left, 1 for right
                initial_animation_set = 'right' if initial_direction == 1 else 'left'

                enemy_data = {
                    'speed': enemy_speed,
                    'animations': loaded_animations, # All enemies of this level share the same loaded animation frames
                    'rect': pg.Rect(enemy_x, enemy_y, enemy_size[0], enemy_size[1]), # Use initial rect
                    'direction': initial_direction,
                    'can_move': False, # Enemy starts static
                    'initial_x': enemy_x, # Store for reset
                    'initial_y': enemy_y, # Store for reset
                    'current_frame_index': 0, # Current frame for animation
                    'animation_frame_counter': 0, # Counter to control animation speed
                    'animation_speed_frames': 16, # Number of game frames per animation sprite
                    'current_animation_set': initial_animation_set # 'left' or 'right'
                }
                # Set the initial image for this specific enemy data entry
                if enemy_data['animations'][initial_animation_set]:
                    enemy_data['image'] = enemy_data['animations'][initial_animation_set][0]
                else:
                    enemy_data['image'] = loaded_animations['right'][0] # Fallback to a default if initial set is empty
                
                self.level_enemies_data[level].append(enemy_data)


    def update(self, current_level, character_rect):
        """
        Updates all enemies for the current level. Handles horizontal movement
        and boundary checks, and updates animation frames for each enemy.
        """
        if current_level not in self.level_enemies_data or not self.level_enemies_data[current_level]:
            # No enemies for this level, or list is empty
            return

        # Iterate through each enemy at the current level
        for enemy_data in self.level_enemies_data[current_level]:
            if enemy_data['can_move']:
                # Independent horizontal movement
                enemy_data['rect'].x += enemy_data['speed'] * enemy_data['direction']

                # Reverse direction upon hitting screen edges and update animation set
                if enemy_data['rect'].right >= self.screen_width - 10: 
                    enemy_data['direction'] = -1
                    enemy_data['current_animation_set'] = 'left'
                elif enemy_data['rect'].left <= 10:
                    enemy_data['direction'] = 1
                    enemy_data['current_animation_set'] = 'right'
                
                # --- Animation Update Logic ---
                enemy_data['animation_frame_counter'] += 1
                if enemy_data['animation_frame_counter'] >= enemy_data['animation_speed_frames']:
                    enemy_data['animation_frame_counter'] = 0
                    current_anim_set = enemy_data['animations'][enemy_data['current_animation_set']]
                    if current_anim_set: # Ensure there are frames in the current animation set
                        enemy_data['current_frame_index'] = (enemy_data['current_frame_index'] + 1) % len(current_anim_set)
                    else:
                        enemy_data['current_frame_index'] = 0 # Fallback

                # Update the image to the current animation frame
                current_anim_set = enemy_data['animations'][enemy_data['current_animation_set']]
                if current_anim_set and len(current_anim_set) > enemy_data['current_frame_index']:
                    enemy_data['image'] = current_anim_set[enemy_data['current_frame_index']]
                else:
                    # Fallback if animation set or index is somehow invalid
                    enemy_data['image'] = enemy_data['animations']['right'][0] # Default to first right frame

    def draw(self, screen, current_level):
        """
        Draws all active enemies for the current level on the screen.
        """
        if current_level not in self.level_enemies_data:
            return # No enemies for this level

        for enemy_data in self.level_enemies_data[current_level]:
            # Only draw if there's a valid image and rect
            if 'image' in enemy_data and 'rect' in enemy_data:
                screen.blit(enemy_data['image'], enemy_data['rect'])

    def reset_for_level(self, level):
        """
        Resets all enemies for a specific level to their defined initial positions and pauses their movement.
        Also resets their animation states.
        """
        if level in self.level_enemies_data:
            for enemy_data in self.level_enemies_data[level]:
                enemy_data['rect'].x = enemy_data['initial_x'] # Reset to defined initial X
                enemy_data['rect'].y = enemy_data['initial_y'] # Reset to defined initial Y
                
                enemy_data['direction'] = random.choice([-1, 1]) # Still randomize initial direction
                enemy_data['current_animation_set'] = 'right' if enemy_data['direction'] == 1 else 'left'
                
                enemy_data['can_move'] = False 
                
                enemy_data['current_frame_index'] = 0 # Reset animation frame
                enemy_data['animation_frame_counter'] = 0 # Reset animation counter
                
                # Update the image to the first frame of the new initial animation set
                if enemy_data['animations'][enemy_data['current_animation_set']]:
                    enemy_data['image'] = enemy_data['animations'][enemy_data['current_animation_set']][0]
                else:
                    enemy_data['image'] = enemy_data['animations']['right'][0] # Fallback


    def reset_all_enemies(self):
        """
        Resets all enemies across all levels to their defined initial positions and pauses their movement.
        Also resets their animation states.
        """
        for level_enemies_list in self.level_enemies_data.values():
            for enemy_data in level_enemies_list:
                enemy_data['rect'].x = enemy_data['initial_x'] # Reset to defined initial X
                enemy_data['rect'].y = enemy_data['initial_y'] # Reset to defined initial Y
                
                enemy_data['direction'] = random.choice([-1, 1])
                enemy_data['current_animation_set'] = 'right' if enemy_data['direction'] == 1 else 'left'
                
                enemy_data['can_move'] = False 
                
                enemy_data['current_frame_index'] = 0 # Reset animation frame
                enemy_data['animation_frame_counter'] = 0 # Reset animation counter

                # Update the image to the first frame of the new initial animation set
                # Fixed: Changed 'level_data' to 'enemy_data' to reference the current enemy's data
                if enemy_data['animations'][enemy_data['current_animation_set']]: 
                    enemy_data['image'] = enemy_data['animations'][enemy_data['current_animation_set']][0]
                else:
                    enemy_data['image'] = enemy_data['animations']['right'][0] # Fallback


    def start_movement_for_level(self, level):
        """
        Enables movement for all enemies at the specified level.
        """
        if level in self.level_enemies_data:
            for enemy_data in self.level_enemies_data[level]:
                enemy_data['can_move'] = True

    def get_current_enemy_rects(self, current_level): # Renamed method for clarity
        """
        Returns a list of Pygame Rect objects for all enemies of the current level for collision detection.
        Returns an empty list if no enemy data exists for the level.
        """
        if current_level in self.level_enemies_data:
            return [enemy_data['rect'] for enemy_data in self.level_enemies_data[current_level]]
        return [] # Return an empty list if no enemies for level
