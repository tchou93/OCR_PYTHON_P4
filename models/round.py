import time
import locale
from typing import List
from uuid import uuid4
from .match import Match


class Round:
    def __init__(
        self,
        name: str,
        start_time="-",
        end_time="-",
        matchs=None,
        finish=False,
        id=None,
    ):
        self.name = name
        self.date_begin: str = start_time
        self.date_end: str = end_time
        self.matchs: List[Match] = [] if matchs is None else matchs
        self.finish: bool = finish
        self.id = str(uuid4()) if id is None else id
        locale.setlocale(locale.LC_ALL, "fr_FR")

    def __repr__(self):
        """Used for print."""
        str_matchs = f"Round {self.name} : "
        for match in self.matchs:
            str_matchs += str(match) + " "
        str_matchs += "\n"
        return f"Tournoi {self.name}:\n" + str_matchs

    def set_date_begin(self):
        """Modifier l'heure de départ du Round"""
        self.date_begin = time.strftime("%A %d %B %Y %H:%M:%S")

    def set_date_end(self):
        """Modifier l'heure de fin du Round"""
        self.date_end = time.strftime("%A %d %B %Y %H:%M:%S")

    def add_match(self, match):
        """Ajouter un match au tournoi"""
        self.matchs.append(match)

    def serialized(self):
        matchs_in_round_ids = [match.id for match in self.matchs]
        serialized_round = {
            "name": self.name,
            "date_begin": self.date_begin,
            "date_end": self.date_end,
            "matchs_in_round_ids": matchs_in_round_ids,
            "finish": self.finish,
            "id": self.id,
        }
        return serialized_round

    @classmethod
    def deserialized(cls, serialized_round, matchs: List[Match]):
        matchs_in_round_ids = serialized_round["matchs_in_round_ids"]
        matchs_in_round = []
        for match_in_round_id in matchs_in_round_ids:
            for match in matchs:
                if match_in_round_id == match.id:
                    matchs_in_round.append(match)
                    break

        name = serialized_round["name"]
        date_begin = serialized_round["date_begin"]
        date_end = serialized_round["date_end"]
        matchs = matchs_in_round
        finish = serialized_round["finish"]
        id = serialized_round["id"]
        return cls(name, date_begin, date_end, matchs, finish, id)
