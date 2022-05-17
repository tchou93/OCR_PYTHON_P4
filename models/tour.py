from typing import List
import time
from xmlrpc.client import boolean
from .match import Match
from uuid import uuid4
import locale

class Tour:
    """Tour."""

    def __init__(self, name:str, start_time="-", end_time="-", matchs = None, finish = False, id=None):
        """Constructeur de la classe Tour"""
        self.name = name
        self.date_begin:str = start_time
        self.date_end:str = end_time
        self.matchs: List[Match] = [] if matchs is None else matchs
        self.finish:bool = finish
        self.id = str(uuid4()) if id is None else id
        locale.setlocale(locale.LC_ALL, 'fr_FR') 

    def __str__(self):
        """Utiliser pour avoir une représentation avec la fontion print"""
        str_matchs = f"Round {self.name} : "
        for match in self.matchs:
            str_matchs += str(match) +" "
        str_matchs += "\n"
        return f"Tournoi {self.name}:\n"+ str_matchs

    def set_date_begin(self):
        """Modifier l'heure de départ du tour"""
        self.date_begin = time.strftime("%A %d %B %Y %H:%M:%S")

    def set_date_end(self):
        """Modifier l'heure de fin du tour"""
        self.date_end = time.strftime("%A %d %B %Y %H:%M:%S")

    def add_match(self, match):
        """Ajouter un match au tournoi"""
        self.matchs.append(match)

    def serialized(self):
        matchs_in_tour_ids = [match.id for match in self.matchs]
        # for match in self.matchs:
        #     matchs_in_tour_ids.append(match.id)
        serialized_tour = {
            'name' : self.name,
            'date_begin' : self.date_begin,
            'date_end': self.date_end,
            'matchs_in_tour_ids' : matchs_in_tour_ids,
            'finish' : self.finish,
            'id' : self.id
        }
        return serialized_tour

    def deserialized(serialized_tour, matchs: List[Match]):
        matchs_in_tour_ids = serialized_tour['matchs_in_tour_ids']
        matchs_in_tour = []
        for match_in_tour_id in matchs_in_tour_ids:
            for match in matchs:
                if (match_in_tour_id == match.id):
                    matchs_in_tour.append(match)
                    break

        name = serialized_tour['name']
        date_begin = serialized_tour['date_begin']
        date_end = serialized_tour['date_end']
        matchs = matchs_in_tour
        finish = serialized_tour['finish']
        id = serialized_tour['id']
        return Tour(
            name,
            date_begin,
            date_end,
            matchs,
            finish,
            id)