from re import S


class Settings:
    """A classs to store all settings for the game Alien Invasion."""
    
    def __init__(self):
        """Initialize game settings."""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        #Ship settings.
        self.ship_speed = 1.5
        self.ship_limit = 3
        
        #Bullets settings.
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        #Alien settings.
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left. 
        # The game start to the right and the change is manages by a method in the game itself.
        self.fleet_direction = 1
        
        
        
        
        