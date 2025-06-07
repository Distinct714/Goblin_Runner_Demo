# level_display_manager.py
import pygame as pg

class LevelDisplay:

    def __init__(self, screen_width, screen_height, level_font_size=60, level_text_pos_y=50):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load and scale all background images explicitly
        self.backgrounds = {
            1: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl1.png"), (self.screen_width, self.screen_height)),
            2: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl2.png"), (self.screen_width, self.screen_height)),
            3: pg.transform.scale(pg.image.load("GAME_DEV_FINAL/assets/background/lvl3.png"), (self.screen_width, self.screen_height))
        }

        # Customizing Level text font and color
        self.level_font = pg.font.Font("GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf", level_font_size)
        self.level_text_color = (0, 0, 0)

        # Thank You screen specific fonts and colors
        self.thank_you_font = pg.font.Font("GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf", 100)
        self.thank_you_color = (255, 255, 0) # Yellow for emphasis
        self.menu_prompt_font = pg.font.Font("GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf", 60)
        self.menu_prompt_color = (200, 200, 200) # Light grey

        self.level_text_pos_y = level_text_pos_y

    def draw_background(self, screen, current_level):
        """Draws the background image for the current level."""
        # Only draw background if it's a regular level (1, 2, or 3)
        if current_level in self.backgrounds:
            screen.blit(self.backgrounds[current_level], (0, 0))
        else:
            # If current_level is not 1, 2, or 3 draw a plain background or a specific "end game" background.
            screen.fill((0, 0, 0))

    def draw_level_text(self, screen, current_level):
        """Draws the 'Level X' text or 'Thank You' message on the screen."""
        if current_level <= 3: # Display level text for actual levels
            level_text = f"Level {current_level}"
            text_surface = self.level_font.render(level_text, True, self.level_text_color)
            
            # Position the text (horizontally centered, adjustable vertical position)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.level_text_pos_y))
            screen.blit(text_surface, text_rect)
        elif current_level == 4: # Assuming 4 indicates the "Thank You" screen
            self._draw_thank_you_screen(screen)

    def _draw_thank_you_screen(self, screen):
        """Helper method to draw the 'Thank You for Playing' screen."""
        self.end_message = "Thank You For Playing Our Game!"
        self.message_surface = self.thank_you_font.render(self.end_message, True, self.thank_you_color)
        self.message_rect = self.message_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        screen.blit(self.message_surface, self.message_rect)

        self.menu_prompt = "Press SPACE to go back to Main Menu"
        self.menu_prompt_surface = self.menu_prompt_font.render(self.menu_prompt, True, self.menu_prompt_color)
        self.menu_prompt_rect = self.menu_prompt_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        screen.blit(self.menu_prompt_surface, self.menu_prompt_rect)