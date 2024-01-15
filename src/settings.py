# Define a class named Settings
class Settings:
    # The constructor method for the Settings class
    def __init__(self):
        """Initialize the game's static settings."""
        # Set the background color of the game screen to a light gray color
        # The color is specified as an RGB tuple where each value is between 0 and 255
        self.bg_color = (230, 230, 230)

        # Ship settings
        # Sets the number of lives (ships) we have per game
        self.ship_limit = 3

        # Bullet settings
        # Set the width of the bullets in pixels
        self.bullet_width = 300
        # Set the height of the bullets in pixels
        self.bullet_height = 15
        # For testing purposes, we can make large bullets to test elimination of the entire alien fleet
        
        
        # Set the color of the bullets to a dark gray color
        # The color is specified as an RGB tuple where each value is between 0 and 255
        self.bullet_color = (60, 60, 60)

        # Set the maximum number of bullets that can be on the screen at the same time
        self.bullets_allowed = 3
        
        # Alien settings
        self.fleet_drop_speed = 10
        # will control how fast the aliens drop downwards when they reach the bottom of the screen
        
        self.good_boy_mode = True
        
        # Setup how quickly game speeds up with difficulty + progression
        self.speedup_scale = 1.5
        # Setup the point multiplier as the game gets harder
        self.score_scale = 2
        
        # initialize the dynamic settings defined below as part of the constructor
        self.initialize_dynamic_settings()
        
        # Score settings
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        # Set the speed of the ship. The higher the number, the faster the ship will move
        self.ship_speed = 1.5
        # Set the speed of the bullets. The higher the number, the faster the bullets will move
        self.bullet_speed = 10.0
        self.alien_speed = 1.0
        # Set the speed of each alien
        # the above settings will change (increase) throughout the game, and are now moved to the dynamic settings
        
        self.fleet_direction = 1
        # will control which direction the alien fleet moves on the x axis
        # 1 means to the right
        # -1 means to the left
        
    def increase_speed(self): 
        """Increase speed settings + alien point multiplier"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        # multiplies the dynamic elements (scales them up) whenever this method is called, thereby speeding up the game

        self.alien_points = int(self.alien_points * self.score_scale)
        # scales up the number of points awarded for hitting an alien every time this method is called (which is usually at the end of a round when a fleet is removed)
        # this is to bring the score in line with the increasing difficulty of the game with each successive round