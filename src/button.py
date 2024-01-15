import pygame.font

class Button:
    """A class to build buttons for the game"""
    def __init__(self, ai_game, msg):
        # constructor takes an instance of the game and whatever msg we want in the button as params
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # game screen fields, using the same screen as the game instance
        
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # Button dimensions and other properties
        
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # Setting rectangle center as the center of the screen, effectively centering the button
        self.rect.center = self.screen_rect.center
        # Everything in pygame is a rectangle, so this button must be one too. This creates that rectangle. It is originally created at 0, 0 but then shifted the screen center
        
        self._prep_msg(msg)
        # message of the button
        
    def _prep_msg(self, msg): 
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # Converts the message text into an image; with the text as the same color as specified in the constructor, field "text_color"
        self.msg_image_rect = self.msg_image.get_rect()
        # gets the rectangle of the image generated from the text above
        self.msg_image_rect.center = self.rect.center
        # centers the image to the center of the rectangle in which the image will go
        
    def draw_button(self):
        """Bringing the above together; draws a button and then draws the image within the button to give a button with text in it"""
        self.screen.fill(self.button_color, self.rect)
        # Draws an empty rectangle with the specified color in the constructor
        self.screen.blit(self.msg_image, self.msg_image_rect)
        # Draws the text image from _prep_msg into the button rectangle