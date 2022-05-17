from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
import time
from uuid import uuid4
import locale

class Tournament:
    """Tournament."""

    def __init__(self, name: str, place: str, time_control: str, description: str, tours_number=4, tours: List[Tour]=None, date_begin="-", date_end ="-", players=None, finish = False, id=None):
        """Constructeur de la classe Tournament"""
        self.name = name
        self.place = place
        self.time_control = time_control
        self.description = description
        self.tours_number = tours_number
        self.tours = [] if tours is None else tours
        self.date_begin = date_begin
        self.date_end = date_end
        self.players: List[Player] = [] if players is None else players
        self.finish:bool = finish
        self.id = str(uuid4()) if id is None else id
        locale.setlocale(locale.LC_ALL, 'fr_FR') 

    def __repr__(self):
        """Utiliser pour avoir une représentation avec la fontion print"""
        description_tournament = f"Nom du tournoi : {self.name}, Lieu : {self.place}, Date: {self.date}, contrôle de temps : {self.time_control}, Description : {self.description} \n"
        return description_tournament

    def add_player(self, player):
        """Ajoute le joueur player au tournoi"""
        self.players.append(player)

    def get_first_tour(self, tour_name):
        tour = Tour(tour_name)
        list_of_players_sort_by_ranks = sorted(self.players, key=lambda p: p.ranking)
        size = int(len(list_of_players_sort_by_ranks)/2)
        matchs_players = list(zip(list_of_players_sort_by_ranks[:size], list_of_players_sort_by_ranks[size:]))
        for (player1, player2) in matchs_players:
            player1.add_already_played_index(self.players.index(player2))
            player2.add_already_played_index(self.players.index(player1))
            tour.add_match(Match(player1,player2))
        return tour

    def get_next_tour(self, tour_name):
        tour = Tour(tour_name)
        list_of_players_sort_by_ranks = sorted(self.players, key=lambda p: p.ranking)
        list_of_players_sort_by_scores_ranks = sorted(list_of_players_sort_by_ranks, key=lambda p: p.score,reverse=True)
        while len(list_of_players_sort_by_scores_ranks) != 0:
            index = 1
            list_of_players_already_played_with_player_1 = []
            for player_already_played_index in list_of_players_sort_by_scores_ranks[0].players_already_played_index:
                list_of_players_already_played_with_player_1.append(self.players[player_already_played_index])
            
            while list_of_players_sort_by_scores_ranks[index] in list_of_players_already_played_with_player_1 :    
                if (index == (len(list_of_players_sort_by_scores_ranks)-1)):
                    # Si il reste deux joueurs alors on force le jeu même si ils ont déjà joué ensemble
                    break
                # Le joueur en tête de liste va jouer avec le prochain jamais joué.
                index += 1
            player1 = list_of_players_sort_by_scores_ranks[0]
            player2 = list_of_players_sort_by_scores_ranks[index]
            match = Match(player1,player2)
            player1.add_already_played_index(self.players.index(player2))
            player2.add_already_played_index(self.players.index(player1))
            tour.add_match(match)
            # On retire de la liste temporaire les joueurs déjà en match
            list_of_players_sort_by_scores_ranks.remove(player1)
            list_of_players_sort_by_scores_ranks.remove(player2)
        return tour

    def add_tour(self):
        """Ajoute un tour au tournoi"""
        list_of_players_sort : List[Player] = []
        tour_name = f"Round {len(self.tours)+1}"
        index = 0
        if (len(self.tours) == 0):
            self.tours.append(self.get_first_tour(tour_name))
        else:
            self.tours.append(self.get_next_tour(tour_name))

    def set_date_begin(self):
        """Modifier la date et l'heure du début de tournoi"""
        self.date_begin = time.strftime("%A %d %B %Y")

    def set_date_end(self):
        """Modifier la date et l'heure de fin du tournoi"""
        self.date_end = time.strftime("%A %d %B %Y")

    def serialized(self):
        tours_in_tournament_ids = []
        players_in_tournament_ids = []
        for tour in self.tours:
            tours_in_tournament_ids.append(tour.id)
        for player in self.players:
            players_in_tournament_ids.append(player.id)

        serialized_tournament = {
            'name' : self.name,
            'place' : self.place,
            'time_control' : self.time_control,
            'description' : self.description,
            'tours_number' : self.tours_number, 
            'tours_in_tournament_ids' : tours_in_tournament_ids,
            'date_begin' : self.date_begin, 
            'date_end' : self.date_end, 
            'players_in_tournament_ids' : players_in_tournament_ids,
            'finish' :  self.finish,
            'id': self.id 
        }
        return serialized_tournament

    def deserialized(serialized_tournament, tours: List[Tour], players: List[Player] ):
        tours_in_tournament_ids = serialized_tournament['tours_in_tournament_ids']
        players_in_tournament_ids = serialized_tournament['players_in_tournament_ids']
        tours_in_tournament = []
        players_in_tournament = []

        for tours_in_tournament_id in tours_in_tournament_ids:
            for tour in tours:
                if (tours_in_tournament_id == tour.id):
                    tours_in_tournament.append(tour)
                    break

        for players_in_tournament_id in players_in_tournament_ids:
            for player in players:
                if (players_in_tournament_id == player.id):
                    players_in_tournament.append(player)
                    break
 
        name = serialized_tournament['name']
        place = serialized_tournament['place']
        time_control = serialized_tournament['time_control']
        description = serialized_tournament['description']
        tours_number = serialized_tournament['tours_number']
        tours_in_tournament = tours_in_tournament
        date_begin = serialized_tournament['date_begin']
        date_end = serialized_tournament['date_end']
        players_in_tournament = players_in_tournament
        finish = serialized_tournament['finish']
        id = serialized_tournament['id']
        return Tournament(
            name,
            place, 
            time_control, 
            description, 
            tours_number, 
            tours_in_tournament,
            date_begin,
            date_end,
            players_in_tournament,
            finish,
            id
            )