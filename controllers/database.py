from os import getcwd
from sys import path

try:
    path.insert(1, getcwd())
except IndexError:
    pass

from ast import Dict
from typing import List, Tuple
from tinydb import TinyDB
from models.player import Player
from models.round import Round
from models.match import Match
from models.tournament import Tournament


class Database_tournament:
    """Database to save and load all the objects."""

    db = TinyDB("db_chess_tournament.json")

    @classmethod
    def serialized_items(cls, items: List) -> List[Dict]:
        """Serialize a list of items(Tournament, Round, Player).

        Args:
            items (List): List of items(Tournament, Round, Player).

        Returns:
            List[Dict]: List of Dict which represent the serialization
            of the items.
        """
        serialized = []
        for item in items:
            serialized.append(item.serialized())
        return serialized

    @classmethod
    def deserialized_players(cls, serialized_players: List[Dict]) -> List[Player]:
        """Deserialize a list of serialized player.

        Args:
            serialized_players (List[Dict]): List of serialized player.

        Returns:
            List[Player]: List of Player instance.
        """
        players = []
        for serialized_player in serialized_players:
            players.append(Player.deserialized(serialized_player))
        return players

    @classmethod
    def deserialized_matchs(
        cls, serialized_matchs: List[Dict], players: List[Player]
    ) -> List[Match]:
        """Deserialize a list of serialized match.

        Args:
            serialized_matchs (List[Dict]):  List of serialized match.
            players (List[Player]): List of Player instance.

        Returns:
            List[Match]: List of Match instance.
        """
        matchs = []
        for serialized_match in serialized_matchs:
            matchs.append(Match.deserialized(serialized_match, players))
        return matchs

    @classmethod
    def deserialized_tours(
        cls, serialized_tours: List[Dict], matchs: List[Match]
    ) -> List[Round]:
        """Deserialize a list of serialized tour.

        Args:
            serialized_tours (List[Dict]): List of serialized tour.
            matchs (List[Match]): List of match instance.

        Returns:
            List[Round]: List of round instance.
        """
        rounds = []
        for serialized_tour in serialized_tours:
            rounds.append(Round.deserialized(serialized_tour, matchs))
        return rounds

    @classmethod
    def deserialized_tournaments(
        cls,
        serialized_tournaments: List[Dict],
        rounds: List[Round],
        players: List[Player],
    ) -> List[Tournament]:
        """Deserialize a list of serialized tournament.

        Args:
            serialized_tournaments (List[Dict]): List of serialized tournament.
            rounds (List[Round]): List of round instance.
            players (List[Player]): List of player instance.

        Returns:
            List[Tournament]: List of player tournament.
        """
        tournaments = []
        for serialized_tournament in serialized_tournaments:
            tournaments.append(
                Tournament.deserialized(serialized_tournament, rounds, players)
            )
        return tournaments

    @classmethod
    def option_save_serialized_table_to_db(
        cls, serialized_items: List, table_name: str
    ):
        """Save serialized items to the database (<table_name> table).

        Args:
            serialized_items (List): List of items(Tournament, Round, Player) serialized.
            table_name (str): Name of the table.
        """
        table_items = cls.db.table(table_name)
        table_items.insert_multiple(serialized_items)

    @classmethod
    def load_serialized_from_db(cls, table_name: str) -> List[Dict]:
        """Load serialized items from the database (<table_name> table).

        Args:
            table_name (str): Name of the table.

        Returns:
            List[Dict]: List of serialized item (Tournament, Player, Round)
        """

        load_table = cls.db.table(table_name)
        return load_table.all()

    @classmethod
    def option_load_from_db(cls) -> Tuple[List[Tournament], List[Player]]:
        """Deserialized all the table from the database to create the
        tournaments.

        Returns:
            Tuple[List[Tournament], List[Player]]: Tuple with a list of tournaments,
            and list of actors build by the database.
        """

        actors = cls.deserialized_players(cls.load_serialized_from_db("player"))
        matchs = cls.deserialized_matchs(cls.load_serialized_from_db("match"), actors)
        rounds = cls.deserialized_tours(cls.load_serialized_from_db("round"), matchs)
        tournaments = cls.deserialized_tournaments(
            cls.load_serialized_from_db("tournament"), rounds, actors
        )
        if not tournaments:
            return (None, None)
        else:
            return (tournaments, actors)

    @classmethod
    def option_save_all_serialized_table_to_db(
        cls, tournaments: List[Tournament], actors: List[Player]
    ):
        """Save all the table to the database from the instances of tournament.

        Args:
            tournaments (List[Tournament]): List of tournament instance  .
        """
        if not tournaments:
            return False
        else:
            cls.db.drop_tables()
            cls.option_save_serialized_table_to_db(
                cls.serialized_items(tournaments), "tournament"
            )
            for tournament in tournaments:
                cls.option_save_serialized_table_to_db(
                    cls.serialized_items(tournament.rounds), "round"
                )

                for round in tournament.rounds:
                    cls.option_save_serialized_table_to_db(
                        cls.serialized_items(round.matchs), "match"
                    )
            cls.option_save_serialized_table_to_db(
                cls.serialized_items(actors), "player"
            )
            return True


if __name__ == "__main__":
    print("test")
