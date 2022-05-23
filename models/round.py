from os import getcwd
from sys import path

try:
    path.insert(1, getcwd())
except IndexError:
    pass

import time
import locale
from typing import List, Dict, Type, TypeVar
from uuid import uuid4
from models.match import Match
from models.player import Player

T = TypeVar("T", bound="Round")


class Round:
    """Class to represent a round in a tournament"""

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
        str_matchs = f"{self.name} : "
        for match in self.matchs:
            str_matchs += str(match) + " "
        return str_matchs

    def set_date_begin(self):
        """Set the instance attribut <date_begin> at the beggining of the Round."""
        self.date_begin = time.strftime("%A %d %B %Y %H:%M:%S")

    def set_date_end(self):
        """Set the instance attribut <date_end> at the end of the Round."""
        self.date_end = time.strftime("%A %d %B %Y %H:%M:%S")

    def add_match(self, match):
        """Add a match to the instance attribut <matchs>."""
        self.matchs.append(match)

    def serialized(self) -> Dict:
        """Serialize an instance of a round.

        Returns:
            Dict: Serialization of an instance of a round.
        """
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
    def deserialized(cls: Type[T], serialized_round: Dict, matchs: List[Match]) -> T:
        """Deserialize a serialized round.

        Args:
            serialized_round (Dict): Serialization of an instance of a round.
            matchs (List[Match]): List of all the instances of matches.

        Returns:
            T: Instance of Round.
        """
        matchs_in_round_ids = serialized_round["matchs_in_round_ids"]
        matchs_in_round = []
        # Build the list of Matches instances from the ids stored in matchs_in_round_ids
        # and the list of all the matches instances
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


if __name__ == "__main__":
    player1 = Player("Inès-Corinne", "Voisin", "03/19/85", "M")
    player2 = Player("Léon", "Aubry", "02/04/00", "F")
    player3 = Player("Michelle ", "Hardy", "09/10/98", "F")
    player4 = Player("Denise Martineau", "Renault", "02/26/90", "M")
    match1 = Match(player1, player2)
    match1.results_match(1)
    match2 = Match(player1, player2)
    match2.results_match(3)
    round = Round("Round test")
    round.add_match(match1)
    round.add_match(match2)
    print(round)
