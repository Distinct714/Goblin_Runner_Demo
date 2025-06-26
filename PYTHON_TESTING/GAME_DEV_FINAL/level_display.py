# GAME MENU MANAGEMENT SYSTEM

import pygame as pg
import sys

class GameMenu:
    # Define standard dimensions for buttons.
    BUTTON_DIMS = {'main': (400, 100), 'back': (250, 80)}

    # Define specified colors for the game menu.
    COLORS = {'button': (104, 37, 37), 'hover': (150, 50, 50), 'text': (255, 255, 255), 'title_text': (0, 0, 0)}

    def __init__(self, screen, game_instance):
        # Stores the Pygame screen surface. Keeps a reference to the main game object.
        self.screen = screen
        self.game = game_instance

        # Gets the width and height of the game screen.
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Set the file path for the custom font and set the various variable with specified size. (Change the path file here)
        self.font_path = 'GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf'
        self.font_large = pg.font.Font(self.font_path, 220)
        self.font_medium = pg.font.Font(self.font_path, 100)
        self.font_regular = pg.font.Font(self.font_path, 70)
        self.font_small = pg.font.Font(self.font_path, 50)

        # Pre-render text surfaces.
        self.text_surfaces = {
            'title': self.font_large.render('Goblin Runner', True, self.COLORS['title_text']),
            'demo': self.font_medium.render('Demo', True, self.COLORS['title_text']),
            'start': self.font_regular.render('Start Game', True, self.COLORS['text']),
            'credit_button': self.font_regular.render('Credits', True, self.COLORS['text']),
            'quit': self.font_regular.render('Quit', True, self.COLORS['text']),
            'back': self.font_regular.render('Back', True, self.COLORS['text']),
            'credits_title': self.font_regular.render('Credits', True, self.COLORS['text'])
        }

        # Define rectangles for all buttons.
        self.button_rects = {
            'start': pg.Rect(0, 0, *self.BUTTON_DIMS['main']),
            'credits': pg.Rect(0, 0, *self.BUTTON_DIMS['main']),
            'quit': pg.Rect(0, 0, *self.BUTTON_DIMS['main']),
            'back': pg.Rect(0, 0, *self.BUTTON_DIMS['back'])
        }

        # Position the main menu buttons on the center of the screen.
        self.button_rects['start'].center = (self.screen_width // 2, self.screen_height // 2 + 50)
        self.button_rects['credits'].center = (self.screen_width // 2, self.screen_height // 2 + 180)
        self.button_rects['quit'].center = (self.screen_width // 2, self.screen_height // 2 + 310)
        self.button_rects['back'].center = (self.screen_width // 2, self.screen_height - 150)

        # Set a flag to know if the main menu is active.
        self.menu_active = True

        # Load and scale the background image to fit the screen.
        self.background_image_scaled = pg.transform.scale(
            pg.image.load('GAME_DEV_FINAL/assets/background/intro.png'),
            (self.screen_width, self.screen_height)
        )

        # Add data for the credits screen: roles, names, and copyright.
        self.creators_data = [
            {'type': 'role_names', 'role': 'Project Lead', 'names': 'Joshua Bote, Arish Evangelista'},
            {'type': 'role_names', 'role': 'Game Designer', 'names': 'Joshua Bote'},
            {'type': 'role_names', 'role': 'Game Programmer', 'names': 'Joshua Bote'},
            {'type': 'role_names', 'role': 'Story Creator', 'names': 'Arish Evangelista'},
            {'type': 'role_names', 'role': 'Game Artists', 'names': 'Arish Evangelista, Jennifer Abino, MJ Royol'},
            {'type': 'role_names', 'role': 'Music', 'names': '\"Relaxing Music with Nature Sounds\", From MusicforBodyandSpirit'},
            {'type': 'message', 'text': 'Copyright 2025. All rights reserved.'},
        ]

    def handle_events(self, events):
        # Checks mouse events in game menu. The return statement here will stop processing events.
        if self.menu_active:
            for event in events:
                
                # If the left mouse button was clicked, get the mouse's position.
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    # Check if "Start Game" button was clicked.
                    if self.button_rects["start"].collidepoint(mouse_pos):
                        self.menu_active = False
                        self.game.start_game()
                        return
                    
                    # Check if "Credits" button was clicked.
                    elif self.button_rects["credits"].collidepoint(mouse_pos): 
                        self.menu_active = False
                        self.game.game_state = self.game.STATE_CREDITS
                        return
                    
                    # Check if "Quit" button was clicked.
                    elif self.button_rects["quit"].collidepoint(mouse_pos): 
                        pg.quit()
                        sys.exit()

        # While in credits screen, check the mouse events.
        elif self.game.game_state == self.game.STATE_CREDITS:
            for event in events:
                # If the left mouse button was clicked, check if "Back" button was clicked and change game state back to main menu.
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rects["back"].collidepoint(event.pos): 
                        self.game.game_state = self.game.STATE_MAIN_MENU 
                        self.menu_active = True
                        return
    def draw(self):
        # Draws the main menu elements on the screen.
        if not self.menu_active:
            return
        
        # Draw the background image.
        self.screen.blit(self.background_image_scaled, (0, 0))

        # Draw the game title and demo subtitle.
        self.screen.blit(self.text_surfaces["title"], 
                         self.text_surfaces["title"].get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 200)))
        self.screen.blit(self.text_surfaces["demo"], 
                         self.text_surfaces["demo"].get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 130)))

        # Get the current mouse position.
        mouse_pos = pg.mouse.get_pos()

        # Change button colors based on whether the mouse is hovering over them.
        start_color = self.COLORS["hover"] if self.button_rects["start"].collidepoint(mouse_pos) else self.COLORS["button"]
        credits_color = self.COLORS["hover"] if self.button_rects["credits"].collidepoint(mouse_pos) else self.COLORS["button"]
        quit_color = self.COLORS["hover"] if self.button_rects["quit"].collidepoint(mouse_pos) else self.COLORS["button"]
        
        # Draw the Start Game button and its rectangle. Draw the text on the button.
        pg.draw.rect(self.screen, start_color, self.button_rects["start"], border_radius=10) # Draws the button rectangle.
        self.screen.blit(self.text_surfaces["start"], self.text_surfaces["start"].get_rect(center=self.button_rects["start"].center))

        # Draw the Credits button and its rectangle. Draw the text on the button.
        pg.draw.rect(self.screen, credits_color, self.button_rects["credits"], border_radius=10)
        self.screen.blit(self.text_surfaces["credit_button"], 
                         self.text_surfaces["credit_button"].get_rect(center=self.button_rects["credits"].center))

        # Draw the Quit button and its rectangle. Draw the text on the button.
        pg.draw.rect(self.screen, quit_color, self.button_rects["quit"], border_radius=10)
        self.screen.blit(self.text_surfaces["quit"], self.text_surfaces["quit"].get_rect(center=self.button_rects["quit"].center)) 

        pg.display.flip()

    def draw_credits_screen(self):
        # Draws all the elements for the credits screen.
        self.screen.blit(self.background_image_scaled, (0, 0)) # Draw the background image.

        # Constants for layout and spacing on the credits screen.
        HORIZONTAL_PAD, VERTICAL_PAD, COLUMN_GAP = 20, 30, 20
        LINE_SPACING_ENTRY, LINE_SPACING_NAME = 5, 5 

        # Set variables to track content dimensions.
        max_role_width, max_names_width, total_content_height = 0, 0, 0 

        # Set an empty lists to hold rendered credit lines and footer messages.
        processed_lines, footer_messages = [], [] 

        # Process each item in the creators_data to render text and specify sizes.
        for item in self.creators_data:

            # If it's a role with names, render the role text and each name. Then, split names by comma.
            if item['type'] == "role_names":
                role_surf = self.font_small.render(item['role'], True, self.COLORS["text"]) 
                names_surfs = [self.font_small.render(name.strip(), True, self.COLORS["text"])
                               for name in item['names'].split(',') if name.strip()] 

                # Update max role width.
                max_role_width = max(max_role_width, role_surf.get_width())

                # If there are names, update max names width.
                if names_surfs:
                    max_names_width = max(max_names_width, max(s.get_width() for s in names_surfs)) 

                # Get height of the role text.
                role_height = role_surf.get_height()

                # Calculate total height for names.
                names_height = sum(s.get_height() for s in names_surfs) + max(0, (len(names_surfs) - 1)) * LINE_SPACING_NAME 
                
                # Add to total height.
                total_content_height += max(role_height, names_height) + LINE_SPACING_ENTRY 

                # Store rendered surfaces.
                processed_lines.append((role_surf, names_surfs))

            # If it's a copyright text, render and store the message.
            elif item['type'] == "message": 
                footer_messages.append(self.font_small.render(item['text'], True, self.COLORS["text"])) 

        # Customize dimensions for the credit columns.
        role_col_width = max_role_width + (HORIZONTAL_PAD * 2) 
        names_col_width = max_names_width + (HORIZONTAL_PAD * 2)
        common_col_height = total_content_height + (VERTICAL_PAD * 2)
        total_columns_width = role_col_width + COLUMN_GAP + names_col_width

        # X-coordinate to center the columns.
        start_x_columns = (self.screen_width - total_columns_width) // 2 
        
        # Customize position and size for the "Credits" title box.
        title_box_width = max(total_columns_width, self.text_surfaces["credits_title"].get_width() + 80)
        # Create title box rectangle.
        credits_title_box_rect = pg.Rect(start_x_columns, self.screen_height // 2 - common_col_height // 2 - 150, 
                                         title_box_width, self.text_surfaces["credits_title"].get_height() + 40) 
        credits_title_text_rect = self.text_surfaces["credits_title"].get_rect(center=credits_title_box_rect.center)

        # Draw the title box.
        pg.draw.rect(self.screen, self.COLORS["button"], credits_title_box_rect, border_radius=10) 

        # Draw the title text.
        self.screen.blit(self.text_surfaces["credits_title"], credits_title_text_rect)

        # Calculate starting Y-position for the credit columns.
        start_y_columns = credits_title_box_rect.bottom + 50

        # Create rectangles for the background of the role and name columns.
        role_column_rect = pg.Rect(start_x_columns, start_y_columns, role_col_width, common_col_height) 
        names_column_rect = pg.Rect(role_column_rect.right + COLUMN_GAP, start_y_columns, names_col_width, common_col_height)

        # Draw role and names column background.
        pg.draw.rect(self.screen, self.COLORS["button"], role_column_rect, border_radius=10)
        pg.draw.rect(self.screen, self.COLORS["button"], names_column_rect, border_radius=10)

        # Starting Y for the first credit entry.
        current_y_entry = role_column_rect.top + VERTICAL_PAD

        # Draw each credit entry (role and names). Position the role text and draw it.
        for role_surf, names_surfs in processed_lines:
            role_text_rect = role_surf.get_rect(centerx=role_column_rect.centerx, top=current_y_entry) 
            self.screen.blit(role_surf, role_text_rect)

            # Start Y for names in this entry
            current_y_name = current_y_entry

            for name_surf in names_surfs:
                # Position name text and draw it.
                name_text_rect = name_surf.get_rect(centerx=names_column_rect.centerx, top=current_y_name) 
                self.screen.blit(name_surf, name_text_rect)

                # Move Y down for next name.
                current_y_name += name_surf.get_height() + LINE_SPACING_NAME
            
            # Calculate total height of this entry.
            entry_height = max(role_surf.get_height(), sum(s.get_height() for s in names_surfs) + max(0, (len(names_surfs) - 1)) * LINE_SPACING_NAME)
            
            # Move Y down for the next credit entry.
            current_y_entry += entry_height + LINE_SPACING_ENTRY

        # Draw footer messages (like copyright).
        footer_y = max(role_column_rect.bottom, names_column_rect.bottom) + 150

        # Loop through each footer message and draw the message.
        for msg_surf in footer_messages: 
            self.screen.blit(msg_surf, msg_surf.get_rect(centerx=self.screen_width // 2, top=footer_y))

        # Draw the "Back" button.
        mouse_pos = pg.mouse.get_pos()

        # Determine button color.
        back_color = self.COLORS["hover"] if self.button_rects["back"].collidepoint(mouse_pos) else self.COLORS["button"]

        # Draw the back button rectangle.
        pg.draw.rect(self.screen, back_color, self.button_rects["back"], border_radius=10)

        # Draw the "Back" text.
        self.screen.blit(self.text_surfaces["back"], self.text_surfaces["back"].get_rect(center=self.button_rects["back"].center))

        pg.display.flip()
