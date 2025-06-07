import pygame as pg
import sys

class GameMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings # This 'settings' is expected to be the Goblin_Runner instance

        # Importing Font in asset files and adjusting font size
        self.font = pg.font.Font("GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf", 80) 
        self.title_font = pg.font.Font("GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf", 220)
        self.below_title = pg.font.Font("GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf", 100)

        # Define menu items and create a surface object from the text
        self.game_title_text = self.title_font.render("Goblin Runner", True, (0, 0, 0)) 
        self.below_title_text = self.below_title.render("Demo", True, (0, 0, 0))
        self.start_game_text = self.font.render("Start Game", True, (255, 255, 255)) 
        self.quit_game_text = self.font.render("Quit", True, (255, 255, 255))

        # Getting rectangles for positioning 
        self.game_title_rect = self.game_title_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2 - 200))
        self.below_title_rect = self.below_title_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2 - 130))

        # Create base rectangles for start and quit text 
        self.start_game_text_rect = self.start_game_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2 + 50))
        self.quit_game_text_rect = self.quit_game_text.get_rect(center=(self.settings.screen_width / 2, self.settings.screen_height / 2 + 180))

        # Create slightly larger rectangles for the buttons (padding) (Like Box Button Size)
        self.start_button_rect = self.start_game_text_rect.inflate(20, 20) 
        self.quit_button_rect = self.quit_game_text_rect.inflate(160, 20) 

        # Store the collision rectangles for mouse clicks, which is the button rectangles
        self.start_game_clickable_rect = self.start_button_rect
        self.quit_game_clickable_rect = self.quit_button_rect

        # Define button colors
        self.button_color = (104, 37, 37)

        # Setting menu as active
        self.menu_active = True

        # Load and scale background image ONCE during initialization
        original_background = pg.image.load("GAME_DEV_FINAL/assets/background/intro.png")
        self.background_image_scaled = pg.transform.scale(original_background, (self.settings.screen_width, self.settings.screen_height))

    # Handles events passed from the main loop
    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            
            # Check for mouse events
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                # When mouse click the start and quit button, this will execute
                if self.start_game_clickable_rect.collidepoint(mouse_pos):
                    self.menu_active = False
                elif self.quit_game_clickable_rect.collidepoint(mouse_pos):
                    sys.exit()
                    
    # Draw the menu items on the screen.
    def draw(self): 
        self.screen.blit(self.background_image_scaled, (0, 0))

        self.screen.blit(self.game_title_text, self.game_title_rect)
        self.screen.blit(self.below_title_text, self.below_title_rect) 

        pg.draw.rect(self.screen, self.button_color, self.start_button_rect)
        self.screen.blit(self.start_game_text, self.start_game_text_rect)

        pg.draw.rect(self.screen, self.button_color, self.quit_button_rect)
        self.screen.blit(self.quit_game_text, self.quit_game_text_rect)

        pg.display.flip()