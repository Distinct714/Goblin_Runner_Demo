# MAIN PROGRAM 

# Import the existing modules 
import pygame as pg 
import sys 

# Import the modules coming from the other directories 
from character import Character  
from game_menu import GameMenu
from level_display import LevelDisplay 
from dialogue import Dialogue 
from enemy import Enemy  
from music import Music


class Goblin_Runner: 

    def __init__(self): 
        # Initialize all Pygame modules. 
        pg.init() 
        
        # Get display information for screen size. Then, store current screen width and height. 
        self.info = pg.display.Info() 
        self.screen_width = self.info.current_w 
        self.screen_height = self.info.current_h 

        # Set up the display screen in fullscreen mode. 
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height), pg.FULLSCREEN)

        # Define font path for the display game text. 
        self.font_path = 'GAME_DEV_FINAL/assets/font/bytebounce/ByteBounce.ttf' 

        # Initialize level display. 
        self.game_level = LevelDisplay(self.screen_width, self.screen_height, level_font_size=100, level_text_pos_y=250) 
        
        # Set initial and maximum game level. 
        self.current_level = 1 
        self.MAX_LEVEL = 3 

        # Set up Game State 
        self.STATE_MAIN_MENU = 0 
        self.STATE_LEVEL_DIALOGUE = 1 
        self.STATE_TUTORIAL_GAMEPLAY = 2 
        self.STATE_GAMEPLAY = 3 
        self.STATE_GAME_OVER = 4 
        self.STATE_GAME_COMPLETED = 5 
        self.STATE_CREDITS = 6 

        # Set initial game state to main menu. 
        self.game_state = self.STATE_MAIN_MENU 

        # Flag to control active gameplay. 
        self.game_active = False 
        
        # Initialize dialogue system. 
        self.game_dialogue = Dialogue(self.screen_width, self.screen_height) 

        # Define character size and its position. 
        self.character_size = 90 
        initial_char_x = 160 
        initial_char_y = self.screen_height - 200 

        # Initialize character management system. 
        self.character = Character(self.screen_width, self.screen_height, initial_char_x, initial_char_y, self.character_size) 

        # Initialize enemy management system. 
        self.enemy_system = Enemy(self.screen_width, self.screen_height, self.MAX_LEVEL) 

        # Create Pygame clock for frame rate control. 
        self.clock = pg.time.Clock() 

        # Initialize main menu management system 
        self.menu = GameMenu(self.screen, self) 

        # Initialize music management system
        self.audio_manager = Music() 
        self.audio_manager.play_background_music()

        # Set up timer to prevent fast level changes. 
        self.level_transition_cooldown = 0 

        # Adjusts character's collision box size. 
        self.collision_offset = 50

        pg.display.flip() 

    def run_game(self): 
        # Control Main Game Loop. 
        running = True 
        
        while running: 
            # Get all Pygame events. 
            events = pg.event.get() 

            for event in events: 
                if event.type == pg.QUIT: 
                    running = False 
                
                # If a key is pressed down and pressed 'q', the game will exit 
                elif event.type == pg.KEYDOWN: 
                    if event.key == pg.K_q: 
                        running = False 
                    
                    # If Spacebar is pressed, the following decision will be made. 
                    elif event.key == pg.K_SPACE: 

                        # If dialogue is active, appear dialogue text 
                        if self.game_dialogue.is_dialogue_active(): 

                            # Advance dialogue, if it ends. 
                            if not self.game_dialogue.advance_dialogue(): 
                                
                                # If Level 1 dialogue finished, proceed to tutorial 
                                if self.game_dialogue.last_dialogue_level_completed == 1: 
                                    self.game_state = self.STATE_TUTORIAL_GAMEPLAY 
                                    self.game_level.start_tutorial() 
                                    self.game_dialogue.last_dialogue_level_completed = None 

                                # If Level 2 or 3 dialogue finished, gameplay will activate and start enemy movement. 
                                elif self.game_dialogue.last_dialogue_level_completed in [2, 3]: 
                                    self.game_state = self.STATE_GAMEPLAY 
                                    self.game_active = True 
                                    self.level_transition_cooldown = self.game_dialogue.COOLDOWN_FRAMES 
                                    self.enemy_system.start_movement_for_level(self.current_level) 
                                
                                # If game completion dialogue finished, return to main menu. 
                                elif self.game_dialogue.last_dialogue_level_completed == 4: 
                                    self.reset_game_for_menu() 
                        
                        # If game over or completed, return to main menu. 
                        elif self.game_state in [self.STATE_GAME_OVER, self.STATE_GAME_COMPLETED]: 
                            self.reset_game_for_menu() 

                        # If in tutorial or gameplay, make character jump. 
                        elif self.game_state in [self.STATE_TUTORIAL_GAMEPLAY, self.STATE_GAMEPLAY]: 
                            self.character.jump() 
            
            # If in main menu, handle menu interactions and draw its elements 
            if self.game_state == self.STATE_MAIN_MENU: 
                self.menu.handle_events(events) 
                self.menu.draw() 
            
            # If in level dialogue, draw level background and dialogue box and text. 
            elif self.game_state == self.STATE_LEVEL_DIALOGUE: 
                self.game_level.draw_background(self.screen, self.current_level) 
                self.game_dialogue.draw_dialogue(self.screen) 
            
            # If in tutorial, draw Level 1 background. 
            elif self.game_state == self.STATE_TUTORIAL_GAMEPLAY: 
                self.game_level.draw_background(self.screen, self.current_level) 

                # Get currently pressed keys. 
                keys = pg.key.get_pressed() 

                # Update character movement and animation and draw character.. 
                self.character.update(keys) 
                self.character.draw(self.screen) 
                
                # Update and draw tutorial. 
                tutorial_completed = self.game_level.update_and_draw_tutorial(self.screen, keys) 

                # If tutorial is finished, activate gameplay and start enemy movement. 
                if tutorial_completed: 
                    self.game_state = self.STATE_GAMEPLAY 
                    self.game_active = True  
                    self.level_transition_cooldown = self.game_dialogue.COOLDOWN_FRAMES 
                    self.enemy_system.start_movement_for_level(self.current_level) 

            # If game is over, draw game over screen. 
            elif self.game_state == self.STATE_GAME_OVER: 
                self.game_level.draw_game_over_screen(self.screen) 
            
            # If game is completed, draw game completion screen like thank you message. 
            elif self.game_state == self.STATE_GAME_COMPLETED: 
                self.game_level.draw_thank_you_screen(self.screen) 
            
            # If in credits screen, allow menu to handle events and draw credits. 
            elif self.game_state == self.STATE_CREDITS: 
                self.menu.handle_events(events) 
                self.menu.draw_credits_screen() 

            # If in active gameplay, update character and get pressed keys. 
            elif self.game_state == self.STATE_GAMEPLAY:
                
                # If cooldown is active, decrease cooldown timer. 
                if self.level_transition_cooldown > 0: 
                    self.level_transition_cooldown -= 1

                keys = pg.key.get_pressed()
                self.character.update(keys)
                
                # If within valid gameplay levels, update enemy. 
                if self.current_level <= self.MAX_LEVEL: 
                    self.enemy_system.update(self.current_level, self.character.rect) 

                    # Create smaller collision rect for character. 
                    shrunk_char_rect = self.character.rect.inflate(-self.collision_offset * 2, -self.collision_offset * 2) 

                    # Get enemy collision rectangles. 
                    enemy_rects_for_level = self.enemy_system.get_current_enemy_rects(self.current_level)

                    # Check each enemy for collision. 
                    for enemy_rect in enemy_rects_for_level: 

                        # If character collides with enemy, set the game to game over and stop checking for more collisions. 
                        if shrunk_char_rect.colliderect(enemy_rect): 
                            self.game_state = self.STATE_GAME_OVER
                            self.game_active = False
                            self.audio_manager.stop_music()
                            break 
                
                # Checks if not on cooldown and still within game levels
                if self.current_level <= self.MAX_LEVEL and self.level_transition_cooldown <= 0:

                    # If character moves off right side and still no reach the last level, advance to next level.
                    if self.character.rect.right >= self.screen_width:
                        if self.current_level < self.MAX_LEVEL:
                            self.current_level += 1 

                            # Start new dialogue in each level.
                            self.game_dialogue.set_level_dialogue(self.current_level) 
                            self.game_dialogue.start_dialogue() 
                            self.game_state = self.STATE_LEVEL_DIALOGUE 
                            self.game_active = False 

                            # Reset cooldown. 
                            self.level_transition_cooldown = self.game_dialogue.COOLDOWN_FRAMES 

                            # Reset character X position and enemy's position for new level.
                            self.character.rect.x = 5 
                            self.enemy_system.reset_for_level(self.current_level) 

                        else:  
                            # If it's the last level, set game to completed and deactivate gameplay. 
                            self.game_state = self.STATE_GAME_COMPLETED  
                            self.game_active = False 
                            
                            # Keep character on screen and reset all enemies. 
                            self.character.rect.right = self.screen_width  
                            self.enemy_system.reset_all_enemies() 

                    # If character moves off left side, prevent going to previous level.
                    elif self.character.rect.left <= 0: 
                        # Keep character on screen at the left edge.
                        self.character.rect.left = 1 
                                
                # Draw background images in each levels. 
                self.game_level.draw_background(self.screen, self.current_level) 
                
                # If within specified gameplay levels, draw character and enemy. 
                if self.current_level <= self.MAX_LEVEL: 
                    self.character.draw(self.screen) 
                    self.enemy_system.draw(self.screen, self.current_level) 
                
                # Draw level text. 
                self.game_level.draw_level_text(self.screen, self.current_level) 
            
            pg.display.flip() 
            self.clock.tick(60) 

        self.audio_manager.quit_mixer()
        pg.quit() 
        sys.exit() 

    def start_game(self): 
        # Start the game through dialogue first.
        self.menu.menu_active = False 
        self.current_level = 1 
        self.game_dialogue.set_level_dialogue(self.current_level) 
        self.game_dialogue.start_dialogue() 

        # Set game state to dialogue. 
        self.game_state = self.STATE_LEVEL_DIALOGUE 

        # Deactivate gameplay for dialogue. 
        self.game_active = False 

        # Reset character position after dialogue in each levels and set character to idle. 
        self.character.rect.x = 160 
        self.character.rect.y = self.screen_height - 200 
        self.character.update({pg.K_a: 0, pg.K_d: 0})  
        
        # Reset all enemies in each levels. 
        self.enemy_system.reset_all_enemies() 

        # Reset cooldown and tutorial state 
        self.level_transition_cooldown = 0 
        self.game_level.reset_tutorial() 

    def reset_game_for_menu(self): 
        # Reset to level 1 and Deactivate gameplay and dialogue. 
        self.current_level = 1 
        self.game_active = False 
        self.game_dialogue.dialogue_active = False 

        # Reset dialogue in game levels. 
        self.game_dialogue.current_dialogue_line_index = 0 
        self.game_dialogue.set_level_dialogue(self.current_level) 
        self.game_dialogue.last_dialogue_level_completed = None 

        # Reset character position and set character to idle. 
        self.character.rect.x = 160 
        self.character.rect.y = self.screen_height - 220 
        self.character.update({pg.K_a: 0, pg.K_d: 0}) 

        # Reset all enemies. 
        self.enemy_system.reset_all_enemies() 

        # Reset cooldown and tutorial state 
        self.level_transition_cooldown = 0 
        self.game_level.reset_tutorial() 
        
        # Set game state to main menu and activate the menu. 
        self.game_state = self.STATE_MAIN_MENU 
        self.menu.menu_active = True 

if __name__ == '__main__': 
    # Create a new game instance and run it. 
    game = Goblin_Runner() 
    game.run_game()
