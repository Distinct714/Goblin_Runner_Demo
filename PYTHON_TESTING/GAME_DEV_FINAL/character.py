import pygame as pg

class Character:
    def __init__(self, screen_width, screen_height, start_x, start_y):
        self.image = pg.image.load("GAME_DEV_FINAL/assets/sprite/pixel-frame-goblin_right/1.png").convert_alpha() # Added .convert_alpha() for better transparency
        self.image = pg.transform.scale(self.image, (110, 110))
        self.rect = self.image.get_rect()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.rect.x = start_x
        self.rect.y = start_y
        
        self.speed = 20 # Horizontal speed

        self.moving_left = False
        self.moving_right = False
        
        # --- NEW JUMPING VARIABLES ---
        self.is_jumping = False
        self.vertical_velocity = 0 # Current speed in the y-direction
        self.jump_power = -50    # How high the character jumps (negative for upwards movement in Pygame)
        self.gravity = 3         # How fast the character falls
        self.initial_y = start_y # The ground level (where the character lands)
        # --- END NEW JUMPING VARIABLES ---
    
    def update(self):
        """
        Update the character's position based on movement flags and apply jump physics.
        """
        # Horizontal movement
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_right:
            self.rect.x += self.speed

        # --- JUMPING LOGIC ---
        if self.is_jumping:
            self.vertical_velocity += self.gravity # Apply gravity
            self.rect.y += self.vertical_velocity # Update vertical position

            # Check if landed on the ground
            if self.rect.y >= self.initial_y:
                self.rect.y = self.initial_y # Snap to ground
                self.is_jumping = False     # Stop jumping
                self.vertical_velocity = 0  # Reset vertical speed
        # --- END JUMPING LOGIC ---

    def draw(self, screen):
        """Draw the character on the screen."""
        screen.blit(self.image, self.rect)

    # --- NEW JUMP METHOD ---
    def jump(self):
        """Initiate a jump if the character is not already jumping."""
        if not self.is_jumping:
            self.is_jumping = True
            self.vertical_velocity = self.jump_power # Set initial upward velocity
            print("DEBUG: Character initiated jump.") # Debug print
    # --- END NEW JUMP METHOD ---