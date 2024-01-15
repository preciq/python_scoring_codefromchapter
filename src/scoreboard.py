import pygame.font
import traceback
from pygame.sprite import Group
from ship import Ship

class Scoreboard: 
    """A class to report scoring information"""
    
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen 
        self.screen_rect = self.screen.get_rect() 
        self.settings = ai_game.settings_for_game
        self.stats = ai_game.stats
        # gets and updates the score from here
        
        # initial values required for showing displayable score on screen
        
        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # score color, font and size set with above settings
        
        # Prepare the initial score image.
        self.prep_score()
        # The score will be displayed as an image, rendered from some text, similar to the play button
        self.prep_high_score()
        # The high score will be displayed as an image, similar to prep_score
        self.prep_level()
        # the level will be displayed as an image as well, like the high score and the score
        self.prep_ships()
        # the number of lives will be displayed as a grouping of ships
        
    def prep_score(self): 
        """Turn the score into a rendered image from text"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        # we round the score first to the nearest tenth (which is what the -1 does)
        # we then use an f string followed by :, which python implicitly knows means we want commas inserted in the number at appropriate places (i.e. 4,302,000)
        # add a score label as well for clarity
        
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        # renders the string generated above (the score) into an image
        
        #Display the score on the top right of the screen
        self.score_rect = self.score_image.get_rect()
        #gets the rectangle for the score, in which it will be displayed
        self.score_rect.right = self.screen_rect.right - 20
        # sets the right edge of the rectangle holding the score image 20 pixels to the left of the right edge of the screen
        self.score_rect.top = 20
        # same thing as above but sets the top of the score rectangle 20 pixels BELOW the screen top
    
    def prep_high_score(self):
        """Turn the high score into a rendered image, also from text"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
        self.text_color, self.settings.bg_color)
        # Center the high score at the top of the screen.
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        # does all the stuff in the prep_score, but for hi score. may be worth refactoring the two methods to extract commonalities
    
    def prep_level(self):
        """Turn the level the player is currently on into a rendered image"""
        level_str = f"Level: {str(self.stats.level)}"
        # gets the current level stored inside the game stats (which changes dynamically, meaning this function will be called at the end of each level, once a wave is cleared)
        # takes it a string (it is originally a number)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        # renders the level as an image and stores it as an attribute
        
        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        # The level image is positioned 10 pixels below the score image
    
    def prep_ships(self): 
        """Show how many ships are left"""
        self.ships = Group()
        # creates a grouping of ships
        for ship_number in range(self.stats.lives):
            # loop runs once for every life available
            ship = Ship(self.ai_game)
            # gets a copy of the ship from the game instance (the sprite, specifically)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            # draws that sprite at a particular position (starting from the left side and moving by one ship to the right)
            # note the y axis remains unchanged
            # this will draw the number of lives player has as ships on the top left side as a row
            self.ships.add(ship)
            # these ships are also added to the grouping of ships (representing lives)
    
    def check_high_score(self): 
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            try:
                with open('hiscores/hiscores.txt', 'w') as file:
                    file.write(str(self.stats.score))
            # the highest score earned. this is saved in the specified file elsewhere, and when a new instance of the game starts, the previous hi score is loaded and displayed so that it never goes away
            except Exception:
                print("Unable to open previous highscores, setting high scores to 0. Exception details --> ")
                traceback.print_exc()
        # exception handling in case the file specified could not be read or has invalid data (not a number) in it
    
    def show_score(self):
        "Render the score, high score and the level on the screen"
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        # this last line draws the grouping of ships to the screen based on the positions assigned in prep_ships
    
    