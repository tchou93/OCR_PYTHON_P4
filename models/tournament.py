from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
import random
import time

class Tournament:
    """Tournament."""

    def __init__(self, name: str, place: str, time_control: str, description: str, tour_number=4, tours: List[Tour]=None, players=None):
        """Constructeur de la classe Tournament"""
        self.name = name
        self.place = place
        self.date_begin = time.strftime("%A %d %B %Y")
        self.date_end = "-"
        self.tours_number = tour_number
        self.tours = [] if tours is None else tours
        self.players: List[Player] = [] if players is None else players
        self.time_control = time_control
        self.description = description
        self.finish:bool = False

    def __repr__(self):
        """Utiliser pour avoir une représentation avec la fontion print"""
        description_tournament = f"Nom du tournoi : {self.name}, Lieu : {self.place}, Date: {self.date}, contrôle de temps : {self.time_control}, Description : {self.description} \n"
        return description_tournament

    def add_player(self, player):
        """Ajoute le joueur player au tournoi"""
        self.players.append(player)

    def players_ranks_sort(self, list_of_players:List[Player]) -> List[Player]:
        """Retourne la liste des joueurs triée en fonction de ranking"""
        return sorted(list_of_players, key=lambda p: p.ranking)
       
    def players_scores_sort(self, list_of_players:List[Player]) -> List[Player]:
        """Trie tous les joueurs en fonction de leur nombre total de points """
        list_of_players_rank_sort = self.players_ranks_sort(list_of_players)
        return sorted(list_of_players_rank_sort, key=lambda p: p.score,reverse=True)

    # def get_first_tour(self):
    #     list_of_players_sort = self.players_ranks_sort(self.players)
    #     size = len(list_of_players_sort)/2
    #     matchs = zip(list_of_players_sort[:size], list_of_players_sort[size:])
    #     while index < (number_of_players_in_tour/2):
    #         tour.add_match(Match(list_of_players_sort[index],list_of_players_sort[index+int(number_of_players_in_tour/2)]))
    #         index += 1
    #     return tour

    def add_tour(self):
        """Ajoute un tour au tournoi"""
        list_of_players_sort : List[Player] = []
        tour: Tour = Tour(f"Round {len(self.tours)+1}")
        number_of_players_in_tour = len(self.players)
        index = 0
        if (len(self.tours) == 0):
            list_of_players_sort = self.players_ranks_sort(self.players)
            while index < (number_of_players_in_tour/2):
                match = Match(list_of_players_sort[index],list_of_players_sort[index+int(number_of_players_in_tour/2)])
                tour.add_match(match)
                index += 1
            self.tours.append(tour)
            return tour
        elif (self.finish == False) and (self.tours[len(self.tours)-1].finish == True):
            list_of_players_sort = self.players_scores_sort(self.players)
            while len(list_of_players_sort) != 0:
                index = 1
                while list_of_players_sort[index] in list_of_players_sort[0].players_already_played :
                    if (index == (len(list_of_players_sort)-1)):
                        break
                    index += 1
                match = Match(list_of_players_sort[0],list_of_players_sort[index])
                tour.add_match(match)
                player1 = list_of_players_sort[0]
                player2 = list_of_players_sort[index]
                list_of_players_sort.remove(player1)
                list_of_players_sort.remove(player2)
            self.tours.append(tour)
            return tour
        else:
            return self.tours[len(self.tours)-1]
            # if(len(self.tours) == self.tours_number):
            #     self.finished = True

    def set_date_end(self):
        """Modifier l'heure de fin du tournoi"""
        self.date_end = time.strftime("%A %d %B %Y")