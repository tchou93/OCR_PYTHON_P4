from typing import List
from tinydb import TinyDB
from models.player import Player
from models.round import Round
from models.match import Match
from models.tournament import Tournament


class Database_tournament:

    db = TinyDB("db_chess_tournament.json")

    @classmethod
    def serialized_items(cls, items):
        serialized = []
        for item in items:
            serialized.append(item.serialized())
        return serialized

    @classmethod
    def deserialized_players(cls, serialized_players):
        players = []
        for serialized_player in serialized_players:
            players.append(Player.deserialized(serialized_player))
        return players

    @classmethod
    def deserialized_matchs(cls, serialized_matchs, players: List[Player]):
        matchs = []
        for serialized_match in serialized_matchs:
            matchs.append(Match.deserialized(serialized_match, players))
        return matchs

    @classmethod
    def deserialized_tours(cls, serialized_tours, matchs: List[Match]):
        rounds = []
        for serialized_tour in serialized_tours:
            rounds.append(Round.deserialized(serialized_tour, matchs))
        return rounds

    @classmethod
    def deserialized_tournaments(
        cls, serialized_tournaments, rounds: List[Round], players: List[Player]
    ):
        tournaments = []
        for serialized_tournament in serialized_tournaments:
            tournaments.append(
                Tournament.deserialized(serialized_tournament, rounds, players)
            )
        return tournaments

    @classmethod
    def option_save_serialized_table_to_db(cls, serialized_items, table_name):
        cls.save_serialized_in_db(serialized_items, table_name)

    @classmethod
    def save_serialized_in_db(cls, serialized_items, table_name):
        table_items = cls.db.table(table_name)
        table_items.insert_multiple(serialized_items)

    @classmethod
    def clear_all_tab_in_db(cls):
        cls.db.drop_tables()

    @classmethod
    def load_serialized_from_db(cls, table_name):
        load_table = cls.db.table(table_name)
        return load_table.all()

    @classmethod
    def option_load_from_db(cls):
        try:
            players = cls.deserialized_players(cls.load_serialized_from_db("player"))
            matchs = cls.deserialized_matchs(
                cls.load_serialized_from_db("match"), players
            )
            rounds = cls.deserialized_tours(
                cls.load_serialized_from_db("round"), matchs
            )
            tournaments = cls.deserialized_tournaments(
                cls.load_serialized_from_db("tournament"), rounds, players
            )
            # cls.view.prompt_for_continue()
            # cls.view.display_load_from_database_done()
            return tournaments
        except IndexError:
            # cls.view.display_load_from_database_error()
            return None

    @classmethod
    def option_save_all_serialized_table_to_db(cls, tournaments: List[Tournament]):
        cls.option_save_serialized_table_to_db(
            cls.serialized_items(tournaments), "tournament"
        )
        for tournament in tournaments:
            cls.option_save_serialized_table_to_db(
                cls.serialized_items(tournament.rounds), "round"
            )
            cls.option_save_serialized_table_to_db(
                cls.serialized_items(tournament.players), "player"
            )
            for round in tournament.rounds:
                cls.option_save_serialized_table_to_db(
                    cls.serialized_items(round.matchs), "match"
                )
        # cls.view.display_save_to_database_done()
