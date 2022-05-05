"""Base view."""
from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
from models.tournament import Tournament
import os
import time

class View:
    """Chess game view."""
    def display_menu_generic(self, menu_title, menu_options):
        while 1:
            os.system("cls") 
            index = 1
            print(f"|{menu_title}|")
            for menu_option in menu_options:
              print(f"{index} - {menu_option}")
              index += 1
            user_input = input(">> ")
            if self.prompt_correct_int(user_input):
                if (int(user_input)) not in range(1,index):
                    print("Erreur lors de la saisie, recommencez...")
                    time.sleep(1)
                else:
                    return int(user_input)

    def prompt_correct_int(self, item):
        try:
            nombre = int(item)
            return True
        except ValueError:
            print("Erreur lors de la saisie, recommencez...")
            time.sleep(1)
            return False

    def prompt_generic(self, prompt_title, items):
        os.system("cls")
        print(f"|{prompt_title}|")
        list_input = []
        for item in items:
            list_input.append(input(item))
        return list_input

    def display_menu_main(self): 
        menu_main = [
            "Tournoi",
            "Sauvegarder les données",
            "Charger les données",
            "Rapports",
            "Simulation de tournoi",
            "Quitter",
        ]
        return self.display_menu_generic("Menu principal",menu_main)

    def display_menu_tournament(self):
        menu_tournament = [
            "Créer un tournoi",
            "Continuer un tournoi",
            "Retour au menu principal"
        ]
        return self.display_menu_generic("Tournoi",menu_tournament)

    def prompt_for_create_tournament(self):
        items=[
            "Nom du tournoi : ",
            "Lieu : ",
            "Date (JJ/MM/AA) : ",
            "Contrôle du temps (Bullet/Blitz/Rapid) : ",
            "Description : ",
            "Nombre de joueur : "
        ]
        return self.prompt_generic("Créer un tournoi",items)

    def prompt_for_add_players(self, number_of_player):
        items=[
            "Prénom : ",
            "Nom : ",
            "Date de naissance (JJ/MM/AA) : ",
            "Sexe (M/F) : "
        ]
        list_info_players = []
        for index in range(int(number_of_player)):
            list_info_players.append(self.prompt_generic(f"Ajouter le Joueur {index+1}:",items))
        return list_info_players

    def prompt_for_continue(self):
        input("Appuyer sur une touche pour continuer...")

    def display_menu_choose_tournament(self, tournaments_in_progress: List[Tournament]):
        items = []
        for tournament_in_progress in tournaments_in_progress:
            items.append(f"{tournament_in_progress.name} (Round {len(tournament_in_progress.tours)}/{tournament_in_progress.tours_number})")
        items.append("Retour au menu tournoi")
        return (self.display_menu_generic("Choisir un tournoi",items))

    def display_menu_tournament_continue(self):
        menu_create_tournament = [
            "Jouer un round",
            "Modifier le classement d’un joueur",
            "Retour au menu des tournois"
        ]
        return self.display_menu_generic("Commencer un tournoi",menu_create_tournament)

    def display_menu_reports(self):
        menu_reports = [
            "Rapport détaillé sur un tournoi",
            "Liste des tournois",
            "Retour au menu principal"
        ]
        return self.display_menu_generic("Rapports",menu_reports)

    def display_menu_tournament_reports(self):
        menu_tournament_reports = [
            "Joueurs du tournoi",
            "Liste des tours du tournoi",
            "Liste des matchs du tournoi",
            "Retour au menu des rapports"
        ]
        return self.display_menu_generic("Rapport détaillé sur un tournoi",menu_tournament_reports)




    # def prompt_for_create_tournament(self):
        # print(list_input_infos_tournament)
        # tournament = Tournament(list_input_infos_tournament[0],list_input_infos_tournament[1],list_input_infos_tournament[2],list_input_infos_tournament[3],list_input_infos_tournament[4])
        # self.tournaments.append(tournament)
        # print("Le tournoi a été crée : ")
        # if user_input not in menu_option[0:len(menu_option-1)][0]:
        #     self.menu_creation_error(menu_title, menu_option)
        #     print(f"Le choix rentré n'existe pas, veuillez recommencer: ")

    # def menu_creation_error(self, menu_title, menu_option: List[(string,string)]):
    #     os.system("cls") 
    #     print(f"|{menu_title}|")
    #     for (index_menu,menu) in menu_option:
    #       print(f"{index_menu} - {menu}")
    #     user_input = input(">> ")
    #     if user_input not in menu_option[0:len(menu_option-1)][0]:

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

