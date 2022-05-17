"""Base view."""
from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
from models.tournament import Tournament
from tabulate import tabulate
from datetime import datetime
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
            "Ajouter le tournoi random1",
            "Ajouter le tournoi random2",
            "Continuer un tournoi",
            "Retour au menu principal"
        ]
        return self.display_menu_generic("Tournoi",menu_tournament)

    def display_menu_reports(self):
        menu_reports = [
            "Rapport détaillé sur un tournoi",
            "Liste des tournois",
            "Liste des acteurs",
            "Retour au menu principal"
        ]
        return self.display_menu_generic("Rapports",menu_reports)

    def display_menu_tournament_reports(self,tournament_name : str):
        menu_tournament_reports = [
            "Récapitulatif de tout le tournoi",
            "Joueurs du tournoi",
            "Liste des tours du tournoi",
            "Liste des matchs du tournoi",
            "Retour au menu choisir un tournoi"
        ]
        return self.display_menu_generic(f"Rapport détaillé sur le tournoi \"{tournament_name}\":",menu_tournament_reports)

    def display_menu_players_in_tournament_reports(self,tournament_name : str):
        menu_tournament_reports = [
            "Liste de tous les joueurs par ordre alphabétique",
            "Liste de tous les joueurs par classement",
            f"Retour au menu des rapports détaillés du tournoi \"{tournament_name}\""
        ]
        return self.display_menu_generic(f"Rapport joueurs du tournoi \"{tournament_name}\":",menu_tournament_reports)

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
            "Retour au menu tournoi"
        ]
        header_menu_tournament_action = self.get_all_information_tournament(tournament)
        return self.display_menu_generic(header_menu_tournament_action,menu_create_tournament)

    def display_menu_add_score(self,match:Match):
        items=[
            f"{match.player1.first_name} {match.player1.last_name} a gagné",
            f"{match.player2.first_name} {match.player2.last_name} a gagné",
            "Egalité",
        ]
        return self.display_menu_generic(f"Résultat du match {match.player1.first_name} {match.player1.last_name} vs {match.player2.first_name} {match.player2.last_name}:",items)

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
 
    def display_menu_report_choose_tournament(self, tounaments: List[Tournament]):
        items = []
        for tournament in tounaments:
            items.append(f"{tournament.name} (Round {len(tournament.tours)}/{tournament.tours_number})")
        items.append("Retour au menu rapport")
        return (self.display_menu_generic("Choisir un tournoi",items))


    ################################
    # Function for display message
    ################################
    def display_message(self, message:str):
        self.terminal_clear()
        print(message)
        self.prompt_for_continue()

    def display_input_error(self):
        message = "Erreur dans une des saisies, veuillez recommencer"
        self.display_message(message)

    def display_tournament_done(self):
        message = "Le tournoi est terminé !"
        self.display_message(message)

    def display_tour_done(self):
        message = "Le tour est terminé, plus de match à jouer"
        self.display_message(message)

    def display_tour_not_done(self):
        message = "Le tour n'est pas encore terminé"
        self.display_message(message)

    def display_save_to_database_done(self):
        message = "La sauvegarde dans la base de donnée a été effectuée dans le fichier db_chess_tournament.json"
        self.display_message(message)

    def display_load_from_database_done(self):
        message = "Le chargement de la base de donnée a été effectuée à partir du fichier db_chess_tournament.json "
        self.display_message(message)

    def display_load_from_database_error(self):
        message = "Le chargement de la base de donnée n'a pas pu se faire, vide? erronée?"
        self.display_message(message)

    #####################
    # Function for prompt
    #####################

    def check_input_number_of_players(self, input_number: int):
        if input_number.isnumeric:
            return True
        return False

    def check_input_number(self, input_number: int):
        if input_number.isnumeric:
            return True
        return False

    def check_input_text(self, input_text: str):
        if input_text == "":
            return False
        return True

    def check_input_time_control(self,input_time_control: str):
        time_control_valid_list = ["Bullet","Blitz","Rapid"]
        if input_time_control in time_control_valid_list:
            return True
        return False

    def check_input_validity_genre(self,input_genre: str):
        genre_valid_list = ["F","M"]
        if input_genre in genre_valid_list:
            return True
        return False
            
    def check_input_validity_birthday(self,birthday: str):
        format = "%m/%d/%y"
        try:
            datetime.strptime(birthday, format)
        except ValueError:
            return False
        return True

    def prompt_for_add_players(self, number_of_players):
        list_info_players = []
        for index in range(number_of_players):
            list_info_players.append(self.prompt_for_add_player(index+1))
        return list_info_players

    def check_validity_items(self,items, items_check):
        for i in range(len(items)):
            if items_check[i] == "check_input_number_of_players":
                if not self.check_input_number_of_players(items[i]): return False
            elif items_check[i] == "check_input_number":
                if not self.check_input_number(items[i]): return False
            elif items_check[i] == "check_input_text":
                if not self.check_input_text(items[i]): return False
            elif items_check[i] == "check_input_time_control":
                if not self.check_input_time_control(items[i]): return False
            elif items_check[i] == "check_input_validity_genre":
                if not self.check_input_validity_genre(items[i]): return False
            elif items_check[i] == "check_input_validity_birthday":
              if not self.check_input_validity_birthday(items[i]): return False
            else:
                return None
        return True

    def prompt_with_check_type_generic(self, items_prompt, prompt_title, items_check):
        confirmation = False
        check_validity = False
        while (not confirmation):
            while (not check_validity):
                items = self.prompt_generic(prompt_title,items_prompt)
                if self.check_validity_items(items, items_check):
                    break
                else:
                    self.display_input_error()   
            if self.prompt_for_confirmation():
                confirmation = True
        return items

    def prompt_for_add_player(self,index):
        items_prompt=[
            "Prénom : ",
            "Nom : ",
            "Date de naissance (MM/JJ/AA) : ",
            "Sexe (M/F) : ",
            "Classement : "
        ]
        items_check= [
            "check_input_text",
            "check_input_text",
            "check_input_validity_birthday",
            "check_input_validity_genre",
            "check_input_number"
        ]
        prompt_title = f"Ajouter le Joueur {index}:"
        return self.prompt_with_check_type_generic(items_prompt,prompt_title,items_check)
    # def prompt_for_add_player(self,index):
    #     items=[
    #         "Prénom : ",
    #         "Nom : ",
    #         "Date de naissance (MM/JJ/AA) : ",
    #         "Sexe (M/F) : ",
    #         "Classement : "
    #     ]
    #     confirmation = False
    #     check_validity = False
    #     while (not confirmation):
    #         while (not check_validity):
    #             list_info_player = self.prompt_generic(f"Ajouter le Joueur {index}:",items)
    #             if (self.check_input_text(list_info_player[0]) 
    #                 and self.check_input_text(list_info_player[1]) 
    #                 and self.check_input_validity_birthday(list_info_player[2]) 
    #                 and self.check_input_validity_genre(list_info_player[3])
    #                 and self.check_input_number(list_info_player[4])):
    #                 break
    #             else:
    #                 self.display_input_error()   
    #         if self.prompt_for_confirmation():
    #             confirmation = True
    #     return list_info_player

    def prompt_for_create_tournament(self):
        items=[
            "Nom du tournoi : ",
            "Lieu : ",
            "Contrôle du temps (Bullet/Blitz/Rapid) : ",
            "Description : "
        ]
        confirmation = False
        check_validity = False
        while (not confirmation):
            while (not check_validity):
                list_info_tournament = self.prompt_generic("Créer un tournoi",items) 
                if (self.check_input_text(list_info_tournament[0]) 
                    and self.check_input_text(list_info_tournament[1]) 
                    and self.check_input_time_control(list_info_tournament[2]) 
                    and self.check_input_text(list_info_tournament[3])):
                    break
                else:
                    self.display_input_error()   
            if self.prompt_for_confirmation():
                confirmation = True  
        return list_info_tournament

    def prompt_for_continue(self):
        input("Appuyer sur une touche pour continuer...") 

    def prompt_for_add_tournament_done(self):
        input("Ajout du tournoi terminé, veuillez appuyer sur une touche pour continuer") 

    def prompt_for_confirmation(self):
        user_input = ""
        while (user_input != ("y" or "n")):
            user_input =  input("Confirmez-vous la saisie? [y/n]") 
            if user_input == "y":
                return True 
            elif user_input == "n":
                return False
            print("Veuillez recommencez en choisissant un choix correct.")
          
    #############################################
    # Function for display information tournament
    #############################################

    def display_information_tournament(self, information:str):
        self.terminal_clear()
        print(information)
        self.prompt_for_continue()

    def display_all_information_tournament(self, tournament:Tournament):
        self.display_information_tournament(self.get_all_information_tournament(tournament))

    def display_tour(self, tournament:Tournament):
        self.display_information_tournament(self.get_string_tour(tournament))

    def display_matchs(self, tournament:Tournament):
        self.display_information_tournament(self.get_string_matchs(tournament))

    def display_player_sorted_by_rank_score(self, players:List[Player]):
        self.display_information_tournament(self.get_string_player_sorted_by_rank_score(players))

    def display_player_sorted_by_rank(self, players:List[Player],tournament_name:str=None):
        self.display_information_tournament(self.get_string_player_sorted_by_rank(players,tournament_name))

    def display_player_sorted_by_name(self, players:List[Player],tournament_name:str=None):
        self.display_information_tournament(self.get_string_player_sorted_by_name(players,tournament_name))

    def display_tournaments_sorted_by_name(self, tournaments:List[Tournament]):
        self.display_information_tournament(self.get_string_tournaments_sorted_by_name(tournaments))

    def display_tournament_infos(self, tournament:Tournament):
        self.display_information_tournament(self.get_string_tournament_infos(tournament))

    def get_all_information_tournament(self, tournament:Tournament):
        display_tournament = self.get_string_tournament_infos(tournament)
        display_tour = self.get_string_tour(tournament)
        display_player_sorted_by_rank_score = self.get_string_player_sorted_by_rank_score(tournament.players)
        return display_tournament + display_tour + display_player_sorted_by_rank_score

    def get_string_tour(self, tournament:Tournament):
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
            table_body =[tour.name,tour.date_begin,tour.date_end,matchs_display,status_tour]
            table.append(table_body)
        return str(tabulate(table,headers="firstrow",tablefmt="grid") +"\n")

    def get_string_matchs(self, tournament:Tournament):
        tours : List[Tour] = tournament.tours
        table = []
        table_body = []
        table_header = ['Match','Statut']
        table.append(table_header)
        for tour in tours:
            for match in tour.matchs:
                matchs_display = f"{match.player1.first_name} {match.player1.last_name} ({match.resultplayer1}) vs {match.player2.first_name} {match.player2.last_name} ({match.resultplayer2})"
                if(match.finish == True):
                    status_match= "Terminé"
                else:
                    status_match= "En cours"
                table.append([matchs_display,status_match])
        return str(tabulate(table,headers="firstrow",tablefmt="grid") +"\n")

    def get_string_player_sorted_by_rank_score(self, players:List[Player]):
        players_sorted_rank = sorted(players, key=lambda p: p.ranking)
        players_sorted_rank_score = sorted(players_sorted_rank, key=lambda p: p.score,reverse=True)
        table = []
        table_header = ['Joueur','Classement', 'Score']
        table.append(table_header)
        for player in players_sorted_rank_score:
            table_body = [f"{player.first_name} {player.last_name}", player.ranking, player.score]
            table.append(table_body)
        return str(tabulate(table,headers="firstrow",tablefmt="grid"))

    def get_string_player_sorted_by_rank(self, players:List[Player],tournament_name:str):
        players_sorted_rank = sorted(players, key=lambda p: p.ranking)
        table = []
        table_header = [f"Joueurs du tournoi \"{tournament_name}\" ranger par classement",'Classement']
        table.append(table_header)
        for player in players_sorted_rank:
            table_body = [f"{player.first_name} {player.last_name}", player.ranking]
            table.append(table_body)
        return str(tabulate(table,headers="firstrow",tablefmt="grid"))

    def get_string_player_sorted_by_name(self, players:List[Player],tournament_name:str=None):
        players_sorted_name = sorted(players, key=lambda p: p.first_name)
        table = []
        if tournament_name == None:
            table_header = [f"Acteurs des tournois ranger par ordre alphabétique:"]
        else:
            table_header = [f"Joueurs du tournoi \"{tournament_name}\" ranger par ordre alphabétique"]
        table.append(table_header)
        for player in players_sorted_name:
            table_body = [f"{player.first_name} {player.last_name}"]
            table.append(table_body)
        return str(tabulate(table,headers="firstrow",tablefmt="grid"))

    def get_string_tournaments_sorted_by_name(self, tournaments:List[Tournament]):
        tournaments_sorted_by_name = sorted(tournaments, key=lambda t: t.name)
        table = []
        table_header = ['Tournois ranger par ordre alphabétique']
        table.append(table_header)
        for tournament in tournaments_sorted_by_name:
            table_body = [self.get_string_tournament_infos(tournament)]
            table.append(table_body)
        return str(tabulate(table,headers="firstrow",tablefmt="grid"))

    def get_string_tournament_infos(self, tournament:Tournament):
        return f"Nom du tournoi : {tournament.name} | Lieu : {tournament.place} | Date début: {tournament.date_begin} | Date fin: {tournament.date_end}\n" + f"contrôle de temps : {tournament.time_control} | Description : {tournament.description} | Round {len(tournament.tours)}/{tournament.tours_number}\n"

    #############################
    # Function diverse
    #############################
    def terminal_clear(self):
        os.system("cls")
        self.display_banner()

    def display_banner(self):
        print("♙     ____ _                                                                    ♙")
        print("♙    / ___| |__   ___  ___ ___   _ __ ___   __ _ _ __   __ _  __ _  ___ _ __    ♙")
        print("♙   | |   | '_ \ / _ \/ __/ __| | '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \ '__|   ♙")
        print("♙   | |___| | | |  __/\__ \__ \ | | | | | | (_| | | | | (_| | (_| |  __/ |      ♙")
        print("♙    \____|_| |_|\___||___/___/ |_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|_|      ♙")
        print("♙                                                            |___/              ♙\n")