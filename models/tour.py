from typing import List
import time
from xmlrpc.client import boolean
from .match import Match

class Tour:
    """Tour."""

    def __init__(self, name:str):
        """Constructeur de la classe Tour"""
        self.matchs: List[Match] = []
        self.name = name
        self.start_time:str = "-"
        self.end_time:str = "-"
        self.finish:bool = False

    def __str__(self):
        """Utiliser pour avoir une représentation avec la fontion print"""
        str_matchs = f"Round {self.name} : "
        for match in self.matchs:
            str_matchs += str(match) +" "
        str_matchs += "\n"
        return f"Tournoi {self.name}:\n"+ str_matchs

    def set_start_time(self):
        """Modifier l'heure de départ du tour"""
        self.start_time = time.strftime("%A %d %B %Y %H:%M:%S")

    def set_finish_time(self):
        """Modifier l'heure de fin du tour"""
        self.end_time = time.strftime("%A %d %B %Y %H:%M:%S")

    def add_match(self, match):
        """Ajouter un match au tournoi"""
        self.matchs.append(match)

        