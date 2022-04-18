import sys
from time import sleep

import pygame

from settings import Settings
from game_stats  import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings =  Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        #If you want it in full screen mode:
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion by Dr Nicolas Schulz")
        
        #Create and instaqnce to store game statistics.
        self.stats =GameStats(self)
        
        #Create a scoreboard.
        self.sb = Scoreboard(self)
                
        #Create instance of the ship. 
        self.ship = Ship(self)
        
        #Create instance of the bullet.
        self.bullets = pygame.sprite.Group()
        
        #Create a group to hold the fleet of aliens.
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        #Create the Play button.
        self.play_button = Button(self, "Play")
        # This code creates an instance of Button with the label Play,
        # but it doesn’t draw the button to the screen. We’ll call the
        # button’s draw_button() method in _update_screen()
                
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()  
                                              
    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)    
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active: 
            #The second argument in the if, prevents the button from beaing active if you are playing. 
            #Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self._start_game()
            
    def _start_game(self):
        #Reset the game statistics.
        self.stats.reset_stats()
        
        #Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        
        #Start the game
        self.stats.game_active = True
        
        #Reset score from previous games.
        self.sb.prep_score()
        
        #Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        
        #Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()
                                
    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            #Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            #Move the ship to the left.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
                        
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            #Move the ship to the right.
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            #Move the ship to the left.
            self.ship.moving_left = False
            
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet positions.
        self.bullets.update()  
        #Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            #Check that the bullets are actually removed. 
            # print(len(self.bullets)) 
        #Check for any bullets that have hit aliens.
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """Check for any bullets that have hit aliens. If so, get rid of both, the bullet and the alien."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            #If entire fleet is destroyed then erase existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            
            #Increase game speed for the next round.
            self.settings.increase_speed()
            
        if collisions:
            #Update the score if an alien is hit.
            for aliens in collisions.values():
                # any bullet that collides with an alien becomes a key in the collisions dictionary. The
                # value associated with each bullet is a list of aliens it has collided with.
                self.stats.score += self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            #Decrement ships_left.
            self.stats.ships_left -= 1
            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            #Create a new fleet and center the player's ship.
            self._create_fleet()
            self.ship.center_ship()
            #Pause
            sleep(0.5)
        else:
            #Set flag for end game.
            self.stats.game_active = False
            
            #Make mouse cursor reappear.
            pygame.mouse.set_visible(True)
        
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:    
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break
      
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        #Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Look for aliens hitting the bottom of the screen. 
        self._check_aliens_bottom()
            
    def _create_fleet(self):
        """Create the fleet of Aliens."""
        
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        #Calculate how much space in the x direction is available (leaving an alien width space in both ends).
        available_space_x = self.settings.screen_width - (2*alien_width)
        
        #Calcualte how many aliens I can fit in that space (leaving an alien width space in between).
        number_aliens_x = available_space_x // (2*alien_width)
        
        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height) 
        number_rows = available_space_y // (2 * alien_height)
        
        #Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        #Create an alien and find the number of aliens in a row.
        #Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        #Each alien is pushed to the right one alien width from the left margin.
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x =  alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien) #Add alien to the aliens group (the alien fleet).
        
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *=-1
                                     
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        #Redraw the screen during each pass trhough the loop.
        self.screen.fill(self.settings.bg_color)
        
        #Draw ship.
        self.ship.blitme()
        
        #Draw bullets  
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  
        self.aliens.draw(self.screen)
        
        #Draw the score information.
        self.sb.show_score() 
        
        #Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
             
        #Make the most recently drawn screen visible.
        pygame.display.flip()
        
        
if __name__ == '__main__':
    #Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()

  
