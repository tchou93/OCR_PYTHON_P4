"""Base view."""
from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
from models.tournament import Tournament

class View:
    """Chess game view."""

    def show_list_of_players_by_ranks(self,players:List[Player]):
        list_of_players_sort_ranks_higher = sorted(players, key=lambda p: p.ranking)
        print("Voici les joueurs du tournoi trié par classement :")
        for player_sort_ranks_higher in list_of_players_sort_ranks_higher:
            print(f"Joueur : {player_sort_ranks_higher.first_name}, Classement : {player_sort_ranks_higher.ranking}")
 
    def show_list_of_players_by_alphabetical_order(sel,players:List[Player]):
        list_of_players_sort_alpha = sorted(players, key=lambda p: p.first_name)
        print("Voici les joueurs du tournoi trié par ordre alphabétique :")
        for player_sort_alpha in list_of_players_sort_alpha:
            print(f"Joueur : {player_sort_alpha.first_name}")

    def show_info_tournament(self,tournament:Tournament):
        print("Voici la liste des tournois :")
        print(f"Nom du tournoi : {tournament.name}, Lieu : {tournament.place}, contrôle de temps : {tournament.time_control}, Description : {tournament.description} \n")

    def show_info_tours(self,tours:List[Tour]):
        print("Voici la liste des tours:")
        for tour in self.tours:
            description_tournament += "\t\t"+tour.name

    def show_info_matchs(self,tours:List[Tour]):
        matchs_of_tournament = "Voici les matchs du tournois : \n"
        for tour in tours:
            matchs = tour.matchs
            for match in matchs:
                if (match.resultplayer1 == "Win"):
                    matchs_of_tournament += f"[{match.player1.first_name} VS {match.player2.first_name} = {match.player1.first_name} Win] \n"
                elif (match.resultplayer1 == "Lost"):
                    matchs_of_tournament += f"[{match.player1.first_name} VS {match.player2.first_name} = {match.player2.first_name} Win] \n"
                else:
                    matchs_of_tournament += f"[{match.player1.first_name} VS {match.player2.first_name} = Draw] \n"
        print(matchs_of_tournament)
        # print("Voici la liste des matchs :")
        # for match in matchs:
        #     if (match.resultplayer1 == "Win"):
        #         return f"[{match.player1.first_name} VS {match.player2.first_name} = {match.player1.first_name} Win]"
        #     elif (match.resultplayer1 == "Lost"):
        #         return f"[{match.player1.first_name} VS {match.player2.first_name} = {match.player2.first_name} Win]"
        #     else:
        #         return f"[{match.player1.first_name} VS {match.player2.first_name} = Draw]"


    # def show_list_of_all_tours(sel,players:List[Player]):

    # def prompt_for_player(self, number):
    #     """Prompt for a name."""
    #     info_player = {}
    #     print(f"Taper les informations pour le joueur {number} : ")
    #     info_player["fist_name"] = input("tapez le fist_name : ")
    #     info_player["last_name"] = input("tapez le last_name : ")
    #     info_player["birthday"] = input("tapez le birthday : ")
    #     info_player["gender"] = input("tapez le gender : ")
    #     return info_player

    # def prompt_for_tournament(self):
    #     """Prompt for a tournament."""
    #     info_tournament = {}
    #     print(f"Taper les informations pour le tournoi: ")
    #     info_tournament["name"] = input("tapez le name : ")
    #     info_tournament["place"] = input("tapez la place : ")
    #     info_tournament["date"] = input("tapez la date: ")
    #     info_tournament["time_control"] = input("tapez le time_control: ")
    #     info_tournament["description"] = input("tapez la description: ")
    #     return info_tournament 

    # def prompt_for_result_match(self, player1, player2):
    #     print(f"Entrer le résultat du match entre le joueur {player1} et le joueur {player2}  ")
    #     result = input(f"Le joueur {player1} ")




    # def show_games(self):
    #     pass

    # def show_reports(self):
    #     pass

    # def prompt_for_data_save(self):
    #     pass

    # def prompt_for_data_load(self):
    #     pass
