"""Define the main controller."""
from typing import List
from models.player import Player
from models.tour import Tour
from models.tournament import Tournament
import random

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

    def create_tournament_simu(self):
        self.tournament = Tournament("Tournoi1","Sevran","28/04/2022","control1","description 1")
        player1 = Player("Tan", "TRAN", "03/10/1985", "M")
        player2 = Player("Tan1", "TRAN1", "04/10/1985", "A")
        player3 = Player("Tan2", "TRAN2", "05/10/1985", "B")
        player4 = Player("Tan3", "TRAN3", "06/10/1985", "C")
        player5 = Player("Tan4", "TRAN4", "07/10/1985", "D")
        player6 = Player("Tan5", "TRAN5", "08/10/1985", "E")
        player7 = Player("Tan6", "TRAN6", "09/10/1985", "F")
        player8 = Player("Tan7", "TRAN7", "10/10/1985", "G")
        self.tournament.add_player(player1)
        self.tournament.add_player(player4)
        self.tournament.add_player(player8)
        self.tournament.add_player(player2)
        self.tournament.add_player(player3)
        self.tournament.add_player(player5)
        self.tournament.add_player(player6)
        self.tournament.add_player(player7)

    def run(self):
        #Test for tournament without View
        self.create_tournament_simu()


        #Set some random ranks
        for player in self.tournament.players:
            player.set_ranking(random.randint(1,10000))

        #Create all the tours and simulate the winners of each match]
        for number_of_tour in range(3):
            self.tournament.add_tour()
            for match in self.tournament.tours[len(self.tournament.tours)-1].matchs:
                match.results_match(random.randint(0,2))
            print(self.tournament)

        self.view.show_list_of_players_by_ranks(self.tournament.players)
        self.view.show_list_of_players_by_alphabetical_order(self.tournament.players)
        self.view.show_info_tournament(self.tournament)
        # self.view.show_info_tournament(self.tournament.tours)
        # self.view.show_info_tournament(self.tournament.