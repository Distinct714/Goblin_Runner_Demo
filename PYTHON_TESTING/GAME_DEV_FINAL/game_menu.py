import pygame as pg
import sys # Import sys for sys.exit()

class GameMenu:
    def __init__(self, screen, game_instance):
        self.screen = screen
        self.game = game_instance
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Font setup - Ensure this path is absolutely correct!
        self.font_path = "GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf"
        
        self.font = pg.font.Font(self.font_path, 70) 
        self.title_font = pg.font.Font(self.font_path, 220)
        self.demo_font = pg.font.Font(self.font_path, 100)
        self.credit_font = pg.font.Font(self.font_path, 50)
        self.back_button_font = pg.font.Font(self.font_path, 70)
        # NEW: Font for the "Credits" screen title
        self.credits_screen_title_font = pg.font.Font(self.font_path, 70) 

        # Render static text surfaces
        self.game_title_text = self.title_font.render("Goblin Runner", True, (0, 0, 0)) 
        self.below_title_text = self.demo_font.render("Demo", True, (0, 0, 0)) 
        
        self.start_game_text_surface = self.font.render("Start Game", True, (255, 255, 255)) 
        self.credit_game_text_surface = self.font.render("Credits", True, (255, 255, 255))
        self.quit_game_text_surface = self.font.render("Quit", True, (255, 255, 255))
        self.back_text_surface = self.back_button_font.render("Back", True, (255, 255, 255))
        # NEW: Render the Credits screen title text
        self.credits_title_text_surface = self.credits_screen_title_font.render("Credits", True, (255, 255, 255))

        # Define button dimensions
        button_width, button_height = 400, 100
        back_button_width, back_button_height = 250, 80
        # NEW: Credits title box dimensions - we'll calculate its width dynamically later
        credits_title_box_height = self.credits_title_text_surface.get_height() + 40 # Add padding

        # Create and position button rectangles
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

        # NEW: Position the Credits title box and text - width will be calculated in _draw_credits_screen
        # Initialize with a placeholder width, or calculate it in _draw_credits_screen completely.
        # For now, we'll make it dynamic in _draw_credits_screen as it depends on column widths.
        self.credits_title_box_rect = pg.Rect(0, 0, 100, credits_title_box_height) # Placeholder width

        # Get text rects centered on button rects
        self.start_game_text_rect = self.start_game_text_surface.get_rect(center=self.start_button_rect.center)
        self.credit_game_text_rect = self.credit_game_text_surface.get_rect(center=self.credit_button_rect.center)
        self.quit_game_text_rect = self.quit_game_text_surface.get_rect(center=self.quit_button_rect.center)
        self.back_text_rect = self.back_text_surface.get_rect(center=self.back_button_rect.center)
        # NEW: Credits screen title text rect - position will be updated dynamically
        self.credits_title_text_rect = self.credits_title_text_surface.get_rect()
        
        # Define colors
        self.button_color = (104, 37, 37)
        self.hover_color = (150, 50, 50)

        self.menu_active = True

        # Load and scale background image
        self.background_image_scaled = pg.transform.scale(
            pg.image.load("GAME_DEV_FINAL/assets/background/intro.png"), 
            (self.screen_width, self.screen_height)
        )

        # Credits Information - Structured for two columns
        self.creators_data = [
            {"type": "role_names", "role": "Project Lead", "names": "Joshua Bote, Arish Evangelista"},
            {"type": "role_names", "role": "Game Designer", "names": "Joshua Bote"},
            {"type": "role_names", "role": "Game Programmer", "names": "Joshua Bote"},
            {"type": "role_names", "role": "Story Creator", "names": "Arish Evangelista"},
            {"type": "role_names", "role": "Game Artists", "names": "Arish Evangelista, Jennifer Abino, MJ Royol"},
            {"type": "message", "text": "Copyright 2025. All rights reserved."},
        ]

    def handle_events(self, events):
        """Handles events for menu interactions."""
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
                        self.game.game_state = self.game.STATE_MAIN_MENU
                        self.menu_active = True
                        return

    def draw(self): 
        """Draws the main menu items."""
        if not self.menu_active:
            return

        self.screen.blit(self.background_image_scaled, (0, 0))

        self.screen.blit(self.game_title_text, self.game_title_rect)
        self.screen.blit(self.below_title_text, self.below_title_rect) 

        mouse_pos = pg.mouse.get_pos()

        # Determine button colors based on hover
        start_current_color = self.hover_color if self.start_button_rect.collidepoint(mouse_pos) else self.button_color
        credit_current_color = self.hover_color if self.credit_button_rect.collidepoint(mouse_pos) else self.button_color
        quit_current_color = self.hover_color if self.quit_button_rect.collidepoint(mouse_pos) else self.button_color

        # Draw buttons
        pg.draw.rect(self.screen, start_current_color, self.start_button_rect, border_radius=10)
        self.screen.blit(self.start_game_text_surface, self.start_game_text_rect)

        pg.draw.rect(self.screen, credit_current_color, self.credit_button_rect, border_radius=10)
        self.screen.blit(self.credit_game_text_surface, self.credit_game_text_rect)

        pg.draw.rect(self.screen, quit_current_color, self.quit_button_rect, border_radius=10)
        self.screen.blit(self.quit_game_text_surface, self.quit_game_text_rect)

        pg.display.flip()

    def _draw_credits_screen(self):
        """Draws the two-column credits screen, now with a title aligned to the columns."""
        self.screen.blit(self.background_image_scaled, (0, 0))

        # --- Spacing Variables for better control ---
        horizontal_padding_for_content = 20 
        vertical_padding_for_boxes = 30 
        gap_between_columns = 20 
        line_spacing_between_entries = 20 
        line_spacing_within_names = 5 

        # Pre-render text and calculate dimensions for columns
        max_role_width = 0
        max_names_width = 0
        total_column_content_height = 0
        processed_column_lines = []
        footer_messages = []

        for item in self.creators_data:
            if item['type'] == "role_names":
                role_surface = self.credit_font.render(item['role'], True, (255, 255, 255))
                
                # Split names and render each one individually using a loop instead of list comprehension
                individual_names_list = []
                names_split = item['names'].split(',')
                for name in names_split:
                    stripped_name = name.strip()
                    if stripped_name:
                        individual_names_list.append(stripped_name)
                
                names_surfaces = []
                for name_str in individual_names_list:
                    names_surfaces.append(self.credit_font.render(name_str, True, (255, 255, 255)))
                
                if role_surface.get_width() > max_role_width:
                    max_role_width = role_surface.get_width()
                
                if names_surfaces:
                    for s in names_surfaces:
                        if s.get_width() > max_names_width:
                            max_names_width = s.get_width()

                role_block_height = role_surface.get_height()
                names_block_height = 0
                if names_surfaces:
                    current_names_height_sum = 0
                    for s in names_surfaces:
                        current_names_height_sum += s.get_height()
                    names_block_height = current_names_height_sum + \
                                         (len(names_surfaces) - 1) * line_spacing_within_names

                row_total_height = max(role_block_height, names_block_height) + line_spacing_between_entries
                total_column_content_height += row_total_height
                processed_column_lines.append((role_surface, names_surfaces))

            elif item['type'] == "spacer":
                total_column_content_height += line_spacing_between_entries * 2
                processed_column_lines.append(None)

            elif item['type'] == "message":
                footer_messages.append(self.credit_font.render(item['text'], True, (255, 255, 255)))

        if processed_column_lines:
            last_actual_line_found = False
            for i in reversed(range(len(processed_column_lines))):
                if processed_column_lines[i] is not None:
                    total_column_content_height -= line_spacing_between_entries
                    last_actual_line_found = True
                    break
            if not last_actual_line_found and total_column_content_height > 0:
                total_column_content_height = 0

        # Calculate final column box dimensions using padding
        role_col_width = max_role_width + (horizontal_padding_for_content * 2)
        names_col_width = max_names_width + (horizontal_padding_for_content * 2)
        common_col_height = total_column_content_height + (vertical_padding_for_boxes * 2)
        total_columns_width = role_col_width + gap_between_columns + names_col_width

        # Position the entire two-column block, ensuring it's horizontally centered
        start_x_for_columns = (self.screen_width - total_columns_width) / 2
        
        # Calculate the overall bounds of the two columns combined
        combined_columns_left = start_x_for_columns
        combined_columns_right = start_x_for_columns + total_columns_width
        combined_columns_width = combined_columns_right - combined_columns_left

        # Position the Credits title box based on column alignment
        credits_title_text_width = self.credits_title_text_surface.get_width()
        
        title_box_target_width = max(combined_columns_width, credits_title_text_width + 80)

        credits_title_box_x = combined_columns_left

        credits_title_box_y = self.screen_height / 2 - common_col_height / 2 - 150 

        self.credits_title_box_rect.topleft = (credits_title_box_x, credits_title_box_y)
        self.credits_title_box_rect.width = title_box_target_width
        self.credits_title_text_rect.center = self.credits_title_box_rect.center

        # Draw the "Credits" title box and text
        pg.draw.rect(self.screen, self.button_color, self.credits_title_box_rect, border_radius=10)
        self.screen.blit(self.credits_title_text_surface, self.credits_title_text_rect)

        # Start below the "Credits" title box, plus some padding
        start_y_for_columns = self.credits_title_box_rect.bottom + 50 

        # Define the two column Rects
        role_column_rect = pg.Rect(start_x_for_columns, start_y_for_columns, role_col_width, common_col_height)
        names_column_rect = pg.Rect(role_column_rect.right + gap_between_columns, start_y_for_columns, names_col_width, common_col_height)

        # Draw the two column boxes
        pg.draw.rect(self.screen, self.button_color, role_column_rect, border_radius=10)
        pg.draw.rect(self.screen, self.button_color, names_column_rect, border_radius=10)

        # Draw text within each column, now horizontally centered and with multi-line names
        current_y_for_entry_block = role_column_rect.top + vertical_padding_for_boxes

        for item_data in processed_column_lines:
            if item_data is None: # Spacer line
                current_y_for_entry_block += line_spacing_between_entries * 2
            else: # (role_surface, names_surfaces_list) tuple
                role_surface, names_surfaces_list = item_data
                
                # Blit role text (centered within its column's width)
                role_text_rect = role_surface.get_rect(centerx=role_column_rect.centerx, top=current_y_for_entry_block)
                self.screen.blit(role_surface, role_text_rect)

                # Blit names text (centered within its column's width, multiple lines)
                current_y_for_names_in_block = current_y_for_entry_block
                
                for name_surf in names_surfaces_list:
                    name_text_rect = name_surf.get_rect(centerx=names_column_rect.centerx, top=current_y_for_names_in_block)
                    self.screen.blit(name_surf, name_text_rect)
                    current_y_for_names_in_block += name_surf.get_height() + line_spacing_within_names

                # Calculate actual height consumed by this entry for proper advancement
                role_side_consumed_height = role_surface.get_height()
                names_side_consumed_height = 0
                if names_surfaces_list:
                    current_names_height_sum = 0
                    for s in names_surfaces_list:
                        current_names_height_sum += s.get_height()
                    names_side_consumed_height = current_names_height_sum + \
                                                 (len(names_surfaces_list) - 1) * line_spacing_within_names
                
                current_y_for_entry_block += max(role_side_consumed_height, names_side_consumed_height) + line_spacing_between_entries

        # Draw footer messages
        footer_y_offset = max(role_column_rect.bottom, names_column_rect.bottom) + 50
        for msg_surf in footer_messages:
            self.screen.blit(msg_surf, msg_surf.get_rect(centerx=self.screen_width / 2, top=footer_y_offset))
            footer_y_offset += msg_surf.get_height() + 10

        # Draw the Back button
        mouse_pos = pg.mouse.get_pos()
        back_current_color = self.hover_color if self.back_button_rect.collidepoint(mouse_pos) else self.button_color
        pg.draw.rect(self.screen, back_current_color, self.back_button_rect, border_radius=10)
        self.screen.blit(self.back_text_surface, self.back_text_rect)

        pg.display.flip()
