import traceback

class GameStats:
    """Track statistics for Alien Invasion."""
    """
    This keeps track of stuff like collisions, so we can track how many points we scored playing the game, or how many lives we have left (if the aliens collide with the ship)
    """
    def __init__(self, ai_game):
        """ Constructor, initializes statistics instance """
        self.settings = ai_game.settings_for_game
        # takes a copy of the same settings used by the game
        self.reset_stats()
        # resets values (score, lives, etc.) for a new game
        try:
            with open('hiscores/hiscores.txt', 'r') as file:
                self.high_score = int(file.read())
            # the highest score earned. this is saved in the specified file elsewhere, and when a new instance of the game starts, the previous hi score is loaded and displayed so that it never goes away
        except Exception:
            print("Unable to open previous highscores, setting high scores to 0. Exception details --> ")
            traceback.print_exc()
        # exception handling in case the file specified could not be read or has invalid data (not a number) in it
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives = self.settings.ship_limit
        # sets the lives equal to whatever we set in the settings
        # as this is called at the beginning of the game, this essentially sets the initial lives a player has
        self.score = 0
        # sets initial score of game to 0. score is reset every time this method is called
        self.level = 1
        # sets the default starting level; increments as more rounds are completed (and fleets defeated)