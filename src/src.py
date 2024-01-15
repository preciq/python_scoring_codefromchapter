# Importing necessary modules
import sys  # Provides access to some variables used or maintained by the Python interpreter and to functions that interact strongly with the interpreter
from time import sleep # Imports the sleep functionality from the time module, which lets us sleep (pause) the game
import pygame  # Pygame is a set of Python modules designed for writing video games
# Importing the Settings class from the settings module
from settings import Settings
from ship import Ship  # Importing the Ship class from the ship module
from bullet import Bullet  # Importing the Bullet class from the bullet module
from alien import Alien # Imports the Alien class from the alien module
from game_stats import GameStats # Game stats import
from button import Button #import button class from Button
from scoreboard import Scoreboard

# The main class for the game
class AlienInvasion:
    # The constructor method for the class
    def __init__(self):
        pygame.init()  # Initialize all imported pygame modules
        self.settings_for_game = Settings()  # Create an instance of Settings

        self.game_active = False
        # boolean flag for tracking if the game is active; will be used to shut game down when lives reach 0
        # initially set to false; player must start the game by clicking the play button (described below), game does not automatically start

        # Create a display surface
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # full screen mode
        self.screen = pygame.display.set_mode((1200, 800))
        # Get the width of the screen and store it in settings
        self.settings_for_game.screen_width = self.screen.get_rect().width
        # Get the height of the screen and store it in settings
        self.settings_for_game.screen_height = self.screen.get_rect().height

        # Set the title of the window
        pygame.display.set_caption("Alien invasion remaster")
        # Create a clock object to control the frame rate
        self.clock = pygame.time.Clock()
        # Set the background color
        self.bg_color = (self.settings_for_game.bg_color)
        
        self.stats = GameStats(self)
        # creates a new instance of a GameStats (for keeping track of statistics in the game like score or lives)
        self.sb = Scoreboard(self)
        # creates a new instance of a scoreboard (for keeping track of the current player score)
        
        # Create an instance of Ship
        self.ship = Ship(self)
        # Create a group to store all bullets
        self.bullets = pygame.sprite.Group()
        # Create a group to store the alien fleet (all generated aliens)
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        self.play_button = Button(self, "Play")
        # generates a "play" button for the game
        

    # Method to start the main loop for the game
    def run_game(self):
        # Start the main loop
        while (True):
            # Check for events
            self._check_events()
            # Update the ship's position
            # still need to check this even if the game is inactive, because the player may press Q to quit
            
            if self.game_active: 
                # only do the following IF the game is active (determined elsewhere by if the player has lives)
                self.ship.update()
                # Update the bullets' positions
                self._update_bullets()
                # Update the aliens positions 
                self._update_aliens()

            # Update the screen
            self._update_screen()
            # Limit the frame rate to 60 FPS
            self.clock.tick(60)

    # Method to check for events
    def _check_events(self):
        # Loop through all events
        for event in pygame.event.get():
            # If the event is QUIT, exit the program
            if event.type == pygame.QUIT:
                sys.exit
            # If the event is a key press
            elif event.type == pygame.KEYDOWN:
                # Check which key was pressed
                self._check_keydown_events(event)
            # If the event is a key release
            elif event.type == pygame.KEYUP:
                # Check which key was released
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if the mouse button is pressed
                mouse_pos = pygame.mouse.get_pos()
                # this returns the position the mouse button was pressed at, in the form of a tuple
                self._check_play_button(mouse_pos)
                # checks if the mouse button was pressed on top of the "Play" button
                # if so, starts a game
                
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if(self.play_button.rect.collidepoint(mouse_pos) and not self.game_active):
            # checks if the mouse_pos provided (coordinates of a click) collide with (overlap) the Play button
            # also checks if the game is inactive (we only want to start a new game if the game is not active; without the second boolean condition, the game would restart every time someone clicks in the play button area, even if the button is not there!)
            
            self.settings_for_game.initialize_dynamic_settings()
            # sets (or resets if this is second or subsequent game) the game settings (the dynamic ones) back to their original starting values when a new game starts 
            
            self.stats.reset_stats()
            # resets the game stats for a new game (gives the player 3 new lives)
            self.sb.prep_score()
            # reset_stats sets the score to 0. prep_score then renders that 0 to the game window
            
            self.sb.prep_high_score()
            # reloads the high score; if this game caused a new high score to be registered, that high score has been written to the persistent txt file. This then reloads the high score for display 
            
            self.sb.prep_level()
            # prepares the level
            
            self.sb.prep_ships()
            # loads the ship-lives on the top right corner
            
            self.game_active = True
            # if the if statement is true, then a valid click was made, which means the game can begin 
            
            self.bullets.empty()
            self.aliens.empty()
            # clears out all existing aliens and bullets for a new game
            
            self._create_fleet()
            self.ship.center_ship()
            # creates a new fleet and centers the ship for a new game
            
            pygame.mouse.set_visible(False)
            # when the player clicks "Play", the mouse cursor is no longer needed and is therefore hidden
        
    # Method to handle key press events
    def _check_keydown_events(self, event):
        # If the right arrow key is pressed, move the ship to the right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # If the left arrow key is pressed, move the ship to the left
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # If the 'q' key is pressed, exit the program
        elif event.key == pygame.K_q:
            sys.exit()
        # If the space bar is pressed, fire a bullet
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    # Method to handle key release events
    def _check_keyup_events(self, event):
        # If the right arrow key is released, stop moving the ship to the right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        # If the left arrow key is released, stop moving the ship to the left
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Method to fire a bullet
    def _fire_bullet(self):
        # If the number of bullets is less than the maximum allowed
        if len(self.bullets) < self.settings_for_game.bullets_allowed:
            # Create a new bullet and add it to the bullets group
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Method to update the bullets
    def _update_bullets(self):
        # Update the position of all bullets
        self.bullets.update()

        self._handle_alien_bullet_collision_removal()
        self.remove_old_bullets()
        self._create_new_fleet_if_old_fleet_beaten()

    def _handle_alien_bullet_collision_removal(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        # here we check if 2 sprites have collided (basically if their rectangles overlap)
        # we're checking all the bullets against all of the aliens
        # if any bullet and alien collide, a key value pair is added to the return value of groupscollide (it returns a dictionary)
        # most importantly, we are telling pygame to delete both the bullet and the alien in the collision (the True values)
        # we could additionally make a penetrative bullet by setting the first boolean value to False (meaning it doesn't disappear after a collision)
        
        if collisions:
            for hits in collisions.values():
                self.stats.score += self.settings_for_game.alien_points * len(hits)
                # adds points to the score for every successful collision
                # loops through to ensure quick multiple hits in succession are also counted and not just counted once
                # i.e. bigger bullets with a large width that take out multiple aliens should now count as multiple hits
            self.sb.prep_score()
            # updates the score image, as the score has now changed
            self.sb.check_high_score()
            # this only updates the high score, it does not re-render it. For that, you play another game and the score gets re-rendered
            
    def remove_old_bullets(self):
        # Remove bullets that have left the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_new_fleet_if_old_fleet_beaten(self):
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
        # this generates a new fleet of aliens
        # if self.aliens is 'not', meaning if the aliens group (the fleet) is empty
        # delete all remaining bullets since the alient fleet is gone
        # and create a new fleet
            self.settings_for_game.increase_speed()
        # this method is called every time a new fleet is generated
        # it increases the speed of the ship, bullets and aliens based on how many rounds we have played
        
            # Increase level
            self.stats.level += 1
            self.sb.prep_level()
            # increases the level by 1 whenever a new fleet is generated, then reloads the level image so that it is rerendered on the next call of show_score()

    # Method to update the screen
    def _update_screen(self):
        # Fill the screen with the background color
        self.screen.fill(self.bg_color)
        # Draw all bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Draw the ship
        self.ship.draw_ship_blit()
        # Draws the alien fleet 
        self.aliens.draw(self.screen)
        
        self.sb.show_score()
        # renders the score image on screen, as defined in the scoreboard module

        if not self.game_active: 
            # if the game is not yet active
            self.play_button.draw_button()
            #draw the play button for the player to click
        # we put this block here so that it is rendered last, and over all other elements (don't want the play button to blocked now do we)

        # Update the display
        pygame.display.flip()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien object (1 alien)
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width.
        alien = Alien(self)
        
        # Get the width and height of a single alien, to be used to calculate how many aliens are addable
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        # Used in the loops below to calculate where to draw the next alien
        
        while current_y < (self.settings_for_game.screen_height - 3 * alien_height):
            # the outer loop will keep allowing rows of aliens to be added until it reaches the bottom of the screen
            while current_x < (self.settings_for_game.screen_width - 2 * alien_width):
                # the inner while loop will continuosly draw a row of aliens until it reaches the end of the screen (right side)
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row; reset x value (back to the left of the screen), and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, current_x, current_y):
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = current_x
        new_alien.rect.y = current_y
        self.aliens.add(new_alien)
        # a function that creates aliens. Will be used in tandem with a loop, which constantly shifts the "current_x" to the right. What this means is that whenever a new alien is drawn, it is drawn more to the right
    
    def _update_aliens(self): 
        """Update alien positions (all of them) in the fleet"""
        self._check_fleet_edges()
        # checks if any alien instance has reached the screens edge
        self.aliens.update()
        # this is a build in method; essentially it updates the alien instance on screen if its values have been changed
        # kind of like a refresh 
        
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
        # this checks if a ship was hit (collision occured between any alien in the aliens group and the ship)
            self._ship_hit()
        
        self._check_aliens_bottom()
        # checks if any aliens have made it to the bottom of the screen; one life should be taken if that is the case (basically the same thing as _ship_hit should happen)
            
    def _check_aliens_bottom(self): 
        """Check if aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            # checks every alien in the aliens group (the current fleet)
            if alien.rect.bottom >= self.settings_for_game.screen_height:
                # if the current alien being checked has a rectangle whose BOTTOM is BELOW the game screen
                self._ship_hit()
                #run the same commands as if the ship is hit and restart the game (which is inside ship_hit)
                break
                #if any alien reaches the bottom, no need to check any other alien so can break the loop here
            
    
    def _ship_hit(self):
        if self.stats.lives > 0:
            # checks if player has ships (lives) remaining
            self.stats.lives -= 1
            # removes one life if the ship is hit
            self.sb.prep_ships()
            # redraws the ships representing lives, with one less because of the above

            self.bullets.empty()
            self.aliens.empty()
            # when ship is hit, game should reset; all existing aliens and bullets are deleted

            self._create_fleet()    
            self.ship.center_ship()
            # generate a new fleet and bring the ship to the centere position when starting a new game

            sleep(0.5)
            # pause the game to let the player get their bearings for a half second
        else:
            # if no lives left, set game active flag to false
            self.game_active = False
            
            pygame.mouse.set_visible(True)
            # Mouse cursor is made visible again when player is out of lives

        
    def _check_fleet_edges(self):
        """Handles if aliens have reached the screen edge"""
        for alien in self.aliens.sprites():
            # checks every alien instance in the fleet
            if alien.check_edges(): 
                # if an alien has reached the edge of the screen
                self._change_fleet_direction()
                # then make them all go in the opposite direction and drop down (how much drop down defined in settings)
                break
    
    def _change_fleet_direction(self):
        """Drops the entire fleet and changes its direction"""
        for alien in self.aliens.sprites():
            # checks every alien instance in the fleet
            alien.rect.y += self.settings_for_game.fleet_drop_speed
            # drops each individual alien ship down by however many units are specified in the settings
        self.settings_for_game.fleet_direction *= -1
        # changes the direction in which all alien ships will move
        
# If this file is run (instead of imported), start the game
if __name__ == '__main__':
    # Create an instance of the game
    game_instance = AlienInvasion()
    # Start the game
    game_instance.run_game()
