"""Base view."""
from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
from models.tournament import Tournament
from tabulate import tabulate
import os
import time

class View:
    """Chess game view."""
    #####################
    # Generic functions
    #####################
    def display_menu_generic(self, menu_title, menu_options):
        while 1:
            self.terminal_clear()
            index = 1
            list_option_str = []
            print(f"|{menu_title}|")
            for menu_option in menu_options:
                list_option_str.append(str(index))
                print(f"{index} - {menu_option}")
                index += 1
            user_input = input(">> ")
            if user_input in list_option_str:
                return int(user_input)
            else:
                print("Erreur lors de la saisie, recommencez...")
                time.sleep(1)

    def prompt_generic(self, prompt_title, items):
        self.terminal_clear()
        print(f"|{prompt_title}|")
        list_input = []
        for item in items:
            list_input.append(input(item))
        return list_input

    ################################
    # Function for display the menu
    ################################
    def display_menu_main(self): 
        menu_main = [
            "Tournoi",
            "Sauvegarder les données",
            "Charger les données",
            "Rapports",
            "[TEST]",
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

    def display_menu_choose_tournament(self, tournaments_in_progress: List[Tournament]):
        items = []
        for tournament_in_progress in tournaments_in_progress:
            items.append(f"{tournament_in_progress.name} (Round {len(tournament_in_progress.tours)}/{tournament_in_progress.tours_number})")
        items.append("Retour au menu tournoi")
        return (self.display_menu_generic("Choisir un tournoi",items))

    def display_menu_tournament_action(self,tournament: Tournament):
        menu_create_tournament = [
            "Ajouter un round",
            "Jouer un match",
            "Modifier le classement d’un joueur",
            "Retour au menu des tournois"
        ]
        header_menu_tournament_action = self.display_all_information_tournament(tournament)
        return self.display_menu_generic(header_menu_tournament_action,menu_create_tournament)

    # def display_menu_add_score(self,tour:Tour):
    #     list_scores = []
    #     for match in tour.matchs:
    #         items=[
    #             f"{match.player1.first_name} {match.player1.last_name} a gagné",
    #             f"{match.player2.first_name} {match.player2.last_name} a gagné",
    #             "Egalité",
    #         ]
    #         list_scores.append(self.display_menu_generic(f"Résultat du match {match.player1.first_name} {match.player1.last_name} vs {match.player2.first_name} {match.player2.last_name}:",items))
    #     return list(map(int, list_scores))

    def display_menu_add_score(self,match:Match):
        items=[
            f"{match.player1.first_name} {match.player1.last_name} a gagné",
            f"{match.player2.first_name} {match.player2.last_name} a gagné",
            "Egalité",
        ]
        return self.display_menu_generic(f"Résultat du match {match.player1.first_name} {match.player1.last_name} vs {match.player2.first_name} {match.player2.last_name}:",items)

    # def prompt_for_add_score(self, tour:Tour):
    #     for match in tour.matchs:
    #         items=[
    #             f"{match.player1} a gagné",
    #             f"{match.player2} a gagné",
    #             "Egalité",
    #         ]
    #     list_scores = []
    #     for index in range(len(tour.matchs)):
    #         list_scores.append(self.display_menu_generic(f"Résultat du match {match.player1} vs {match.player2}:",items))
    #     return list_info_players

    def display_menu_modify_player_rank(self, tournament: Tournament):
        players:List[Player] = tournament.players
        menu_players_ranks = []
        for player in players:
            menu_players_ranks.append(f"{player.first_name} {player.last_name} (Classement: {player.ranking})")
        menu_players_ranks.append("Quitter")
        user_input_option = self.display_menu_generic("Modification du classement",menu_players_ranks)
        if user_input_option != len(players) + 1:
            user_input_rank = input(f"Entrer le nouveau classement pour le joueur {players[user_input_option-1].first_name} {players[user_input_option-1].last_name}: ")
            return (user_input_option,int(user_input_rank))
        else:
            return (user_input_option,-1)
 

    ################################
    # Function for display message
    ################################
    def display_tournament_done(self):
        self.terminal_clear()
        print("Le tournoi est terminé, l'ajout de tour n'est plus possible !")

    def display_tour_done(self):
        self.terminal_clear()
        print("Le tour est terminé, plus de match à jouer")

    def display_tour_not_done(self):
        self.terminal_clear()
        print("Le tour n'est pas encore terminé")

    def display_save_in_database_done(self):
        self.terminal_clear()
        print("La sauvegarde dans la base de donnée a été effectué dans le fichier db_chess_tournament.json")

    def display_load_in_database_done(self):
        self.terminal_clear()
        print("Le chargement de la base de donnée a été effectué à partir du fichier db_chess_tournament.json ")

    #####################
    # Function for prompt
    #####################

    def prompt_for_add_players(self, number_of_player):
        items=[
            "Prénom : ",
            "Nom : ",
            "Date de naissance (JJ/MM/AA) : ",
            "Sexe (M/F) : ",
            "Classement : "
        ]
        list_info_players = []
        for index in range(number_of_player):
            list_info_players.append(self.prompt_generic(f"Ajouter le Joueur {index+1}:",items))
        return list_info_players

    def prompt_for_create_tournament(self):
        items=[
            "Nom du tournoi : ",
            "Lieu : ",
            "Contrôle du temps (Bullet/Blitz/Rapid) : ",
            "Description : ",
            "Nombre de joueur : "
        ]
        return self.prompt_generic("Créer un tournoi",items)    

    def prompt_for_continue(self):
        input("Appuyer sur une touche pour continuer...") 

        
    #############################
    # Function for display Object
    #############################

    def display_all_information_tournament(self, tournament:Tournament):
        display_tournament = self.display_tournament(tournament)
        display_tour = self.display_tour(tournament)
        display_player_rank_score = self.display_player_rank_score(tournament)
        return display_tournament + display_tour + display_player_rank_score

    def display_tour(self, tournament:Tournament):
        tours : List[Tour] = tournament.tours
        table = []
        table_header = ['Tour','Début','Fin','Match','Statut']
        table.append(table_header)
        for tour in tours:
            matchs_display = ""
            for match in tour.matchs:
                matchs_display += f"{match.player1.first_name} {match.player1.last_name} ({match.resultplayer1}) vs {match.player2.first_name} {match.player2.last_name} ({match.resultplayer2}) \n"
            if(tour.finish == True):
                status_tour= "Terminé"
            else:
                status_tour= "En cours"
            table_body =[tour.name,tour.start_time,tour.end_time,matchs_display,status_tour]
            table.append(table_body)
        print(tabulate(table,headers="firstrow",tablefmt="grid"))
        return str(tabulate(table,headers="firstrow",tablefmt="grid")+"\n")

    def display_player_rank_score(self, tournament:Tournament):
        players_sorted_rank = sorted(tournament.players, key=lambda p: p.ranking)
        players_sorted_rank_score = sorted(players_sorted_rank, key=lambda p: p.score,reverse=True)
        table = []
        table_header = ['Joueur','Classement', 'Score']
        table.append(table_header)
        for player in players_sorted_rank_score:
            table_body = [f"{player.first_name} {player.last_name}", player.ranking, player.score]
            table.append(table_body)
        print(tabulate(table,headers="firstrow",tablefmt="grid"))
        return str(tabulate(table,headers="firstrow",tablefmt="grid"))

    def display_tournament(self, tournament:Tournament):
        print(f"Nom du tournoi : {tournament.name} | Lieu : {tournament.place} | Date début: {tournament.date_begin} | Date fin: {tournament.date_end}")
        print(f"contrôle de temps : {tournament.time_control} | Description : {tournament.description} | Round {len(tournament.tours)}/{tournament.tours_number}")
        return f"Nom du tournoi : {tournament.name} | Lieu : {tournament.place} | Date début: {tournament.date_begin} | Date fin: {tournament.date_end}\n" + f"contrôle de temps : {tournament.time_control} | Description : {tournament.description} | Round {len(tournament.tours)}/{tournament.tours_number}\n"

    #############################
    # Function diverse
    #############################
    def terminal_clear(self):
        os.system("cls")