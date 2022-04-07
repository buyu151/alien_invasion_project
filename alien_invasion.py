import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings =  Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        pygame.display.set_caption("Alien Invasion by Dr Nicolas Schulz")
        
        #Set background color
        self.bg_color = self.settings.bg_color
        
        #Create instance of the ship. 
        self.ship = Ship(self)
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            #Redrwa the screen during each pass trhough the loop.
            self.screen.fill(self.bg_color)
            
            #Draw ship.
            self.ship.blitme()
                    
            #Make the most recently drawn screen visible.
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
