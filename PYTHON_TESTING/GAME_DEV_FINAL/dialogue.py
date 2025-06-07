import pygame as pg

class Dialogue:
    """
    Manages and displays dialogue lines for different levels.
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.font = pg.font.Font("GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf", 40)  # Font for dialogue text
        self.text_color = (255, 255, 255)   # White text
        self.box_color = (0, 0, 0, 180)     # Semi-transparent black for the dialogue box

        self.dialogue_box_height = 150
        self.dialogue_box_rect = pg.Rect(
            0, self.screen_height - self.dialogue_box_height, 
            self.screen_width, self.dialogue_box_height
        )

        self.dialogue_active = False # True when dialogue box is on screen
        self.current_dialogue_lines = [] # List of lines for the current dialogue sequence
        self.current_dialogue_line_index = 0 # Index of the line currently displayed

        # Dialogue for each level (level number -> list of strings)
        self.level_dialogues = {
            1: [
                "- Enter space to continue -",
                "Shinji: uhhhh my head hurts, huh where am I?",
                "Shinji: Is this a cave!? Why am I in a cave!?",
                "Shinji: Wait I see light maybe it\'s the exit?", 
                "Shinji: It\'s so bright outside, huh am I in a forest?",
                "Shinji: Wait, why am I in the middle of the forest",
                "Shinji: Wait that voice,",
                "Shinji: she really did send me to another world.",
                "Shinji: But, why? Why me? And why am I a goblin!?",
                "Shinji's thoughts: No, I won\'t give up, I\'ll defeat this demon king and once I do,",
                "Shinji's thoughts: I\'ll tell her how I really feel."
            ],

            2: [
                "- Shinji saw another goblin -",
                "Shinji: That\'s another goblin.",
                "Shinji: I think were friends, right? ",
                "Shinji: I mean were both goblins, right?"
            ],

            3: [
                "- Shinji see ogres -",
                "Shinji: Is that? An ogres!?",
                "Shinji: He's big, could I even defeat him?",
                "Shinji: Wait a sec.",
                "Shinji: That forest looks mysterious...",
                "Shinji: Maybe I could past my way there."
            ],

            # Dialogue for the 'Game Over' screen (collision) and 'Game Completion'
            99: [
                "You've been defeated!",
                "Game Over!",
                "Press SPACE to return to the main menu."
            ],
            4: [
                "Press SPACE to return to the main menu."
            ]
        }

    def set_level_dialogue(self, level):
        """
        Loads the dialogue lines for a specific level.
        """
        self.current_dialogue_lines = self.level_dialogues.get(level, ["No dialogue for this level."])
        self.current_dialogue_line_index = 0

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
            self.dialogue_active = False # No more lines, deactivate dialogue
            self.current_dialogue_line_index = 0 # Reset for next time
            return False # Dialogue finished

    def is_dialogue_active(self):
        """Returns True if the dialogue box is currently active."""
        return self.dialogue_active

    def draw_dialogue(self, screen):
        """Draws the current dialogue box and text on the screen."""
        if not self.dialogue_active:
            return

        # Draw semi-transparent background box
        s = pg.Surface((self.dialogue_box_rect.width, self.dialogue_box_rect.height), pg.SRCALPHA)
        s.fill(self.box_color)
        screen.blit(s, self.dialogue_box_rect)

        # Get current dialogue line
        current_line = self.current_dialogue_lines[self.current_dialogue_line_index]
        text_surface = self.font.render(current_line, True, self.text_color)
        
        # Position text inside the dialogue box
        text_rect = text_surface.get_rect(center=(self.dialogue_box_rect.centerx, self.dialogue_box_rect.centery))
        screen.blit(text_surface, text_rect)