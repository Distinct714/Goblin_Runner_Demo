import pygame as pg

class Dialogue:
    """
    Manages and displays dialogue lines with a single, fixed appearance.
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # --- Fixed Settings for all Dialogue Boxes ---
        self.font_size = 50
        self.text_color = (255, 255, 255)    # White text
        self.box_color = (0, 0, 0, 200)     # Semi-transparent black for the dialogue box
        
        # Fixed dialogue box dimensions (80% width, 30% height of screen)
        self.dialogue_box_width = int(screen_width * 0.8)  
        self.dialogue_box_height = int(screen_height * 0.3) 
        
        # Dialogue box is always centered
        self.dialogue_box_rect = pg.Rect(
            (self.screen_width - self.dialogue_box_width) // 2,  
            (self.screen_height - self.dialogue_box_height) // 2, 
            self.dialogue_box_width,
            self.dialogue_box_height
        )

        # Font setup
        self.font_path = "GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf"
        self.font = pg.font.Font(self.font_path, self.font_size)
        
        self.dialogue_active = False # True when dialogue box is on screen
        self.current_dialogue_lines = [] # List of lines for the current dialogue sequence
        self.current_dialogue_line_index = 0 # Index of the line currently displayed
        self.last_dialogue_level_completed = None # Tracks which dialogue sequence just ended
        self.COOLDOWN_FRAMES = 60 # Cooldown for transitions (e.g., 1 second at 60 FPS)

        # Dialogue content for each level/key (now just lists of strings)
        self.level_dialogues = {
            1: [
                "Shinji: uhhhh my head hurts, huh where am I?",
                "Shinji: Is this a cave!? Why am I in a cave!?",
                "Shinji: Wait I see light maybe it\'s the exit?", 
                "Shinji: It\'s so bright outside.", # This is the line where the overlay will disappear
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
            ],
            4: [ # This is likely your 'Game Completion' dialogue\
                "Shinji is now dead.",
            ]
        }
        # Define the index at which the dark overlay should be removed for level 1
        # "Shinji: It's so bright outside." is at index 3 in the level 1 dialogue list (0-indexed)
        self.REMOVE_OVERLAY_INDEX_LVL1 = 3 

    def set_level_dialogue(self, level_key):
        """
        Loads the dialogue lines for a specific level or key.
        If the level_key is not found, it sets an empty dialogue.
        """
        # Get dialogue lines; if the key isn't found, an empty list is used
        self.current_dialogue_lines = self.level_dialogues.get(level_key, [])
        self.current_dialogue_line_index = 0
        self._current_dialogue_key = level_key # Keep track of the current dialogue's key

    def start_dialogue(self):
        """Activates the dialogue display."""
        self.dialogue_active = True

    def advance_dialogue(self):
        """
        Advances to the next dialogue line. Returns True if more lines, False if dialogue ends.
        """
        self.current_dialogue_line_index += 1
        if self.current_dialogue_line_index < len(self.current_dialogue_lines):
            return True # More lines to show
        else:
            self.dialogue_active = False # Deactivate dialogue when all lines are shown
            self.current_dialogue_line_index = 0 # Reset index for next time
            self.last_dialogue_level_completed = self._current_dialogue_key # Mark which dialogue just ended
            return False

    def is_dialogue_active(self):
        """Returns True if the dialogue box is currently active."""
        return self.dialogue_active

    def _draw_dark_overlay(self, screen):
        """Draws a semi-transparent dark overlay over the entire screen."""
        overlay = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 230)) # Black with 180 alpha (semi-transparent)
        screen.blit(overlay, (0, 0))

    def draw_dialogue(self, screen):
        """Draws the current dialogue box and text on the screen."""
        if not self.dialogue_active:
            return

        # NEW: Apply dark overlay if it's level 1 dialogue and before the specific line
        if self._current_dialogue_key == 1 and self.current_dialogue_line_index < self.REMOVE_OVERLAY_INDEX_LVL1:
            self._draw_dark_overlay(screen)

        # Draw the semi-transparent background box for dialogue text
        s = pg.Surface((self.dialogue_box_rect.width, self.dialogue_box_rect.height), pg.SRCALPHA)
        s.fill(self.box_color)
        screen.blit(s, self.dialogue_box_rect)

        # Render and position the current dialogue line
        if self.current_dialogue_lines: # Only draw if there are actual lines
            current_line = self.current_dialogue_lines[self.current_dialogue_line_index]
            text_surface = self.font.render(current_line, True, self.text_color)
            
            # Center the text within the dialogue box
            text_rect = text_surface.get_rect(center=(self.dialogue_box_rect.centerx, self.dialogue_box_rect.centery))
            screen.blit(text_surface, text_rect)
