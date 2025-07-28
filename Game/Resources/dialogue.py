# DIALOGUE MANAGEMENT SYSTEM

import pygame as pg

class Dialogue:

    def __init__(self, screen_width, screen_height):
        # Store the width and height of the game screen.
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Set the font size for the text.
        self.font_size = 50

        # Set the color for the text.
        self.text_color = (255, 255, 255)
        
        # Set the color for the dialogue box background (semi-transparent black).
        self.box_color = (0, 0, 0, 200)
        
        # Calculate the width of the dialogue box.
        self.dialogue_box_width = int(screen_width * 0.8) 
        # Calculate the height of the dialogue box.
        self.dialogue_box_height = int(screen_height * 0.3)
        
        # Create a rectangle that defines the position and size of the dialogue box.
        # It's centered horizontally and vertically on the screen.
        self.dialogue_box_rect = pg.Rect(
            (self.screen_width - self.dialogue_box_width) // 2, 
            (self.screen_height - self.dialogue_box_height) // 2,
            self.dialogue_box_width,
            self.dialogue_box_height
        )

        # Set the file path for the custom font and load the font with the specified size.
        self.font_path = "GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf"
        self.font = pg.font.Font(self.font_path, self.font_size)
        
        # A flag to check if dialogue is currently active and should be shown.
        self.dialogue_active = False

        # A list to hold all the lines of dialogue for the current sequence.
        self.current_dialogue_lines = []

        # An index to keep track of which line is currently being displayed.
        self.current_dialogue_line_index = 0

        # Stores the key of the last dialogue sequence that finished.
        self.last_dialogue_level_completed = None

        # A cooldown period to prevent rapid dialogue advancement. (In game frames)
        self.COOLDOWN_FRAMES = 60

        # Create a dictionary to store all the dialogue lines for different parts of the game (levels/keys).
        # Each keys connect to a list of strings, where each string is a dialogue line. (values)
        self.level_dialogues = {
            1: [
                "Shinji: uhhhh my head hurts, huh where am I?",
                "Shinji: Is this a cave!? Why am I in a cave!?",
                "Shinji: Wait I see light maybe it\'s the exit?", 
                "Shinji: It\'s so bright outside.",
                "Shinji: Huh? am I in a forest?",
                "Shinji: Wait, why am I in the middle of the forest",
                "- A familiar voice you hear - ",
                "Shinji: Wait that voice,",
                "Shinji: she really did send me to another world.",
                "Shinji: But, why? Why me? And why am I a goblin!?",
                "Shinji: No, I won\'t give up, ",
                "Shinji: I\'ll defeat this demon king and once I do,",
                "Shinji: I\'ll tell her how I really feel."
            ],
            2: [
                "- Shinji saw three goblins -",
                "Shinji: That\'s another goblins.",
                "Shinji: I think were friends, right? ",
                "Shinji: I mean were both goblins, right?"
            ],
            3: [
                "- Shinji see ogres -",
                "Shinji: Is that? An ogres!?",
                "Shinji: They're big, could I even defeat them?",
                "Shinji: Wait a sec.",
                "Shinji: That forest looks mysterious...",
                "Shinji: Maybe I could past my way there."
            ]
        }

        # Defines the index of the dialogue line in level 1 after which a dark screen overlay should disappear.
        self.REMOVE_OVERLAY_INDEX_LVL1 = 3 

    def set_level_dialogue(self, level_key):
        # Sets the dialogue lines to be displayed based on a given level key.

        # Get the list of dialogue lines for the given key, or an empty list if key not found.
        self.current_dialogue_lines = self.level_dialogues.get(level_key, [])

        # Reset the current line index to the beginning of the new dialogue.
        self.current_dialogue_line_index = 0

        # Store the key of the dialogue currently being set.
        self._current_dialogue_key = level_key

    def start_dialogue(self):
        # Activates the dialogue system, making the dialogue box visible.
        self.dialogue_active = True

    def advance_dialogue(self):
        # Moves to the next line of dialogue.
        # Returns True if there are more lines to show, False if the dialogue has ended.

        # Increment the index to show the next line.
        self.current_dialogue_line_index += 1

        # Check if there are still more lines left in the current dialogue sequence.
        if self.current_dialogue_line_index < len(self.current_dialogue_lines):
            return True
        else:
            self.dialogue_active = False

            # Reset the line index for future dialogues.
            self.current_dialogue_line_index = 0

            # Record which dialogue sequence just finished.
            self.last_dialogue_level_completed = self._current_dialogue_key

            # Return False, indicating dialogue is over.
            return False

    def is_dialogue_active(self):
        # Checks if the dialogue box is currently on the screen.
        return self.dialogue_active

    def _draw_dark_overlay(self, screen):
        # Draws a semi-transparent dark layer over the entire game screen.
        # This is used to darken the background when dialogue is showing.

        # Create a new transparent surface the size of the screen.
        overlay = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        
        # Fill the overlay with a dark color and some transparency (alpha 230).
        overlay.fill((0, 0, 0, 230))
        
        # Draw the overlay onto the main game screen.
        screen.blit(overlay, (0, 0))

    def draw_dialogue(self, screen):
        # Draws the dialogue box and the current line of text on the screen.
  
        # If dialogue is not active, do nothing and return.
        if not self.dialogue_active:
            return

        # Check if it's level 1 dialogue and check if the current line index is before the specific point
        # where the overlay should disappear.
        if self._current_dialogue_key == 1 and self.current_dialogue_line_index < self.REMOVE_OVERLAY_INDEX_LVL1:
            self._draw_dark_overlay(screen)

        # Create a semi-transparent surface for the dialogue box itself. (s for surface)
        s = pg.Surface((self.dialogue_box_rect.width, self.dialogue_box_rect.height), pg.SRCALPHA)

        # Fill this surface with the dialogue box color.
        s.fill(self.box_color)

        # Draw the dialogue box background onto the main screen.
        screen.blit(s, self.dialogue_box_rect)

        # This will only proceed to render text if there are actual dialogue lines loaded.
        if self.current_dialogue_lines:
            # Get the current line of dialogue to display.
            current_line = self.current_dialogue_lines[self.current_dialogue_line_index]

            # Render the text surface from the current line using the chosen font and color.
            text_surface = self.font.render(current_line, True, self.text_color)
            
            # Get the rectangle for the rendered text and center it within the dialogue box.
            text_rect = text_surface.get_rect(center=(self.dialogue_box_rect.centerx, self.dialogue_box_rect.centery))

            # Draw the text surface onto the main screen at its centered position.
            screen.blit(text_surface, text_rect)
