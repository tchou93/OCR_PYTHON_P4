from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match

class Tournament:
    """Tournament."""

    # def __init__(self, name: str, place: str, date, time_control, description, tour_number=4, tours: List[Tour]=None, players=None):
    #     """Has a presentation for the tournament."""
    #     self.name = name
    #     self.place = place
    #     self.date = date
    #     self.tours_number = tour_number
    #     self.tours = [] if tours is None else tours
    #     self.players: List[Player] = [] if players is None else players
    #     self.time_control = time_control
    #     self.description = description

    def __init__(self, name: str, place: str, date, time_control, description, tour_number=4, tours: List[Tour]=None, players=None):
        """Has a presentation for the tournament."""
        self.name = name
        self.place = place
        self.date = date
        self.tours_number = 4
        self.tours: List[Tour] = []
        self.players: List[Player] = []
        self.time_control = time_control
        self.description = description


    # def __repr__(self):
    #     return self.name
    #     """Used in print."""
    #     description_tournament = f"Nom du tournoi : {self.name}, Lieu : {self.place}, contrôle de temps : {self.time_control}, Description : {self.description} \n"
    #     description_tournament += f"\tVoici les joueurs du tournoi:\n"
    #     num_player=1
    #     for player in self.players:
    #         # description_tournament += f"\tjoueur {num_player} :\n"
    #         description_tournament += "\t"+str(player)
    #         num_player += 1

    #     description_tournament += f"\t\tVoici les Tours :\n"

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

        for player in self.players:
            players_name_already_tmp = []
            for players_name_already_played in player.players_name_already_played:
                players_name_already_tmp.append(players_name_already_played.first_name)
            description_tournament += "\t\t"+  player.first_name + " a déjà joué avec : "+ str(players_name_already_tmp) + "\n"
        description_tournament +="\n"

        return description_tournament

    def add_player(self, player):
        self.players.append(player)


    def players_ranks_sort(self, list_of_players:List[Player]) -> List[Player]:
        """Retourne la liste des joueurs triée en fonction de ranking"""
        return sorted(list_of_players, key=lambda p: p.ranking)
       

    def players_scores_sort(self, list_of_players:List[Player]) -> List[Player]:
        """triez tous les joueurs en fonction de leur nombre total de points """
        list_of_players_rank_sort = self.players_ranks_sort(list_of_players)
        return sorted(list_of_players_rank_sort, key=lambda p: p.score,reverse=True)

    # def layers_scores_sort_part2(list_of_scores_sort:List[Player]):
    #     """Si le joueur 1 a déjà joué contre le joueur 2, associez-le plutôt au joueur 3."""
    #     pass

    # def get_first_tour(self):
    #     list_of_players_sort = self.players_ranks_sort(self.players)
    #     size = len(list_of_players_sort)/2
    #     matchs = zip(list_of_players_sort[:size], list_of_players_sort[size:])
    #     while index < (number_of_players_in_tour/2):
    #         tour.add_match(Match(list_of_players_sort[index],list_of_players_sort[index+int(number_of_players_in_tour/2)]))
    #         index += 1
    #     return tour

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
            # tour = self.get_first_tour()
        else:
            list_of_players_sort = self.players_scores_sort(self.players)
            while len(list_of_players_sort) != 0:
                index = 1
                while list_of_players_sort[index] in list_of_players_sort[0].players_name_already_played :
                    print(f"{list_of_players_sort[0].first_name} a déjà joué avec {list_of_players_sort[index].first_name}")
                    if (index == (len(list_of_players_sort)-1)):
                        print("break")
                        break
                    index += 1
                tour.add_match(Match(list_of_players_sort[0],list_of_players_sort[index]))
                player1 = list_of_players_sort[0]
                player2 = list_of_players_sort[index]
                list_of_players_sort.remove(player1)
                list_of_players_sort.remove(player2)
        self.tours.append(tour)
