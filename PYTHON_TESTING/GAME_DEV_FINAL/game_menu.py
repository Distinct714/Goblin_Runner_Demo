# GAME MENU MANAGEMENT SYSTEM

import pygame as pg
import sys

class GameMenu:
    
    def __init__(self, screen, game_instance):
        self.screen = screen
        self.game = game_instance
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Set the font file for all text.
        self.font_path = "GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf"
        
        # Set up different font sizes for various texts.
        self.font = pg.font.Font(self.font_path, 70) 
        self.title_font = pg.font.Font(self.font_path, 220)
        self.demo_font = pg.font.Font(self.font_path, 100)
        self.credit_font = pg.font.Font(self.font_path, 50)
        self.back_button_font = pg.font.Font(self.font_path, 70)
        self.credits_screen_title_font = pg.font.Font(self.font_path, 70) 

        # Create the text images for the main menu.
        self.game_title_text = self.title_font.render("Goblin Runner", True, (0, 0, 0)) 
        self.below_title_text = self.demo_font.render("Demo", True, (0, 0, 0)) 
        
        self.start_game_text_surface = self.font.render("Start Game", True, (255, 255, 255)) 
        self.credit_game_text_surface = self.font.render("Credits", True, (255, 255, 255))
        self.quit_game_text_surface = self.font.render("Quit", True, (255, 255, 255))
        self.back_text_surface = self.back_button_font.render("Back", True, (255, 255, 255))
        self.credits_title_text_surface = self.credits_screen_title_font.render("Credits", True, (255, 255, 255))

        # Set standard button sizes.
        button_width, button_height = 400, 100
        back_button_width, back_button_height = 250, 80

        # Create rectangles for the main menu titles and buttons.
        self.game_title_rect = self.game_title_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 200))
        self.below_title_rect = self.below_title_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 130))
        
        self.start_button_rect = pg.Rect(0, 0, button_width, button_height)
        self.start_button_rect.center = (self.screen_width / 2, self.screen_height / 2 + 50)

        self.credit_button_rect = pg.Rect(0, 0, button_width, button_height)
        self.credit_button_rect.center = (self.screen_width / 2, self.screen_height / 2 + 180)

        self.quit_button_rect = pg.Rect(0, 0, button_width, button_height)
        self.quit_button_rect.center = (self.screen_width / 2, self.screen_height / 2 + 310)

        self.back_button_rect = pg.Rect(0, 0, back_button_width, back_button_height)
        self.back_button_rect.center = (self.screen_width / 2, self.screen_height - 100)

        # Set up a placeholder for the credits title box.
        self.credits_title_box_rect = pg.Rect(0, 0, 100, self.credits_title_text_surface.get_height() + 40) 

        # Center the text images within their button rectangles.
        self.start_game_text_rect = self.start_game_text_surface.get_rect(center=self.start_button_rect.center)
        self.credit_game_text_rect = self.credit_game_text_surface.get_rect(center=self.credit_button_rect.center)
        self.quit_game_text_rect = self.quit_game_text_surface.get_rect(center=self.quit_button_rect.center)
        self.back_text_rect = self.back_text_surface.get_rect(center=self.back_button_rect.center)
        self.credits_title_text_rect = self.credits_title_text_surface.get_rect() # Position will be set later.
        
        # Define colors for buttons and when hovered over.
        self.button_color = (104, 37, 37)
        self.hover_color = (150, 50, 50)

        # Set True if the main menu is currently showing.
        self.menu_active = True

        # Load and resize the background image for the menu.
        self.background_image_scaled = pg.transform.scale(
            pg.image.load("GAME_DEV_FINAL/assets/background/intro.png"), 
            (self.screen_width, self.screen_height)
        )

        # Add information for the credits screen, roles and names.
        self.creators_data = [
            {"type": "role_names", "role": "Project Lead", "names": "Joshua Bote, Arish Evangelista"},
            {"type": "role_names", "role": "Game Designer", "names": "Joshua Bote"},
            {"type": "role_names", "role": "Game Programmer", "names": "Joshua Bote"},
            {"type": "role_names", "role": "Story Creator", "names": "Arish Evangelista"},
            {"type": "role_names", "role": "Game Artists", "names": "Arish Evangelista, Jennifer Abino, MJ Royol"},
            {"type": "message", "text": "Copyright 2025. All rights reserved."},
        ]

    def handle_events(self, events):
        # Checks for mouse clicks on menu buttons. The return in this method means stop checking events.
        if self.menu_active:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    
                    if self.start_button_rect.collidepoint(mouse_pos):
                        self.menu_active = False
                        self.game.start_game()
                        return
                    
                    elif self.credit_button_rect.collidepoint(mouse_pos):
                        self.menu_active = False
                        self.game.game_state = self.game.STATE_CREDITS
                        return
                    elif self.quit_button_rect.collidepoint(mouse_pos):
                        pg.quit()
                        sys.exit()

        elif self.game.game_state == self.game.STATE_CREDITS:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button_rect.collidepoint(event.pos):

                         # Go back to main menu.
                        self.game.game_state = self.game.STATE_MAIN_MENU

                         # Show main menu.
                        self.menu_active = True
                        return

    def draw(self): 
        # Draws the main menu on the screen. 

        # Don't draw if menu is not active.
        if not self.menu_active:
            return
        
         # Draw background image in the game menu.
        self.screen.blit(self.background_image_scaled, (0, 0))

         # Draw game title and "Demo" text.
        self.screen.blit(self.game_title_text, self.game_title_rect)
        self.screen.blit(self.below_title_text, self.below_title_rect)
        
         # Get mouse position.
        mouse_pos = pg.mouse.get_pos()

        # Change button color if mouse is hovering over it. (Using ternary statement)
        start_current_color = self.hover_color if self.start_button_rect.collidepoint(mouse_pos) else self.button_color
        credit_current_color = self.hover_color if self.credit_button_rect.collidepoint(mouse_pos) else self.button_color
        quit_current_color = self.hover_color if self.quit_button_rect.collidepoint(mouse_pos) else self.button_color

        # Draw each button rectangle and its text.
        pg.draw.rect(self.screen, start_current_color, self.start_button_rect, border_radius=10)
        self.screen.blit(self.start_game_text_surface, self.start_game_text_rect)

        pg.draw.rect(self.screen, credit_current_color, self.credit_button_rect, border_radius=10)
        self.screen.blit(self.credit_game_text_surface, self.credit_game_text_rect)

        pg.draw.rect(self.screen, quit_current_color, self.quit_button_rect, border_radius=10)
        self.screen.blit(self.quit_game_text_surface, self.quit_game_text_rect)

        pg.display.flip()

    def _draw_credits_screen(self):
        # Draws the two-column credits screen with a title.

         # Draw background image in the credit screen.
        self.screen.blit(self.background_image_scaled, (0, 0))

        # Settings for spacing the credit text.
        horizontal_padding = 20 
        vertical_padding = 30 
        column_gap = 20 
        line_spacing_entry = 20 
        line_spacing_name = 5 

        max_role_width = 0 # Widest role text.
        max_names_width = 0 # Widest name text.
        total_content_height = 0 # Total height for all credit entries.
        processed_lines = [] # Store rendered text for drawing.
        footer_messages = [] # Messages at the bottom of the credits.

        # Loop through each credit item to prepare text and measure sizes.
        for item in self.creators_data:
            if item['type'] == "role_names":
                role_surface = self.credit_font.render(item['role'], True, (255, 255, 255))
                
                # Split names into individual lines and render them.
                names_surfaces = [self.credit_font.render(name.strip(), True, (255, 255, 255)) 
                                  for name in item['names'].split(',') if name.strip()]
                
                max_role_width = max(max_role_width, role_surface.get_width())
                if names_surfaces:
                    max_names_width = max(max_names_width, max(s.get_width() for s in names_surfaces))

                # Calculate height needed for this entry.
                role_block_height = role_surface.get_height()
                names_block_height = sum(s.get_height() for s in names_surfaces) + \
                                     max(0, (len(names_surfaces) - 1)) * line_spacing_name
                
                row_total_height = max(role_block_height, names_block_height) + line_spacing_entry
                total_content_height += row_total_height
                processed_lines.append((role_surface, names_surfaces))

            elif item['type'] == "message":
                footer_messages.append(self.credit_font.render(item['text'], True, (255, 255, 255)))

        # Remove extra spacing at the very end of the content height.
        if processed_lines:
            total_content_height -= line_spacing_entry

        # Calculate final sizes for the two credit columns.
        role_col_width = max_role_width + (horizontal_padding * 2)
        names_col_width = max_names_width + (horizontal_padding * 2)
        common_col_height = total_content_height + (vertical_padding * 2)
        total_columns_width = role_col_width + column_gap + names_col_width

        # Position the entire credit section in the middle of the screen.
        start_x_columns = (self.screen_width - total_columns_width) / 2
        
        # Calculate the credit title box's position and size.
        title_box_width = max(total_columns_width, self.credits_title_text_surface.get_width() + 80)
        title_box_x = start_x_columns
        title_box_y = self.screen_height / 2 - common_col_height / 2 - 150 

        self.credits_title_box_rect.topleft = (title_box_x, title_box_y)
        self.credits_title_box_rect.width = title_box_width
        self.credits_title_text_rect.center = self.credits_title_box_rect.center

        # Draw the "Credits" title box and text.
        pg.draw.rect(self.screen, self.button_color, self.credits_title_box_rect, border_radius=10)
        self.screen.blit(self.credits_title_text_surface, self.credits_title_text_rect)

        # Start drawing credit entries below the title.
        start_y_columns = self.credits_title_box_rect.bottom + 50 

        # Create rectangles for the two columns where credits will be drawn.
        role_column_rect = pg.Rect(start_x_columns, start_y_columns, role_col_width, common_col_height)
        names_column_rect = pg.Rect(role_column_rect.right + column_gap, start_y_columns, names_col_width, common_col_height)

        # Draw the background boxes for the two columns.
        pg.draw.rect(self.screen, self.button_color, role_column_rect, border_radius=10)
        pg.draw.rect(self.screen, self.button_color, names_column_rect, border_radius=10)

        current_y_for_entry = role_column_rect.top + vertical_padding # Starting Y for content.

        # Draw each role and name in the columns.
        for role_surface, names_surfaces in processed_lines:
            # Draw role text.
            role_text_rect = role_surface.get_rect(centerx=role_column_rect.centerx, top=current_y_for_entry)
            self.screen.blit(role_surface, role_text_rect)

            # Draw each name, one below the other.
            current_y_for_name = current_y_for_entry
            for name_surf in names_surfaces:
                name_text_rect = name_surf.get_rect(centerx=names_column_rect.centerx, top=current_y_for_name)
                self.screen.blit(name_surf, name_text_rect)
                current_y_for_name += name_surf.get_height() + line_spacing_name

            # Move Y down for the next entry.
            role_height = role_surface.get_height()
            names_height = sum(s.get_height() for s in names_surfaces) + \
                           max(0, (len(names_surfaces) - 1)) * line_spacing_name
            
            current_y_for_entry += max(role_height, names_height) + line_spacing_entry

        # Draw messages at the very bottom of the screen.
        footer_y = max(role_column_rect.bottom, names_column_rect.bottom) + 50
        for msg_surf in footer_messages:
            self.screen.blit(msg_surf, msg_surf.get_rect(centerx=self.screen_width / 2, top=footer_y))
            footer_y += msg_surf.get_height() + 10

        # Draw the "Back" button.
        mouse_pos = pg.mouse.get_pos()
        back_current_color = self.hover_color if self.back_button_rect.collidepoint(mouse_pos) else self.button_color
        pg.draw.rect(self.screen, back_current_color, self.back_button_rect, border_radius=10)
        self.screen.blit(self.back_text_surface, self.back_text_rect)

        pg.display.flip()
