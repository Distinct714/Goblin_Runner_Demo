# LEVEL DISPLAY MANAGEMENT SYSTEM

import pygame as pg

class LevelDisplay:
    
    def __init__(self, screen_width, screen_height, level_font_size=60, level_text_pos_y=50):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load and scale background images for each level.
        self.backgrounds = {
            1: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl1.png"), (self.screen_width, self.screen_height)),
            2: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl2.png"), (self.screen_width, self.screen_height)),
            3: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl3.png"), (self.screen_width, self.screen_height))
        }

        # Set the custom font for all text.
        self.font_path = "GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf"

        # Customize Font and color for level numbers.
        self.level_font = pg.font.Font(self.font_path, level_font_size)
        self.level_text_color = (0, 0, 0)
        self.level_text_pos_y = level_text_pos_y

        # Customize Fonts and colors for "Thank You" screen.
        self.thank_you_font = pg.font.Font(self.font_path, 100)
        self.thank_you_color = (255, 255, 0)
        self.menu_prompt_font = pg.font.Font(self.font_path, 60)
        self.menu_prompt_color = (200, 200, 200)

        # Customize Font and color for "Game Over" screen.
        self.game_over_font = pg.font.Font(self.font_path, 100)
        self.game_over_color = (255, 0, 0)

        # Tutorial state and setup.
        self.tutorial_active = False
        self.tutorial_step = 0
        
        # Create a list for tutorial prompts: key, instruction, box color.
        self.tutorial_prompts = [
            ('A', "Press A to move left.", (0, 0, 0, 200)),
            ('D', "Press D to move right.", (0, 0, 0, 200)),
            ('SPACE', "Press Space to jump.", (0, 0, 0, 200)),
        ]

        # Customize Font and color for tutorial text.
        self.tutorial_font = pg.font.Font(self.font_path, 50)
        self.tutorial_text_color = (255, 255, 255)

        # Customize Font and color for tutorial title.
        self.tutorial_title_font = pg.font.Font(self.font_path, 100)
        self.tutorial_title_color = (0, 0, 0)

        # Customize tutorial box dimensions and position.
        self.tutorial_rect_width = self.screen_width * 0.5
        self.tutorial_rect_height = self.screen_height * 0.1
        self.tutorial_rect_y_offset = self.screen_height * 0.50

        # Map string keys to Pygame key constants.
        self._key_map = {
            'A': pg.K_a,
            'D': pg.K_d,
            'SPACE': pg.K_SPACE,
        }

        # Keep track of keys from the last frame to detect new presses.
        self._previous_keys_pressed = pg.key.get_pressed()
        self.current_expected_pg_key = None

    def draw_background(self, screen, current_level):
        # Shows the right background image for the current level.
        if current_level in self.backgrounds:
            screen.blit(self.backgrounds[current_level], (0, 0))
        else:
            # If no specific background, fill the screen black.
            screen.fill((0, 0, 0))

    def draw_level_text(self, screen, current_level):
        # Customize and display "Level X" text at the top of the screen.
        if current_level <= 3:
            text_surface = self.level_font.render(f"Level {current_level}", True, self.level_text_color)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.level_text_pos_y))
            screen.blit(text_surface, text_rect)

    def _draw_thank_you_screen(self, screen):
        # Shows the "Thank You for Playing" message and menu prompt.
        
        # A background color for "Thank You for Playing" message
        screen.fill((0, 0, 0))
        
        # Customize the position and color of "Thank You for Playing" message and menu prompt.
        message_surface = self.thank_you_font.render("Thank You For Playing Our Game!", True, self.thank_you_color)
        message_rect = message_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(message_surface, message_rect)

        menu_prompt_surface = self.menu_prompt_font.render("Press SPACE to go back to Main Menu", True, self.menu_prompt_color)
        menu_prompt_rect = menu_prompt_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(menu_prompt_surface, menu_prompt_rect)

    def _draw_game_over_screen(self, screen):
        # Shows the "GAME OVER!" message and menu prompt.
        screen.fill((0, 0, 0))
        
         # Customize the position and color of "GAME OVER!" message and menu prompt.
        game_over_surface = self.game_over_font.render("GAME OVER!", True, self.game_over_color)
        game_over_rect = game_over_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(game_over_surface, game_over_rect)

        menu_prompt_surface = self.menu_prompt_font.render("Press SPACE to return to Main Menu", True, self.menu_prompt_color)
        menu_prompt_rect = menu_prompt_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(menu_prompt_surface, menu_prompt_rect)

    def start_tutorial(self):
        # Starts the tutorial, setting it to the first step.
        self.tutorial_active = True
        self.tutorial_step = 0
        
        # Set the first expected key for the tutorial.
        if self.tutorial_prompts:
            self.current_expected_pg_key = self._key_map.get(self.tutorial_prompts[self.tutorial_step][0])
        else:
            # Turn off tutorial if no prompts.
            self.tutorial_active = False
            self.current_expected_pg_key = None

        # Reset key state.
        self._previous_keys_pressed = pg.key.get_pressed()

    def reset_tutorial(self):
        # Turns off and resets the tutorial to the beginning.
        self.tutorial_active = False
        self.tutorial_step = 0
        self.current_expected_pg_key = None
        self._previous_keys_pressed = pg.key.get_pressed()

    def update_and_draw_tutorial(self, screen, current_keys_pressed):
        # Manages the tutorial progression and draws tutorial messages.
        # Returns True when the tutorial is finished.

        # Stop tutorial if done or inactive.
        if not self.tutorial_active or self.tutorial_step >= len(self.tutorial_prompts):
            self.tutorial_active = False 
            return True

        # Draw the "Tutorial" title.
        title_surface = self.tutorial_title_font.render("Tutorial", True, self.tutorial_title_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.tutorial_rect_y_offset - 80))
        screen.blit(title_surface, title_rect)

        key_string, prompt_text, rect_color = self.tutorial_prompts[self.tutorial_step]
        expected_pg_key = self._key_map.get(key_string)

        # Check if the correct key is pressed to advance the tutorial.
        if expected_pg_key:
            key_pressed_now = current_keys_pressed[expected_pg_key]
            key_was_pressed_before = self._previous_keys_pressed[expected_pg_key]

            if (key_string in ['A', 'D'] and key_pressed_now) or \
               (key_string == 'SPACE' and key_pressed_now and not key_was_pressed_before):
                self.tutorial_step += 1 # Move to next tutorial step.

                # If there are more steps, update the expected key.
                if self.tutorial_step < len(self.tutorial_prompts):
                    self.current_expected_pg_key = self._key_map.get(self.tutorial_prompts[self.tutorial_step][0])
                else:
                    self.tutorial_active = False # Tutorial is complete.
                    return True

        # Save current key states for the next check.
        self._previous_keys_pressed = current_keys_pressed

        # Draw the semi-transparent box for tutorial text.
        box_surface = pg.Surface((self.tutorial_rect_width, self.tutorial_rect_height), pg.SRCALPHA)
        box_surface.fill(rect_color)
        box_x = (self.screen_width - self.tutorial_rect_width) // 2
        box_y = self.tutorial_rect_y_offset
        screen.blit(box_surface, (box_x, box_y))

        # Draw the tutorial instruction text inside the box.
        text_surface = self.tutorial_font.render(prompt_text, True, self.tutorial_text_color)
        text_rect = text_surface.get_rect(center=(box_x + self.tutorial_rect_width // 2, box_y + self.tutorial_rect_height // 2))
        screen.blit(text_surface, text_rect)

         # Tutorial is still running.
        return False
