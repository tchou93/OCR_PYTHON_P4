from typing import List, Dict, Type, TypeVar
from uuid import uuid4
from .player import Player

T = TypeVar("T", bound="Match")


class Match:
    """Class to represent a match in a tournament
    Instance attributes:
        player1: Player
        player2: Player
        resultplayer1: str
        resultplayer2: str
        finish: boolean
        id: str
    Instance methods:
        results_match(self, result: int)
        serialized(self) -> Dict
    Class method:
        deserialized(cls: Type[T], serialized_match: Dict, players: List[Player]) -> T
    """

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

    def results_match(self, result: int):
        """Take the result of the match with the parameter <result>
        then call the function win/lost of the players
        finally set the instance attribute <resultplayer>.

        Args:
            result (int): 1 => player1 win, 2 => player2 win, 3 => draw.
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
        """Serialize an instance of a match.

        Returns:
            Dict: Serialization of an instance of a match.
        """
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
    def deserialized(cls: Type[T], serialized_match: Dict, players: List[Player]) -> T:
        """Deserialize a serialized match.

        Args:
            serialized_match (Dict): Serialization of an instance of a match.
            players (List[Player]): List of all the instances of players.

        Returns:
            T: Instance of Match.
        """
        # Find the player1 and player2 instances from the ids stored in player1_id and player2_id
        # and the list of all the players instances
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
