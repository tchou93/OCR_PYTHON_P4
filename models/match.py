from typing import List, Dict
from uuid import uuid4
from .player import Player


class Match:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        resultplayer1="-",
        resultplayer2="-",
        finish=False,
        id=None,
    ):
        self.player1 = player1
        self.player2 = player2
        self.resultplayer1 = resultplayer1
        self.resultplayer2 = resultplayer2
        self.finish = finish
        self.id = str(uuid4()) if id is None else id

    def __repr__(self):
        """Used for print."""
        return (
            f"[{self.player1.first_name} {self.player1.last_name},{self.resultplayer1}]"
            ",[{self.player2.first_name} {self.player2.last_name},{self.resultplayer2}]"
        )

    def get_match(self):
        return ([self.player1, self.resultplayer1], [self.player2, self.resultplayer2])

    def results_match(self, result: int) -> None:
        """
        Selon le résultat du match rentré en paramètre, la fonction met à jour le score
        de chaque joueur et rempli leurs champs de résultat.
        """
        if result == 1:
            self.player1.win()
            self.player2.lost()
            self.resultplayer1 = "Win"
            self.resultplayer2 = "Lost"
        elif result == 2:
            self.player1.lost()
            self.player2.win()
            self.resultplayer1 = "Lost"
            self.resultplayer2 = "Win"
        elif result == 3:
            self.player1.draw()
            self.player2.draw()
            self.resultplayer1 = "Draw"
            self.resultplayer2 = "Draw"
        self.finish = True

    def serialized(self) -> Dict:
        serialized_match = {
            "player1_id": self.player1.id,
            "player2_id": self.player2.id,
            "resultplayer1": self.resultplayer1,
            "resultplayer2": self.resultplayer2,
            "finish": self.finish,
            "id": self.id,
        }
        return serialized_match

    @classmethod
    def deserialized(cls, serialized_match: Dict, players: List[Player]):
        for player in players:
            if player.id == serialized_match["player1_id"]:
                player1 = player
            elif player.id == serialized_match["player2_id"]:
                player2 = player
        resultplayer1 = serialized_match["resultplayer1"]
        resultplayer2 = serialized_match["resultplayer2"]
        finish = serialized_match["finish"]
        id = serialized_match["id"]
        return cls(player1, player2, resultplayer1, resultplayer2, finish, id)
