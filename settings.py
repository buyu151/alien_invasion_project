from re import S


class Settings:
    """A classs to store all settings for the game Alien Invasion."""
    
    def __init__(self):
        """Initialize game settings."""
        
        #Initialize game's static settings.
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        #Ship settings.
        self.ship_limit = 3
        
        #Bullets settings.
        self.bullet_width = 10
        self.bullet_height = 25
        self.bullet_color = (170, 255, 0)
        self.bullets_allowed = 3
        
        #Alien settings.
        self.fleet_drop_speed = 10
                
        #How quickly the game speeds up.
        self.speedup_scale = 1.1
        
        #How quickly the alien points values increase.
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initilize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.5
        #Scoring
        self.alien_points = 50
        
        # fleet_direction of 1 represents right; -1 represents left. 
        # The game start to the right and the change is manages by a method in the game itself.
        self.fleet_direction = 1
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)
        # print(self.alien_points) #Check the points change with the dificulty.
        
        
        
        
        
        
        