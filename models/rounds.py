import time

class Rounds:
    """Rounds."""

    def __init__(self, games, name):
        """Has a presentation for Rounds."""
        self.games = games
        self.name = name

    def set_start_time(self):
        self.start_time = time.strftime("%A %d %B %Y %H:%M:%S")

    def set_finish_time(self):
        self.finish_time = time.strftime("%A %d %B %Y %H:%M:%S")

    def get_start_time(self):
        return self.start_time 

    def get_start_time(self):
        return self.finish_time