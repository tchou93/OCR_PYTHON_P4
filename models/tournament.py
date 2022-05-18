import time
import locale
from uuid import uuid4
from typing import List
from models.player import Player
from models.round import Round
from models.match import Match


class Tournament:
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
        locale.setlocale(locale.LC_ALL, "fr_FR")

    def __repr__(self):
        """Utiliser pour avoir une représentation avec la fontion print"""
        description_tournament = (
            f"Nom du tournoi : {self.name}, Lieu : {self.place}, Date: {self.date_begin}"
            " - {self.date_end}, contrôle de temps : {self.time_control}, Description : {self.description} \n"
        )
        return description_tournament

    def add_player(self, player):
        """Ajoute le joueur player au tournoi"""
        self.players.append(player)

    def get_first_tour(self, round_name):
        round = Round(round_name)
        list_of_players_sort_by_ranks = sorted(self.players, key=lambda p: p.ranking)
        size = int(len(list_of_players_sort_by_ranks) / 2)
        matchs_players = list(
            zip(
                list_of_players_sort_by_ranks[:size],
                list_of_players_sort_by_ranks[size:],
            )
        )
        for (player1, player2) in matchs_players:
            player1.add_already_played_index(self.players.index(player2))
            player2.add_already_played_index(self.players.index(player1))
            round.add_match(Match(player1, player2))
        return round

    def get_next_tour(self, round_name):
        round = Round(round_name)
        list_of_players_sort_by_ranks = sorted(self.players, key=lambda p: p.ranking)
        list_of_players_sort_by_scores_ranks = sorted(
            list_of_players_sort_by_ranks, key=lambda p: p.score, reverse=True
        )
        while len(list_of_players_sort_by_scores_ranks) != 0:
            index = 1
            list_of_players_already_played_with_player_1 = []
            for player_already_played_index in list_of_players_sort_by_scores_ranks[
                0
            ].players_already_played_index:
                list_of_players_already_played_with_player_1.append(
                    self.players[player_already_played_index]
                )

            while (
                list_of_players_sort_by_scores_ranks[index]
                in list_of_players_already_played_with_player_1
            ):
                if index == (len(list_of_players_sort_by_scores_ranks) - 1):
                    # Si il reste deux joueurs alors on force le jeu même si ils ont déjà joué ensemble
                    break
                # Le joueur en tête de liste va jouer avec le prochain jamais joué.
                index += 1
            player1 = list_of_players_sort_by_scores_ranks[0]
            player2 = list_of_players_sort_by_scores_ranks[index]
            match = Match(player1, player2)
            player1.add_already_played_index(self.players.index(player2))
            player2.add_already_played_index(self.players.index(player1))
            round.add_match(match)
            # On retire de la liste temporaire les joueurs déjà en match
            list_of_players_sort_by_scores_ranks.remove(player1)
            list_of_players_sort_by_scores_ranks.remove(player2)
        return round

    def add_round(self):
        """Ajoute un round au tournoi"""
        round_name = f"Round {len(self.rounds)+1}"
        if len(self.rounds) == 0:
            self.rounds.append(self.get_first_tour(round_name))
        else:
            self.rounds.append(self.get_next_tour(round_name))

    def set_date_begin(self):
        """Modifier la date et l'heure du début de tournoi"""
        self.date_begin = time.strftime("%A %d %B %Y")

    def set_date_end(self):
        """Modifier la date et l'heure de fin du tournoi"""
        self.date_end = time.strftime("%A %d %B %Y")

    def serialized(self):
        rounds_in_tournament_id = []
        players_in_tournament_ids = []
        for tour in self.rounds:
            rounds_in_tournament_id.append(tour.id)
        for player in self.players:
            players_in_tournament_ids.append(player.id)

        serialized_tournament = {
            "name": self.name,
            "place": self.place,
            "time_control": self.time_control,
            "description": self.description,
            "rounds_number": self.rounds_number,
            "rounds_in_tournament_id": rounds_in_tournament_id,
            "date_begin": self.date_begin,
            "date_end": self.date_end,
            "players_in_tournament_ids": players_in_tournament_ids,
            "finish": self.finish,
            "id": self.id,
        }
        return serialized_tournament

    @classmethod
    def deserialized(
        cls, serialized_tournament, rounds: List[Round], players: List[Player]
    ):
        rounds_in_tournament_ids = serialized_tournament["rounds_in_tournament_id"]
        players_in_tournament_ids = serialized_tournament["players_in_tournament_ids"]
        rounds_in_tournament = []
        players_in_tournament = []

        for rounds_in_tournament_id in rounds_in_tournament_ids:
            for round in rounds:
                if rounds_in_tournament_id == round.id:
                    rounds_in_tournament.append(round)
                    break

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
        )
