from typing import List
import time
from xmlrpc.client import boolean
from .match import Match
from uuid import uuid4

class Tour:
    """Tour."""

    def __init__(self, name:str, start_time="-", end_time="-", matchs = None, finish = False, id=None):
        """Constructeur de la classe Tour"""
        self.name = name
        self.start_time:str = start_time
        self.end_time:str = end_time
        self.matchs: List[Match] = [] if matchs is None else matchs
        self.finish:bool = finish
        self.id = str(uuid4()) if id is None else id

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

    def serialized(self):
        matchs_in_tour_ids = []
        for match in self.matchs:
            matchs_in_tour_ids.append(match.id)
        serialized_tour = {
            'name' : self.name,
            'start_time' : self.start_time,
            'end_time': self.end_time,
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
        start_time = serialized_tour['start_time']
        end_time = serialized_tour['end_time']
        matchs = matchs_in_tour
        finish = serialized_tour['finish']
        id = serialized_tour['id']
        return Tour(
            name,
            start_time,
            end_time,
            matchs,
            finish,
            id)
    
    # def serialized(self):
    #     serialized_player = {
    #         'first_name' : self.first_name,
    #         'last_name' : self.last_name,
    #         'birthday': self.birthday,
    #         'gender' : self.gender,
    #         'ranking' : self.ranking
    #     }
    #     return serialized_player 

    # def deserialized(serialized_player):
    #     first_name = serialized_player['first_name']
    #     last_name = serialized_player['last_name']
    #     birthday = serialized_player['birthday']
    #     gender = serialized_player['gender']
    #     ranking = serialized_player['ranking']
    #     return Player(first_name,last_name,birthday,gender,ranking)