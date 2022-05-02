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
        self.tournaments:List[Tournament] = []

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
        tournament = Tournament("Tournoi1","Sevran","28/04/2022","control1","description 1")
        player1 = Player("Tan", "TRAN", "03/10/1985", "M")
        player2 = Player("Tan1", "TRAN1", "04/10/1985", "A")
        player3 = Player("Tan2", "TRAN2", "05/10/1985", "B")
        player4 = Player("Tan3", "TRAN3", "06/10/1985", "C")
        player5 = Player("Tan4", "TRAN4", "07/10/1985", "D")
        player6 = Player("Tan5", "TRAN5", "08/10/1985", "E")
        player7 = Player("Tan6", "TRAN6", "09/10/1985", "F")
        player8 = Player("Tan7", "TRAN7", "10/10/1985", "G")
        tournament.add_player(player1)
        tournament.add_player(player4)
        tournament.add_player(player8)
        tournament.add_player(player2)
        tournament.add_player(player3)
        tournament.add_player(player5)
        tournament.add_player(player6)
        tournament.add_player(player7)
        self.tournaments.append(tournament)

    def tournament_simu(self):
        #Test for tournament without View
        self.create_tournament_simu()
        tournament1 = self.tournaments[0]

        #Set some random ranks
        for player in tournament1.players:
            player.set_ranking(random.randint(1,10000))

        #Create all the tours and simulate the winners of each match]
        print(f"Bienvenue sur le tournoi {tournament1.name} :")
        for number_of_tour in range(4):
            print(f"Le Round {number_of_tour+1} commence :")
            tournament1.add_tour()
            for match in tournament1.tours[len(tournament1.tours)-1].matchs:
                match.results_match(random.randint(0,2))
            print(tournament1)
            print(f"Le Round {number_of_tour+1} est terminé :")  
            print(f"[1] Mettre à jour les classements")
            print(f"[2] Continuer avec le prochain Round")
            user_input = input()
            if int(user_input) == 1:
                while 1:
                    index = 1
                    for player in tournament1.players:
                        print(f"{index} : {player.first_name} {player.last_name} Classement: {player.ranking}")
                        index += 1
                    print("100 : Quittez")
                    user_input_name_player = input("Choisir le joueur ou quitter: ")
                    if(int(user_input_name_player) == 100):
                        break
                    user_input_rank_player = input("Choisir le nouveau rang: ")
                    tournament1.players[int(user_input_name_player)-1].ranking = int(user_input_rank_player)
                print(f"Mise à jour terminé")
            elif int(user_input) == 2:
                continue
        print(f"Merci le tournoi est terminé")

    def menu(self):
        choix_min = 1
        choix_max = 4
        while 1:
           print("-----------------------------------------------------------------")
           print("Bienvenue dans le gestionnaire de tournoi :")
           print(f"{choix_min}: Simulation d'un tournoi avec deux tours ")
           print(f"{choix_min+1}: TBD ")
           print(f"{choix_min+2}: TBD")
           print(f"{choix_max}: Quittez.")
           print("------------------------------------------------------------------")
           choix = input("Veuillez choisir l'option voulu: ")
           choix = int(choix)
           if choix == (choix_max):
                break
           elif choix < choix_min or choix > choix_max:
                print("Le choix ne correspond à aucun choix, recommencez! ")
           elif choix==1:
                print("-------------------------------------------------------------")
                print("Simulation d'un tournoi avec deux tours")
                print("-------------------------------------------------------------")    
                self.tournament_simu()
           elif choix==2:
                pass
                # print("-----------------------------------------------------")
                # print("Liste de tous les joueurs d'un tournoi par classement")
                # print("-----------------------------------------------------")
                # self.view.show_list_of_players_by_ranks(self.tournaments[0].players)
           elif choix==3:
                pass
                # print("---------------------------------------")
                # print("Simulation d'un tournoi avec deux tours")
                # print("---------------------------------------")
                # self.tournament_simu()
    

        # self.view.show_list_of_players_by_ranks(tournament1.players)
        # self.view.show_list_of_players_by_alphabetical_order(tournament1.players)
        # self.view.show_info_tournament(tournament1)
        # self.view.show_info_tours(tournament1.tours)
        # self.view.show_info_matchs(tournament1.tours)
        # self.view.show_info_tournament(self.tournament.