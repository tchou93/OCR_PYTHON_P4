from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match

class Tournament:
    """Tournament."""

    def __init__(self, name, place, date, time_control, description):
        """Has a presentation for the tournament."""
        self.name = name
        self.place = place
        self.date = date
        self.tours_number = 4
        self.tours: List[Tour] = []
        self.players: List[Player] = []
        self.time_control = time_control
        self.description = description 

        
    def __str__(self):
        """Used in print."""
        description_tournament = f"Nom du tournoi : {self.name}, Lieu : {self.place}, contrôle de temps : {self.time_control}, Description : {self.description} \n"
        description_tournament += f"\tVoici les joueurs du tournoi:\n"

        num_player=1
        for player in self.players:
            # description_tournament += f"\tjoueur {num_player} :\n" 
            description_tournament += "\t"+str(player)
            num_player += 1 

        description_tournament += f"\t\tVoici les Tours :\n"

        for tour in self.tours:
            description_tournament += "\t\t"+tour.name+": "+str(tour)

        for player in self.players:
            description_tournament += "\t\t"+ player.first_name + " : " + str(player.score) + "\n"
        description_tournament +="\n"

        return description_tournament

    def add_player(self, player):
        self.players.append(player)

    def players_ranks_sort(self, list_of_players:List[Player]):
        list_of_players_sort = []
        dic_ranks_players = {}
        list_of_ranks = []
        for player in list_of_players:
            dic_ranks_players[player.ranking] = player
            list_of_ranks.append(player.ranking)
        list_of_ranks.sort(reverse=True)
        for rank_sort in list_of_ranks:    
            list_of_players_sort.append(dic_ranks_players[rank_sort])
        return list_of_players_sort

    def dict_of_score_player(self, list_of_players:List[Player]):
        dict_of_score = {}
        for player in list_of_players:
            if player.score in dict_of_score:
                list_of_player_same_score = dict_of_score[player.score]
                list_of_player_same_score.append(player)
                dict_of_score[player.score] = list_of_player_same_score
            else:
                dict_of_score[player.score] = [player]
        return dict_of_score

    def players_scores_sort(self, list_of_players:List[Player]):
        list_of_players_sort = []
        list_of_scores = []
        dict_of_score = self.dict_of_score_player(list_of_players)
        index = 0
        for player in list_of_players:
            list_of_scores.append(player.score)
        list_of_scores.sort()
        while index < len(list_of_scores):
            count_score = list_of_scores.count(list_of_scores[index])
            # print(index)
            if count_score > 1:
                for player in self.players_ranks_sort(dict_of_score[list_of_scores[index]]):
                    list_of_players_sort.append(player)
                index += count_score
            else:
                list_of_players_sort.append((dict_of_score[list_of_scores[index]][0]))
                index += 1

        return list_of_players_sort

    def add_tour(self):
        list_of_players_sort : List[Player] = []
        tour = Tour(f"Round {len(self.tours)+1}")
        number_of_players_in_tour = len(self.players)
        index = 0 
        if (len(self.tours) == 0):
            list_of_players_sort = self.players_ranks_sort(self.players)
            while index < (number_of_players_in_tour/2):
                tour.add_match(Match(list_of_players_sort[index],list_of_players_sort[index+int(number_of_players_in_tour/2)]))
                index += 1
        else:
            list_of_players_sort = self.players_scores_sort(self.players)
            while index < number_of_players_in_tour:
                tour.add_match(Match(list_of_players_sort[index],list_of_players_sort[index+1]))
                index +=2 
        self.tours.append(tour)
 