"""Define the main controller."""
from typing import List
from models.player import Player
from models.tour import Tour
from models.tournament import Tournament

class Controller:
    """Main controller."""

    def __init__(self,view):
        self.view  = view
        self.tournament = None

    def create_tournament(self):
        info_tournament = self.view.prompt_for_tournament()
        self.tournament = Tournament(info_tournament["name"],info_tournament["place"],info_tournament["date"],info_tournament["time_control"],info_tournament["description"])

    def add_players(self,number_of_players):
        for i in range(number_of_players):
            info_player = self.view.prompt_for_player(i+1)
            # if not info_player:/
            #     return
            player = Player(info_player["fist_name"], info_player["last_name"], info_player["birthday"], info_player["gender"])
            self.tournament.add_player(player)
        print(self.tournament)
        # for player in self.players:
        #     print(player)

    # def add_result_tour(self,number_of_players):
    #     result_tour = self.view.prompt_for_result_tour



    def run(self):
        self.create_tournament()
        self.add_players(2)
        self.tournament.add_tour()


    # def show_ranking(self):
    # def show_games(self):
    # def show_reports(self):
    # def prompt_for_data_save(self):
    # def prompt_for_data_load(self):