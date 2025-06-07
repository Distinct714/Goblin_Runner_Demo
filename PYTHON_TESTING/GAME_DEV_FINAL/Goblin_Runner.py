import pygame as pg
import sys
import random 

from character import Character
from game_menu import GameMenu
from level_display import LevelDisplay
from dialogue import Dialogue
from enemy import Enemy

class Goblin_Runner:
    def __init__(self):
        pg.init()
        
        self.info = pg.display.Info()
        self.screen_width = self.info.current_w
        self.screen_height = self.info.current_h

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height), pg.FULLSCREEN)

        self.game_level = LevelDisplay(
            self.screen_width,
            self.screen_height,
            level_font_size=100,
            level_text_pos_y=250
        )

        self.current_level = 1
        self.MAX_LEVEL = 3
        self.COMPLETION_SCREEN_ID = 4 
        self.GAME_OVER_PLACEHOLDER_ID = 99

        self.game_active = False # Game starts inactive (menu or dialogue first)
        
        self.game_dialogue = Dialogue(self.screen_width, self.screen_height)

        # Character initial position
        initial_char_x = 160
        initial_char_y = self.screen_height - 220 

        self.character = Character(self.screen_width, self.screen_height, initial_char_x, initial_char_y)

        self.enemy_system = Enemy(self.screen_width, self.screen_height, self.MAX_LEVEL)

        self.clock = pg.time.Clock()

        self.menu = GameMenu(self.screen, self)

        # Cooldown for level transitions to prevent immediate re-triggering
        self.level_transition_cooldown = 0
        self.COOLDOWN_FRAMES = 60   

        pg.display.flip() # Initial screen flip

    def run_game(self):
        running = True
        
        # Set initial dialogue for Level 1 when the game first starts
        self.game_dialogue.set_level_dialogue(self.current_level)

        while running:
            events = pg.event.get()

            for event in events:
                if event.type == pg.QUIT:
                    running = False
                    
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q: # Quit game with 'q'
                        running = False
                        
                    if event.key == pg.K_SPACE: # Handle Spacebar for dialogue/menu/jump
                        # Priority 1: Dialogue is active
                        if self.game_dialogue.is_dialogue_active():
                            if not self.game_dialogue.advance_dialogue():
                                # Dialogue has ended, activate gameplay
                                self.game_active = True
                                self.level_transition_cooldown = self.COOLDOWN_FRAMES 
                                # Start enemy movement only for actual gameplay levels
                                if self.current_level <= self.MAX_LEVEL:
                                    self.enemy_system.start_movement_for_level(self.current_level)
                                print(f"DEBUG: Dialogue ended. Game active: {self.game_active}.")
                                
                        # Priority 2: On Completion screen or Game Over state
                        elif self.current_level == self.COMPLETION_SCREEN_ID or self.current_level == self.GAME_OVER_PLACEHOLDER_ID:
                            self.reset_game_for_menu() # Return to main menu
                            self.menu.menu_active = True
                            self.game_active = False
                            print("DEBUG: Special screen Space press. Returning to menu.")

                        # Priority 3: Game is active and not on special screen, allow character to jump
                        elif self.game_active and self.current_level <= self.MAX_LEVEL:
                            self.character.jump()
                            print("DEBUG: Space pressed during active gameplay, attempting jump.")

                # Handle character horizontal movement input
                if self.game_active and self.current_level <= self.MAX_LEVEL: # Only allow movement during active gameplay levels
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_LEFT:
                            self.character.moving_left = True
                        if event.key == pg.K_RIGHT:
                            self.character.moving_right = True
                    elif event.type == pg.KEYUP:
                        if event.key == pg.K_LEFT:
                            self.character.moving_left = False
                        if event.key == pg.K_RIGHT:
                            self.character.moving_right = False

            # Game State Management
            if not self.game_active:
                if self.menu.menu_active:
                    self.menu.handle_events(events)
                    self.menu.draw()
                
                elif self.game_dialogue.is_dialogue_active():
                    if self.current_level == self.GAME_OVER_PLACEHOLDER_ID:
                        self.screen.fill((0, 0, 0)) # Black background for game over dialogue
                    elif self.current_level == self.COMPLETION_SCREEN_ID:
                        self.game_level._draw_thank_you_screen(self.screen)
                    else:
                        self.game_level.draw_background(self.screen, self.current_level)
                    self.game_dialogue.draw_dialogue(self.screen)
                    pg.display.flip()
                
                # If it's a special screen (Completion or Game Over) but dialogue isn't active
                elif self.current_level == self.COMPLETION_SCREEN_ID:
                    self.game_level._draw_thank_you_screen(self.screen)
                    pg.display.flip()
                elif self.current_level == self.GAME_OVER_PLACEHOLDER_ID:
                    self.screen.fill((0, 0, 0))
                    pg.display.flip()
                
                else:
                    self.game_dialogue.start_dialogue()
                    print(f"DEBUG: Starting dialogue for level {self.current_level}.")

            else: # Game is active, run gameplay loop
                # Decrement cooldown timer if active
                if self.level_transition_cooldown > 0:
                    self.level_transition_cooldown -= 1

                # Update game elements
                self.character.update()
                
                if self.current_level <= self.MAX_LEVEL: # Only update/draw enemy on gameplay levels
                    self.enemy_system.update(self.current_level)

                    # Collision detection between character and enemy
                    current_enemy_rect = self.enemy_system.get_current_enemy_rect(self.current_level)
                    if self.character.rect.colliderect(current_enemy_rect):
                        print("DEBUG: Collision detected! Game Over.")
                        self.current_level = self.GAME_OVER_PLACEHOLDER_ID # Set to game over state ID
                        self.game_active = False # End active gameplay
                        self.game_dialogue.set_level_dialogue(self.current_level) # Load game over dialogue
                        self.game_dialogue.start_dialogue() # Start displaying game over message
                        
                # Level Transition Logic (moving right off screen)
                if self.current_level <= self.MAX_LEVEL and self.level_transition_cooldown <= 0:
                    if self.character.rect.right >= self.screen_width:
                        if self.current_level < self.MAX_LEVEL:
                            self.current_level += 1
                            self.game_dialogue.set_level_dialogue(self.current_level)
                            self.game_dialogue.start_dialogue()
                            self.game_active = False # Pause gameplay for new level dialogue
                            self.level_transition_cooldown = 0 # Reset cooldown
                            self.character.rect.x = 5 # Reset character position to left side
                            self.character.moving_right = False
                            self.character.moving_left = False
                            # Reset enemy for new level
                            self.enemy_system.reset_for_level(self.current_level)
                        else:
                            # Reached max level, transition to game completion screen
                            self.current_level = self.COMPLETION_SCREEN_ID 
                            self.game_active = False
                            self.character.rect.right = self.screen_width # Keep character on screen
                            self.game_dialogue.set_level_dialogue(self.current_level) # Load completion dialogue
                            self.game_dialogue.start_dialogue() # Start displaying completion message
                    
                    # Check for transition to previous level (moving left off screen)
                    elif self.character.rect.left <= 0:
                        if self.current_level > 1:
                            self.current_level -= 1
                            self.game_dialogue.set_level_dialogue(self.current_level)
                            self.game_dialogue.start_dialogue()
                            self.game_active = False # Pause gameplay for new level dialogue
                            self.level_transition_cooldown = 0 # Reset cooldown
                            self.character.rect.x = self.screen_width - self.character.rect.width - 5 # Reset character position to right side
                            self.character.moving_left = False
                            self.character.moving_right = False
                            # Reset enemy for previous level
                            self.enemy_system.reset_for_level(self.current_level)
                        else:
                            self.character.rect.left = 1 # Prevent going below screen left on Level 1

                # Drawing everything
                self.game_level.draw_background(self.screen, self.current_level) 
                
                if self.current_level <= self.MAX_LEVEL: # Only draw character on gameplay levels
                    self.character.draw(self.screen)
                    self.enemy_system.draw(self.screen, self.current_level) # Draw enemy
                
                if self.current_level <= self.MAX_LEVEL:
                    self.game_level.draw_level_text(self.screen, self.current_level)

                pg.display.flip() # Update the full screen

            self.clock.tick(60) # Cap frame rate at 60 FPS
            
        pg.quit()
        sys.exit()

    def reset_game_for_menu(self):
        """
        Resets the game state to allow returning to the main menu for a new playthrough.
        """
        self.current_level = 1
        self.game_active = False
        self.game_dialogue.dialogue_active = False # Ensure dialogue is not active

        self.game_dialogue.current_dialogue_line_index = 0
        self.game_dialogue.set_level_dialogue(self.current_level) # Reset dialogue to Level 1

        self.character.rect.x = 160
        self.character.moving_left = False
        self.character.moving_right = False

        self.enemy_system.reset_all_enemies()

        self.level_transition_cooldown = 0


if __name__ == '__main__':
    game = Goblin_Runner()
    game.run_game()