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
        
        #Bullets settings.
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        
        #Alien settings.
        self.alien_speed = 0.3
        
        
        
        