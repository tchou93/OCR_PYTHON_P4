from typing import List
import time
from .match import Match

class Tour:
    """Tour."""

    def __init__(self, name):
        """Has a presentation for tour."""
        self.matchs: List[Match] = []
        self.name = name

    def __str__(self):
        """Used in print."""
        str_matchs = f"Round {self.name} : "
        for match in self.matchs:
            str_matchs += str(match) +" "
        str_matchs += "\n"
        return str_matchs

    def set_start_time(self):
        self.start_time = time.strftime("%A %d %B %Y %H:%M:%S")

    def set_finish_time(self):
        self.finish_time = time.strftime("%A %d %B %Y %H:%M:%S")
        
    def get_start_time(self):
        return self.start_time 

    def get_start_time(self):
        return self.finish_time

    def add_match(self, match):
        self.matchs.append(match)

        