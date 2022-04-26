"""Define the main controller."""
from typing import List
from models.player import Player
from models.tour import Tour

class Controller:
    """Main controller."""

    def __init__(self,view):
        self.players: List[Player] = []
        self.tours: List[Tour] = []
        self.view  = view
        self.tournament = None

    def add_players(self,number_of_players):
        while len(self.players) <= number_of_players:
            info_player= self.view.prompt_for_player()
            # if not info_player:
            #     return
            player = Player(info_player["fist_name"], info_player["last_name"], info_player["birthday"], info_player["gender"])
            self.players.append(player)

    # def add_tours(self,number_of_players):
    #     player_in_tour = number_of_players
    #     index_tour = 1
    #     while player_in_tour > 1:
    #         tour = Tour(f"Round {index_tour}")
    #         tour.add_match()

    #         player_in_tour /= 2
    #         index_tour += 1

    def run(self):
        pass


    # def show_ranking(self):
    # def show_games(self):
    # def show_reports(self):
    # def prompt_for_data_save(self):
    # def prompt_for_data_load(self):