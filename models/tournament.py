from os import getcwd
from sys import path

try:
    path.insert(1, getcwd())
except IndexError:
    pass

import time
import locale
from uuid import uuid4
from typing import List, Dict, Tuple, Type, TypeVar
from models.player import Player
from models.round import Round
from models.match import Match

T = TypeVar("T", bound="Tournament")


class Tournament:
    """Class to represent a tournament"""

    def __init__(
        self,
        name: str,
        place: str,
        time_control: str,
        description: str,
        rounds_number=4,
        rounds: List[Round] = None,
        date_begin="-",
        date_end="-",
        players=None,
        finish=False,
        id=None,
        save_datas_players=None,
    ):
        self.name = name
        self.place = place
        self.time_control = time_control
        self.description = description
        self.rounds_number = rounds_number
        self.rounds = [] if rounds is None else rounds
        self.date_begin = date_begin
        self.date_end = date_end
        self.players: List[Player] = [] if players is None else players
        self.finish: bool = finish
        self.id = str(uuid4()) if id is None else id
        # This variable is used to save datas (score and list of players
        # alreay played) when a tournament is finished from players
        self.save_datas_players: List[Tuple[float, List[int]]] = (
            [] if save_datas_players is None else save_datas_players
        )
        locale.setlocale(locale.LC_ALL, "fr_FR")

    def __repr__(self):
        """Used for print."""
        description_tournament = (
            f"Nom du tournoi : {self.name}, Lieu : {self.place}, Date: {self.date_begin}"
            f" - {self.date_end}, contrôle de temps : {self.time_control}, Description : {self.description} \n"
        )
        return description_tournament

    def add_player(self, player):
        """Add a player to the instance attribut <players>."""
        self.players.append(player)

    def get_first_round(self, round_name: str) -> Round:
        """Build the first round (swiss system)

        Args:
            round_name (str): Name of the round.

        Returns:
            Round: Instance of the first round.
        """
        round = Round(round_name)
        list_of_players_sort_by_ranks = sorted(self.players, key=lambda p: p.ranking)
        size = int(len(list_of_players_sort_by_ranks) / 2)
        matchs_players = list(
            zip(
                list_of_players_sort_by_ranks[:size],
                list_of_players_sort_by_ranks[size:],
            )
        )
        # Best players of the first part of the players sort by ranks with the best
        # players of the second part.
        for (player1, player2) in matchs_players:
            player1.add_already_played_index(self.players.index(player2))
            player2.add_already_played_index(self.players.index(player1))
            round.add_match(Match(player1, player2))
        return round

    def get_next_round(self, round_name: str) -> Round:
        """Build the next round (swiss system)

        Args:
            round_name (str): Name of the round.

        Returns:
            Round: Instance of the next round.
        """
        round = Round(round_name)
        # Sort the player by score and rank
        list_of_players_sort_by_ranks = sorted(self.players, key=lambda p: p.ranking)
        list_of_players_sort_by_scores_ranks = sorted(
            list_of_players_sort_by_ranks, key=lambda p: p.score, reverse=True
        )
        while len(list_of_players_sort_by_scores_ranks) != 0:
            index = 1
            list_of_players_already_played_with_player_1 = []

            # Build an instance list of players already played with player 1 with
            # a list of index.
            for player_already_played_index in list_of_players_sort_by_scores_ranks[
                0
            ].players_already_played_index:
                list_of_players_already_played_with_player_1.append(
                    self.players[player_already_played_index]
                )

            # Associate the player 1 of the sort list with the player 2 if there is
            # already no match between us, else Associate the player 3 ect ...
            while (
                list_of_players_sort_by_scores_ranks[index]
                in list_of_players_already_played_with_player_1
            ):
                if index == (len(list_of_players_sort_by_scores_ranks) - 1):
                    # If there is only left 2 players to play, then we force the game
                    # even if they have already played together
                    break
                index += 1
            # Determine the player1 and player2 for the match and create it
            player1 = list_of_players_sort_by_scores_ranks[0]
            player2 = list_of_players_sort_by_scores_ranks[index]
            # Add the index in the instance attribut <players_already_played_index>
            # for player 1 and player 2
            player1.add_already_played_index(self.players.index(player2))
            player2.add_already_played_index(self.players.index(player1))
            # Add the match in the current round
            match = Match(player1, player2)
            round.add_match(match)
            # Remove player1 and player2 from the tempory list (sort by score and rank)
            list_of_players_sort_by_scores_ranks.remove(player1)
            list_of_players_sort_by_scores_ranks.remove(player2)
        return round

    def add_round(self):
        """Use the sub-functions get_first_round and get_next_round
        to add a round"""
        round_name = f"Round {len(self.rounds)+1}"
        if len(self.rounds) == 0:
            self.rounds.append(self.get_first_round(round_name))
        else:
            self.rounds.append(self.get_next_round(round_name))

    def set_date_begin(self):
        """Set the instance attribut <date_begin> at the beggining of the Round."""
        self.date_begin = time.strftime("%A %d %B %Y")

    def set_date_end(self):
        """Set the instance attribut <date_end> at the end of the Round."""
        self.date_end = time.strftime("%A %d %B %Y")

    def serialized(self) -> Dict:
        """Serialize an instance of a tournament.

        Returns:
            Dict: Serialization of an instance of a tournament.
        """
        rounds_in_tournament_ids = []
        players_in_tournament_ids = []
        for tour in self.rounds:
            rounds_in_tournament_ids.append(tour.id)
        for player in self.players:
            players_in_tournament_ids.append(player.id)

        serialized_tournament = {
            "name": self.name,
            "place": self.place,
            "time_control": self.time_control,
            "description": self.description,
            "rounds_number": self.rounds_number,
            "rounds_in_tournament_ids": rounds_in_tournament_ids,
            "date_begin": self.date_begin,
            "date_end": self.date_end,
            "players_in_tournament_ids": players_in_tournament_ids,
            "finish": self.finish,
            "id": self.id,
            "save_datas_players": self.save_datas_players,
        }
        return serialized_tournament

    @classmethod
    def deserialized(
        cls: Type[T],
        serialized_tournament: Dict,
        rounds: List[Round],
        players: List[Player],
    ) -> T:
        """Deserialize a serialized tournament.

        Args:
            serialized_tournament (Dict): Serialization of an instance of a tournament.
            rounds (List[Round]): List of all the instances of rounds.
            players (List[Player]): List of all the instances of players.

        Returns:
            T: Instance of Tournament.
        """
        rounds_in_tournament_ids = serialized_tournament["rounds_in_tournament_ids"]
        players_in_tournament_ids = serialized_tournament["players_in_tournament_ids"]
        rounds_in_tournament = []
        players_in_tournament = []

        # Build the list of rounds instances from the ids stored in rounds_in_tournament_ids
        # and the list of all the rounds instances
        for rounds_in_tournament_id in rounds_in_tournament_ids:
            for round in rounds:
                if rounds_in_tournament_id == round.id:
                    rounds_in_tournament.append(round)
                    break

        # Build the list of players instances from the ids stored in players_in_tournament_ids
        # and the list of all the players instances
        for players_in_tournament_id in players_in_tournament_ids:
            for player in players:
                if players_in_tournament_id == player.id:
                    players_in_tournament.append(player)
                    break

        name = serialized_tournament["name"]
        place = serialized_tournament["place"]
        time_control = serialized_tournament["time_control"]
        description = serialized_tournament["description"]
        rounds_number = serialized_tournament["rounds_number"]
        rounds_in_tournament = rounds_in_tournament
        date_begin = serialized_tournament["date_begin"]
        date_end = serialized_tournament["date_end"]
        players_in_tournament = players_in_tournament
        finish = serialized_tournament["finish"]
        id = serialized_tournament["id"]
        save_datas_players = serialized_tournament["save_datas_players"]
        return cls(
            name,
            place,
            time_control,
            description,
            rounds_number,
            rounds_in_tournament,
            date_begin,
            date_end,
            players_in_tournament,
            finish,
            id,
            save_datas_players,
        )


if __name__ == "__main__":
    new_tournament = Tournament(
        "Tournoi Random1", "Paris", "Bullet", "Description du tounoi Random1"
    )
    new_tournament.set_date_begin()
    new_tournament.set_date_end()
    print(new_tournament)
