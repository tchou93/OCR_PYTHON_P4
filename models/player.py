from typing import List, Dict, Type, TypeVar
from uuid import uuid4

T = TypeVar("T", bound="Player")


class Player:
    """Class to represent a player in a tournament
    Instance attributes:
        first_name: str
        last_name: str
        birthday: str
        gender: str
        ranking: int
        score: int
        players_already_played_index: List[Int]
        id: str
    Instance methods:
        win(self)
        lost(self)
        draw(self)
        add_already_played_index(self, index_player: int)
        serialized(self)
    Class method:
        deserialized(cls: Type[T], serialized_player) -> T
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthday: str,
        gender: str,
        ranking=0,
        score=0,
        players_already_played_index=None,
        id=None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.ranking = ranking
        self.score = score
        self.players_already_played_index: List[int] = (
            [] if players_already_played_index is None else players_already_played_index
        )
        self.id = str(uuid4()) if id is None else id

    def __repr__(self):
        """Used for print."""
        return (
            f"Nom : {self.first_name}, Prénom : {self.last_name}, Date de naissance : {self.birthday}"
            ", Genre : {self.gender}, Classement : {self.ranking} \n"
        )

    def win(self):
        """Add 1 in the intance attribut <score> if the player wins."""
        self.score += 1

    def lost(self):
        """Add 0 in the intance attribut <score> if the player loses."""
        self.score += 0

    def draw(self):
        """Add 0.5 in the intance attribut <score> if there is a draw."""
        self.score += 0.5

    def add_already_played_index(self, index_player: int):
        """Add the index of the instance of Player who has already been played."""
        self.players_already_played_index.append(index_player)

    def serialized(self) -> Dict:
        """Serialize an instance of a player.

        Returns:
            Dict: Serialization of an instance of a player.
        """
        serialized_player = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "gender": self.gender,
            "ranking": self.ranking,
            "score": self.score,
            "players_already_played_index": self.players_already_played_index,
            "id": self.id,
        }
        return serialized_player

    @classmethod
    def deserialized(cls: Type[T], serialized_player) -> T:
        """Deserialize a serialized player.

        Args:
            serialized_player (Dict): Serialization of an instance of a player.

        Returns:
            T: Instance of Player.
        """
        first_name = serialized_player["first_name"]
        last_name = serialized_player["last_name"]
        birthday = serialized_player["birthday"]
        gender = serialized_player["gender"]
        ranking = serialized_player["ranking"]
        score = serialized_player["score"]
        players_already_played_index = serialized_player["players_already_played_index"]
        id = serialized_player["id"]
        return cls(
            first_name,
            last_name,
            birthday,
            gender,
            ranking,
            score,
            players_already_played_index,
            id,
        )
