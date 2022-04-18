import json

class GameStats:
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings 
        self.reset_stats()
        
        #High score should never be reset.
        #Instead it resides in a json file.
        with open('high_score.json', 'r') as f:
             h_score = json.load(f)
             self.high_score = int(h_score['high_score'])
        
        #Start Alien Invasion in an inactive state until play buttom is pressed.
        self.game_active = False
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0 
        self.level = 1
        
        