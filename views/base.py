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
        display_players_ranks = "Voici les joueurs du tournoi trié par classement : \n"
        for player_sort_ranks_higher in list_of_players_sort_ranks_higher:
            display_players_ranks += f"Joueur : {player_sort_ranks_higher.first_name}, Classement : {player_sort_ranks_higher.ranking} \n"
        print(display_players_ranks)

    def show_list_of_players_by_alphabetical_order(sel,players:List[Player]):
        list_of_players_sort_alpha = sorted(players, key=lambda p: p.first_name)
        display_players_alpha = "Voici les joueurs du tournoi trié par ordre alphabétique : \n"
        for player_sort_alpha in list_of_players_sort_alpha:
            display_players_alpha += f"Joueur : {player_sort_alpha.first_name} \n"
        print(display_players_alpha)

    def show_info_tournament(self,tournament:Tournament):
        print("Voici la liste des tournois :")
        print(f"Nom du tournoi : {tournament.name}, Lieu : {tournament.place}, contrôle de temps : {tournament.time_control}, Description : {tournament.description} \n")

    def show_info_tours(self,tours:List[Tour]):
        display_info_tours = "Voici la liste des tours :\n"
        for tour in tours:
            display_info_tours += tour.name + " "
        display_info_tours += "\n"
        print(display_info_tours)
        
    def show_info_matchs(self,tours:List[Tour]):
        display_info_matchs = "Voici les matchs du tournois : \n"
        for tour in tours:
            matchs = tour.matchs
            for match in matchs:
                if (match.resultplayer1 == "Win"):
                    display_info_matchs += f"[{match.player1.first_name} VS {match.player2.first_name} = {match.player1.first_name} Win] \n"
                elif (match.resultplayer1 == "Lost"):
                    display_info_matchs += f"[{match.player1.first_name} VS {match.player2.first_name} = {match.player2.first_name} Win] \n"
                else:
                    display_info_matchs += f"[{match.player1.first_name} VS {match.player2.first_name} = Draw] \n"
        print(display_info_matchs)


    # def show_menu(self,tours:List[Tour]):
    #     while 1:
    #        print("-----------------------------------------------------------------")
    #        print("Bienvenue dans le gestionnaire de tournoi")
    #        print("1: TBD ")
    #        print("2: TBD ")
    #        print("3: Simulation d'un tournoi avec deux tours")
    #        print("4: Quittez.")
    #        print("------------------------------------------------------------------")
    #        choix = input("Veuillez choisir l'option voulu ")
    #        choix = int(choix)
    #        if choix==4:
    #            break
    #        elif choix<1 or choix>4:
    #            print("Le choix ne correspond à aucun choix, recommencez! ")
    #        elif choix==1:
    #            print("--------------------------")
    #            print("!!! pas encore gérer !!!")
    #            print("--------------------------")
    #        elif choix==2:
    #            print("--------------------------")
    #            print("!!! pas encore gérer !!!")
    #            print("--------------------------")
    #        elif choix==3:
    #            print("---------------------------------------")
    #            print("Simulation d'un tournoi avec deux tours")
    #            print("---------------------------------------")
            #    book_url = input("Veuillez indiquer l'url exacte du livre à extraire: ")



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
