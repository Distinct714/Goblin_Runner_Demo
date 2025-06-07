
# Importing Existing Modules
import sys
from time import sleep
import pygame as pg

# Importing Modules in other created directories.
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and creata game resources."""
        pg.init()
        self.clock = pg.time.Clock()
        self.settings = Settings() # Call settings.py

        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pg.display.set_caption("Alien Invasion")

        original_game_background = self.settings.bg_img
        self.background_image_scaled = pg.transform.scale(original_game_background, (self.settings.screen_width, self.settings.screen_height))

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()

        # Creating an instance of the Alien
        self._create_fleet()

        # Start alien invasion in an active state
        self.game_active = True

        # Set the background color of the screen
        self.bg_img = self.settings.bg_img

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()
            self.clock.tick(60)

            # Get rid of bullets that have disappeared
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            print(len(self.bullets))

            
            self.screen.blit(self.background_image_scaled, (0, 0)) 

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit() 
                
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pg.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pg.K_q:
                sys.exit()
            elif event.key == pg.K_SPACE:
                self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pg.K_LEFT:
                self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update the position of bullets and remove old bullets"""
        # Update bullet position
        self.bullets.update()

        # Remove bullets that disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        # Check for any bullets that have hit aliens
        # If so, get rid of the bullets and the aliens
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collision"""
        # Remove any bullets and aliens that have collided.
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
    
    def _ship_hit(self):
        """ Respond to hits from aliens"""
        if self.stats.ships_left > 0:
            # Decrement ship_left
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        
        else:
            self.game_active = False

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien ship collision
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom od the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship get hit
                self._ship_hit()
                break
    
    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Create an alien and keep adding aliens until there's no room left,
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2* alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finished a row; reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height 

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1
    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        # Redraw the screen during each pass through the loop


        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pg.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()