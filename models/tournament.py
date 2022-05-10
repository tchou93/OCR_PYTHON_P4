from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
import random
import time
from uuid import uuid4

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

    # def find_index_player(sel, player:Player, players:List[Player]):
    #     for i in range(len(players)):
    #         if player == players[i]:
    #             return i

    def add_tour(self):
        """Ajoute un tour au tournoi"""
        list_of_players_sort : List[Player] = []
        tour: Tour = Tour(f"Round {len(self.tours)+1}")
        number_of_players_in_tour = len(self.players)
        index = 0
        if (len(self.tours) == 0):
            list_of_players_sort = self.players_ranks_sort(self.players)
            while index < (number_of_players_in_tour/2):
                player1 = list_of_players_sort[index]
                player2 = list_of_players_sort[index+int(number_of_players_in_tour/2)]  
                match = Match(player1,player2)
                player1.add_already_played(self.players.index(player2))
                player2.add_already_played(self.players.index(player1))
                tour.add_match(match)
                index += 1
            self.tours.append(tour)
            return tour
        elif (self.finish == False) and (self.tours[len(self.tours)-1].finish == True):
            list_of_players_sort = self.players_scores_sort(self.players)
            while len(list_of_players_sort) != 0:
                index = 1
                players_already_played = []
                for i in list_of_players_sort[0].players_already_played:
                    players_already_played.append(self.players[i])
                while list_of_players_sort[index] in list_of_players_sort[0].players_already_played :
                    if (index == (len(list_of_players_sort)-1)):
                        break
                    index += 1
                player1 = list_of_players_sort[0]
                player2 = list_of_players_sort[index]
                match = Match(player1,player2)
                player1.add_already_played(self.players.index(player2))
                player2.add_already_played(self.players.index(player1))
                tour.add_match(match)
                list_of_players_sort.remove(player1)
                list_of_players_sort.remove(player2)
            self.tours.append(tour)
            return tour
        else:
            return self.tours[len(self.tours)-1]
            # if(len(self.tours) == self.tours_number):
            #     self.finished = True

    def set_date_begin(self):
        """Modifier la date et l'heure du début de tournoi"""
        self.date_end = time.strftime("%A %d %B %Y")

    def set_date_end(self):
        """Modifier la date et l'heure de fin du tournoi"""
        self.date_end = time.strftime("%A %d %B %Y")


        # self.name = name
        # self.place = place
        # self.time_control = time_control
        # self.description = description
        # self.tours_number = tours_number
        # self.tours = [] if tours is None else tours
        # self.date_begin = date_begin
        # self.date_end = date_end
        # self.players: List[Player] = [] if players is None else players
        # self.finish:bool = finish

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