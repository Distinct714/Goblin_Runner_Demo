import pygame as pg
import random 

class Enemy:
    """
    Manages enemy data for different levels, including their static image and movement.
    This version uses a single image per enemy and introduces random left/right movement.
    """
    def __init__(self, screen_width, screen_height, max_level):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_level = max_level

        # Dictionary to store per-level enemy configurations and their dynamic states
        self.level_enemies_data = {} 

        print("DEBUG: EnemySystem: Initializing all enemy data...")
        self._initialize_all_enemies_data()
        print(f"DEBUG: EnemySystem: Data initialized for {len(self.level_enemies_data)} levels.")

        # Placeholders for the 'current' image and rect, which will be updated
        # based on the active level in update/draw methods.
        self.image = None # Holds the image of the enemy for the current level
        self.rect = pg.Rect(0, 0, 0, 0) # Holds the rect of the enemy for the current level

    def _initialize_all_enemies_data(self):
        """
        Populates self.level_enemies_data with initial configurations for each level.
        Each enemy will have a single, static image.
        """
        enemy_size = (80, 80) # Consistent size for all enemies

        for level in range(1, self.max_level + 1):
            # Initial position can be random or fixed
            enemy_x = random.randint(self.screen_width // 4, self.screen_width * 3 // 4 - enemy_size[0]) 
            enemy_y = self.screen_height - 220
            enemy_speed = 3 + (level * 0.5) # Speed increases with level

            image_path = ''
            
            # Define the single image path for each level's enemy
            # ENSURE THESE IMAGE FILES EXIST IN YOUR 'assets' FOLDER!
            if level == 1:
                image_path = 'GAME_DEV_FINAL/assets/sprite/pixel-frame-slime_right/1.png' # Example image for Level 1 enemy
            elif level == 2:
                image_path = 'GAME_DEV_FINAL/assets/sprite/pixel-frame-goblin_right/1.png' # Example image for Level 2 enemy
            elif level == 3:
                image_path = 'GAME_DEV_FINAL/assets/sprite/pixel-frame-ogre_right/1.png' # Example image for Level 3 enemy
            
            loaded_image = None
            if image_path:
                # Removed: try-except block
                original_img = pg.image.load(image_path).convert_alpha()
                loaded_image = pg.transform.scale(original_img, enemy_size)
                print(f"DEBUG: Loaded image '{image_path}' for level {level}.")
            
            # Fallback to a placeholder image if loading fails or no path was defined
            # This part will now only be reached if image_path is empty,
            # otherwise, Pygame will raise an error if image loading fails.
            if loaded_image is None:
                print(f"Error: No valid image path defined for level {level}. Creating emergency placeholder.")
                placeholder = pg.Surface(enemy_size)
                placeholder.fill((255, 0, 0)) # Red placeholder
                loaded_image = placeholder

            # Store the initial state for each level's enemy
            self.level_enemies_data[level] = {
                'speed': enemy_speed,
                'original_x': enemy_x,
                'original_y': enemy_y,
                'image': loaded_image, # Store the single loaded image
                'rect': loaded_image.get_rect(x=enemy_x, y=enemy_y), # Initial rect for the level
                'direction': random.choice([-1, 1]), # Start moving left (-1) or right (1) randomly
                'can_move': False # Initialize enemy as not moving
            }
            print(f"DEBUG: Initialized enemy data for level {level}. Rect: {self.level_enemies_data[level]['rect']}")

    def update(self, current_level):
        """
        Updates the enemy for the current level based on its stored state.
        Movement only occurs if 'can_move' is True for the current enemy.
        """
        if current_level not in self.level_enemies_data:
            self.image = None
            self.rect = pg.Rect(0, 0, 0, 0) # Set to empty rect if no enemy data
            return

        enemy_data = self.level_enemies_data[current_level]

        # Movement logic only if 'can_move' is True
        if enemy_data['can_move']:
            # Update position
            enemy_data['rect'].x += enemy_data['speed'] * enemy_data['direction']

            # Reverse direction if hitting screen edges
            # Add a small buffer so they don't get stuck precisely on the edge
            if enemy_data['rect'].right >= self.screen_width - 10: 
                enemy_data['direction'] = -1
            elif enemy_data['rect'].left <= 10:
                enemy_data['direction'] = 1
        
        # Always update the EnemySystem's current image and rect to the active enemy's
        self.image = enemy_data['image']
        self.rect = enemy_data['rect'] 

    def draw(self, screen, current_level):
        """
        Draws the active enemy for the current level on the screen.
        """
        # Only draw if the current level is a gameplay level (not game over/completion)
        # And ensure image and rect are valid
        if self.image and self.rect and current_level <= self.max_level: 
            screen.blit(self.image, self.rect)

    def reset_for_level(self, level):
        """
        Resets the position and movement state of the enemy for a specific level.
        Also resets 'can_move' to False.
        """
        if level in self.level_enemies_data:
            enemy_data = self.level_enemies_data[level]
            # Reset to original position but keep it random
            enemy_data['rect'].x = random.randint(self.screen_width // 4, self.screen_width * 3 // 4 - enemy_data['rect'].width) 
            enemy_data['rect'].y = enemy_data['original_y'] # Y remains constant
            enemy_data['direction'] = random.choice([-1, 1]) # Randomize initial direction for next level
            enemy_data['can_move'] = False 
            print(f"DEBUG: Enemy for level {level} reset.")

    def reset_all_enemies(self):
        """
        Resets the position and movement state of all managed enemies.
        Also resets 'can_move' to False for all.
        """
        for level_data in self.level_enemies_data.values():
            level_data['rect'].x = random.randint(self.screen_width // 4, self.screen_width * 3 // 4 - level_data['rect'].width)
            level_data['rect'].y = level_data['original_y']
            level_data['direction'] = random.choice([-1, 1])
            level_data['can_move'] = False 
        print("DEBUG: All enemies reset.")

    def start_movement_for_level(self, level):
        """
        Sets the 'can_move' flag to True for the enemy at the specified level.
        """
        if level in self.level_enemies_data:
            self.level_enemies_data[level]['can_move'] = True
            print(f"DEBUG: Enemy for level {level} can now move.")

    def get_current_enemy_rect(self, current_level):
        """
        Returns the Pygame Rect object for the enemy of the current level.
        This is used primarily for collision detection.
        """
        if current_level in self.level_enemies_data and self.level_enemies_data[current_level]['rect']:
            return self.level_enemies_data[current_level]['rect']
        return pg.Rect(0, 0, 0, 0) # Return an empty rect if no enemy for level or if rect is None