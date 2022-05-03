"""Base view."""
from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
from models.tournament import Tournament

class View:
    """Chess game view."""
    
    # def show_list_of_players_by_ranks(self,players:List[Player]):
    #     list_of_players_sort_ranks_higher = sorted(players, key=lambda p: p.ranking)
    #     display_players_ranks = "Voici les joueurs du tournoi trié par classement : \n"
    #     for player_sort_ranks_higher in list_of_players_sort_ranks_higher:
    #         display_players_ranks += f"Joueur : {player_sort_ranks_higher.first_name}, Classement : {player_sort_ranks_higher.ranking} \n"
    #     print(display_players_ranks)

    # def show_list_of_players_by_alphabetical_order(sel,players:List[Player]):
    #     list_of_players_sort_alpha = sorted(players, key=lambda p: p.first_name)
    #     display_players_alpha = "Voici les joueurs du tournoi trié par ordre alphabétique : \n"
    #     for player_sort_alpha in list_of_players_sort_alpha:
    #         display_players_alpha += f"Joueur : {player_sort_alpha.first_name} \n"
    #     print(display_players_alpha)

    # def show_info_tournament(self,tournament:Tournament):
    #     print("Voici la liste des tournois :")
    #     print(f"Nom du tournoi : {tournament.name}, Lieu : {tournament.place}, contrôle de temps : {tournament.time_control}, Description : {tournament.description} \n")

    # def show_info_tours(self,tours:List[Tour]):
    #     display_info_tours = "Voici la liste des tours :\n"
    #     for tour in tours:
    #         display_info_tours += tour.name + " "
    #     display_info_tours += "\n"
    #     print(display_info_tours)
        
    # def show_info_matchs(self,tours:List[Tour]):
    #     display_info_matchs = "Voici les matchs du tournois : \n"
    #     for tour in tours:
    #         matchs = tour.matchs
    #         for match in matchs:
    #             if (match.resultplayer1 == "Win"):
    #                 display_info_matchs += f"[{match.player1.first_name} VS {match.player2.first_name} = {match.player1.first_name} Win] \n"
    #             elif (match.resultplayer1 == "Lost"):
    #                 display_info_matchs += f"[{match.player1.first_name} VS {match.player2.first_name} = {match.player2.first_name} Win] \n"
    #             else:
    #                 display_info_matchs += f"[{match.player1.first_name} VS {match.player2.first_name} = Draw] \n"
    #     print(display_info_matchs)

