import pygame.font

class Button:
    
    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        #Set the dimensions and properties of the buttom.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('fonts/DEADCRT.ttf', 40) 
        #The None argument tells Pygame to use the default font, and 48
        # specifies the size of the text.
        
        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        #The button message needs to be prepped only once.
        self._prep_msg(msg)
      
     #Pygame works with text by rendering the string you
    # want to display as an image.     
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) 
        #Second argument to false if you don't want AA on yourt font (i.e. if you want pixel style on).
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        #Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
        
        
        