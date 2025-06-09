import pygame as pg

class LevelDisplay:

    def __init__(self, screen_width, screen_height, level_font_size=60, level_text_pos_y=50):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load and scale all background images explicitly
        # IMPORTANT: Ensure these paths are correct relative to where your main.py is run.
        self.backgrounds = {
            1: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl1.png"), (self.screen_width, self.screen_height)),
            2: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl2.png"), (self.screen_width, self.screen_height)),
            3: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl3.png"), (self.screen_width, self.screen_height))
        }

        # Font path (used for all custom fonts)
        self.font_path = "GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf"

        # Customizing Level text font and color
        self.level_font = pg.font.Font(self.font_path, level_font_size)
        self.level_text_color = (0, 0, 0) # Black for level number

        # Thank You screen specific fonts and colors
        self.thank_you_font = pg.font.Font(self.font_path, 100)
        self.thank_you_color = (255, 255, 0) # Yellow for emphasis
        self.menu_prompt_font = pg.font.Font(self.font_path, 60)
        self.menu_prompt_color = (200, 200, 200) # Light grey

        # Game Over screen specific fonts and colors
        self.game_over_font = pg.font.Font(self.font_path, 100)
        self.game_over_color = (255, 0, 0) # Red for game over message

        self.level_text_pos_y = level_text_pos_y

        # --- Tutorial Gameplay Specific Variables ---
        self.tutorial_active = False
        self.tutorial_step = 0
        self.tutorial_prompts = [
            ('A', "Press A to move left.", (0, 0, 0, 200)),
            ('D', "Press D to move right.", (0, 0, 0, 200)),
            ('SPACE', "Press Space to jump.", (0, 0, 0, 200)),
        ]
        # This will now store the Pygame key constant directly for comparison
        self.current_expected_pg_key = None 
        self.tutorial_font = pg.font.Font(self.font_path, 30) # Font for tutorial prompts
        self.tutorial_text_color = (255, 255, 255) # White text for tutorial prompts

        # New: Font and color for the "Tutorial" title
        self.tutorial_title_font = pg.font.Font(self.font_path, 60) # Larger font for title
        self.tutorial_title_color = (255, 255, 255) # White title text

        # Tutorial rectangle fixed size/position
        self.tutorial_rect_width = self.screen_width * 0.2
        self.tutorial_rect_height = self.screen_height * 0.1
        self.tutorial_rect_y_offset = self.screen_height * 0.75 # Position from top

        # Mapping key strings to Pygame key constants for internal use
        self._key_map = {
            'A': pg.K_a,
            'D': pg.K_d,
            'SPACE': pg.K_SPACE,
        }
        # Track previous key state to detect key presses (for discrete events like SPACE)
        self._previous_keys_pressed = pg.key.get_pressed()


    def draw_background(self, screen, current_level):
        """Draws the background image for the current level."""
        # Only draw background if it's a regular level (1, 2, or 3)
        if current_level in self.backgrounds:
            screen.blit(self.backgrounds[current_level], (0, 0))
        else:
            # For states like Game Over or Thank You, just draw a plain black background
            screen.fill((0, 0, 0))

    def draw_level_text(self, screen, current_level):
        """Draws the 'Level X' text on the screen."""
        if current_level <= 3: # Display level text for actual levels
            level_text = f"Level {current_level}"
            text_surface = self.level_font.render(level_text, True, self.level_text_color)
            
            # Position the text (horizontally centered, adjustable vertical position)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.level_text_pos_y))
            screen.blit(text_surface, text_rect)

    def _draw_thank_you_screen(self, screen):
        """Helper method to draw the 'Thank You for Playing' screen."""
        screen.fill((0, 0, 0)) # Ensure black background for this screen
        
        end_message = "Thank You For Playing Our Game!"
        message_surface = self.thank_you_font.render(end_message, True, self.thank_you_color)
        message_rect = message_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(message_surface, message_rect)

        menu_prompt = "Press SPACE to go back to Main Menu"
        menu_prompt_surface = self.menu_prompt_font.render(menu_prompt, True, self.menu_prompt_color)
        menu_prompt_rect = menu_prompt_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(menu_prompt_surface, menu_prompt_rect)

    def _draw_game_over_screen(self, screen):
        """Helper method to draw the 'Game Over' screen."""
        screen.fill((0, 0, 0)) # Ensure black background for this screen
        
        game_over_message = "GAME OVER!"
        game_over_surface = self.game_over_font.render(game_over_message, True, self.game_over_color)
        game_over_rect = game_over_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(game_over_surface, game_over_rect)

        menu_prompt = "Press SPACE to return to Main Menu"
        menu_prompt_surface = self.menu_prompt_font.render(menu_prompt, True, self.menu_prompt_color)
        menu_prompt_rect = menu_prompt_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(menu_prompt_surface, menu_prompt_rect)

    # --- TUTORIAL METHODS ---
    def start_tutorial(self):
        """Initializes the tutorial sequence."""
        self.tutorial_active = True
        self.tutorial_step = 0
        if self.tutorial_prompts:
            # Set the expected key based on the first tutorial step
            self.current_expected_pg_key = self._key_map.get(self.tutorial_prompts[self.tutorial_step][0])
        else:
            self.tutorial_active = False # No tutorial steps defined
            self.current_expected_pg_key = None
        self._previous_keys_pressed = pg.key.get_pressed() # Capture initial key state

    def reset_tutorial(self):
        """Resets the tutorial state for a new game."""
        self.tutorial_active = False
        self.tutorial_step = 0
        self.current_expected_pg_key = None
        self._previous_keys_pressed = pg.key.get_pressed() # Reset previous key state too

    def update_and_draw_tutorial(self, screen, current_keys_pressed):
        """
        Updates the tutorial state based on pressed keys and draws the current tutorial step.
        Returns True if the tutorial is completed, False otherwise.
        """
        if not self.tutorial_active:
            return True # Tutorial not active, considered completed

        if self.tutorial_step >= len(self.tutorial_prompts):
            self.tutorial_active = False
            return True # All steps completed

        # Draw the "Tutorial" title above the instruction box
        tutorial_title_surface = self.tutorial_title_font.render("Tutorial", True, self.tutorial_title_color)
        tutorial_title_rect = tutorial_title_surface.get_rect(center=(self.screen_width // 2, self.tutorial_rect_y_offset - 70))
        screen.blit(tutorial_title_surface, tutorial_title_rect)

        # Get current step's info
        key_string, prompt_text, rect_color = self.tutorial_prompts[self.tutorial_step]
        expected_pg_key = self._key_map.get(key_string)

        # Logic to advance tutorial step
        if expected_pg_key:
            # For 'A' and 'D', we check if the key is currently held down
            if key_string in ['A', 'D']:
                if current_keys_pressed[expected_pg_key]:
                    self.tutorial_step += 1
                    # Update the expected key for the next step immediately
                    if self.tutorial_step < len(self.tutorial_prompts):
                        self.current_expected_pg_key = self._key_map.get(self.tutorial_prompts[self.tutorial_step][0])
                    else:
                        self.tutorial_active = False # Tutorial completed
                        return True # Signal tutorial completion
            # For 'SPACE', we need to detect a *single press* (key down then up, or just down).
            # We use the previous frame's key state to detect a new press.
            elif key_string == 'SPACE':
                # Check if SPACE is currently pressed AND was NOT pressed in the previous frame
                if current_keys_pressed[expected_pg_key] and not self._previous_keys_pressed[expected_pg_key]:
                    self.tutorial_step += 1
                    # Update the expected key for the next step immediately
                    if self.tutorial_step < len(self.tutorial_prompts):
                        self.current_expected_pg_key = self._key_map.get(self.tutorial_prompts[self.tutorial_step][0])
                    else:
                        self.tutorial_active = False # Tutorial completed
                        return True # Signal tutorial completion

        # After checking, update the previous_keys_pressed for the next frame
        self._previous_keys_pressed = current_keys_pressed


        # Draw the tutorial rectangle and text
        s = pg.Surface((self.tutorial_rect_width, self.tutorial_rect_height), pg.SRCALPHA)
        s.fill(rect_color)

        rect_x = (self.screen_width - self.tutorial_rect_width) // 2
        rect_y = self.tutorial_rect_y_offset
        screen.blit(s, (rect_x, rect_y))

        text_surface = self.tutorial_font.render(prompt_text, True, self.tutorial_text_color)
        text_rect = text_surface.get_rect(center=(rect_x + self.tutorial_rect_width // 2, rect_y + self.tutorial_rect_height // 2))
        screen.blit(text_surface, text_rect)

        return False # Tutorial not yet completed
