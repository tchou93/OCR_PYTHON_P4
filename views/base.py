from os import getcwd
from sys import path

try:
    path.insert(1, getcwd())
except IndexError:
    pass

import os
import time
from datetime import datetime
from typing import List, Tuple
from xmlrpc.client import boolean
from tabulate import tabulate
from models.player import Player
from models.round import Round
from models.match import Match
from models.tournament import Tournament


class View:
    """Used to display/asks some informations for users
    Instance methods:
        - Display the menu:
        display_menu_generic(self, menu_title: str, menu_options: List[str]) -> int
        display_menu_main(self) -> int
        display_menu_tournament(self) -> int
        display_menu_reports(self) -> int
        display_menu_tournament_reports(self, tournament_name: str) -> int
        display_menu_players_in_tournament_reports(self, tournament_name: str) -> int
        display_menu_choose_tournament(
        display_menu_tournament_action(self, tournament: Tournament) -> int
        display_menu_add_score(self, match: Match) -> int
        display_menu_modify_player_rank(self, tournament: Tournament) -> Tuple[int, int]:
        display_menu_report_choose_tournament(self, tounaments: List[Tournament]) -> int:
        display_message(self, message: str)
        display_input_error(self)
        display_tournament_done(self)
        display_tour_done(self)
        display_tour_not_done(self)
        display_save_to_database_done(self)
        display_load_from_database_done(self)
        display_load_from_database_error(self)
        - Function for prompt validity:
        check_input_number_of_players(self, input_number: int) -> boolean
        check_input_range(self, input_number: int) -> boolean
        check_input_text(self, input_text: str) -> boolean
        check_input_time_control(self, input_time_control: str) -> boolean
        check_input_validity_genre(self, input_genre: str) -> boolean
        check_input_validity_birthday(self, birthday: str) -> boolean
        check_validity_items(self, items, items_check) -> boolean
        - Function for prompt:
        prompt_generic(self, prompt_title: str, items: List[str]) -> List[str]
        prompt_with_check_type_generic(self, items_prompt, prompt_title, items_check) -> List[str]
        prompt_for_add_player(self, index) -> List[str]
        prompt_for_create_tournament(self) -> List[str]
        prompt_for_add_players(self, number_of_players) -> List[List[str]]
        prompt_for_continue(self)
        prompt_for_add_tournament_done(self)
        prompt_for_confirmation(self) -> boolean
        - Function for display information tournament:
        display_information_tournament(self, information: str)
        display_all_information_tournament(self, tournament: Tournament)
        display_round(self, tournament: Tournament)
        display_matchs(self, tournament: Tournament)
        display_player_sorted_by_rank_score(self, players: List[Player])
        display_player_sorted_by_rank(self, players: List[Player], tournament_name: str = None)
        display_player_sorted_by_name(self, players: List[Player], tournament_name: str = None)
        display_tournaments_sorted_by_name(self, tournaments: List[Tournament])
        display_tournament_infos(self, tournament: Tournament)
        get_all_information_tournament(self, tournament: Tournament) -> str
        get_string_round(self, tournament: Tournament) -> str
        get_string_matchs(self, tournament: Tournament) -> str
        get_string_player_sorted_by_rank_score(self, players: List[Player]) -> str
        get_string_player_sorted_by_rank(self, players: List[Player], tournament_name: str) -> str
        get_string_player_sorted_by_name(self, players: List[Player], tournament_name: str = None) -> str
        get_string_tournaments_sorted_by_name(self, tournaments: List[Tournament]) -> str
        get_string_tournament_infos(self, tournament: Tournament) -> str
        - Function diverse:
        terminal_clear(self)
        display_banner(self)
    """

    def __init__(self):
        pass

    ################################
    # Function for display the menu
    ################################

    def display_menu_generic(self, menu_title: str, menu_options: List[str]) -> int:
        """This function is used in order to create a specific menu."""
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

    def display_menu_main(self) -> int:
        """Display the main menu."""
        menu_main = [
            "Tournoi",
            "Sauvegarder les données",
            "Charger les données",
            "Rapports",
            "Quitter",
        ]
        return self.display_menu_generic("Menu principal", menu_main)

    def display_menu_tournament(self) -> int:
        """Display the menu tournament."""
        menu_tournament = [
            "Créer un tournoi",
            "[SIMU] Ajouter le tournoi random1",
            "[SIMU] Ajouter le tournoi random2",
            "Continuer un tournoi",
            "Retour au menu principal",
        ]
        return self.display_menu_generic("Tournoi", menu_tournament)

    def display_menu_reports(self) -> int:
        """Display the menu reports."""
        menu_reports = [
            "Rapport détaillé sur un tournoi",
            "Liste des tournois",
            "Liste des acteurs",
            "Retour au menu principal",
        ]
        return self.display_menu_generic("Rapports", menu_reports)

    def display_menu_tournament_reports(self, tournament_name: str) -> int:
        """Display the menu tournament reports."""
        menu_tournament_reports = [
            "Récapitulatif de tout le tournoi",
            "Joueurs du tournoi",
            "Liste des rounds du tournoi",
            "Liste des matchs du tournoi",
            "Retour au menu choisir un tournoi",
        ]
        return self.display_menu_generic(
            f'Rapport détaillé sur le tournoi "{tournament_name}":',
            menu_tournament_reports,
        )

    def display_menu_players_in_tournament_reports(self, tournament_name: str) -> int:
        """Display the menu players in tournament reports."""
        menu_tournament_reports = [
            "Liste de tous les joueurs par ordre alphabétique",
            "Liste de tous les joueurs par classement",
            f'Retour au menu des rapports détaillés du tournoi "{tournament_name}"',
        ]
        return self.display_menu_generic(
            f'Rapport joueurs du tournoi "{tournament_name}":', menu_tournament_reports
        )

    def display_menu_choose_tournament(
        self, tournaments_in_progress: List[Tournament]
    ) -> int:
        """Display a menu with the list of all tournament."""
        items = []
        for tournament_in_progress in tournaments_in_progress:
            items.append(
                f"{tournament_in_progress.name} (Round {len(tournament_in_progress.rounds)}"
                f"/{tournament_in_progress.rounds_number})"
            )
        items.append("Retour au menu tournoi")
        return self.display_menu_generic("Choisir un tournoi", items)

    def display_menu_tournament_action(self, tournament: Tournament) -> int:
        """Display a menu tournament action."""
        menu_create_tournament = [
            "Ajouter un round",
            "Jouer un match",
            "Modifier le classement d’un joueur",
            "Retour au menu tournoi",
        ]
        header_menu_tournament_action = self.get_all_information_tournament(tournament)
        return self.display_menu_generic(
            header_menu_tournament_action, menu_create_tournament
        )

    def display_menu_add_score(self, match: Match) -> int:
        """Display a menu add score."""
        items = [
            f"{match.player1.first_name} {match.player1.last_name} a gagné",
            f"{match.player2.first_name} {match.player2.last_name} a gagné",
            "Egalité",
        ]
        return self.display_menu_generic(
            f"Résultat du match {match.player1.first_name} {match.player1.last_name}"
            f" vs {match.player2.first_name} {match.player2.last_name}:",
            items,
        )

    def display_menu_modify_player_rank(
        self, tournament: Tournament
    ) -> Tuple[int, int]:
        """Display a menu with the rank of
        all the players, user can change the value."""
        players: List[Player] = tournament.players
        menu_players_ranks = []
        for player in players:
            menu_players_ranks.append(
                f"{player.first_name} {player.last_name} (Classement: {player.ranking})"
            )
        menu_players_ranks.append("Quitter")
        user_input_option = self.display_menu_generic(
            "Modification du classement", menu_players_ranks
        )

        if user_input_option != len(players) + 1:
            user_input_rank = input(
                "Entrer le nouveau classement pour le joueur"
                f"{players[user_input_option-1].first_name} {players[user_input_option-1].last_name}: "
            )
            return (user_input_option, int(user_input_rank))
        else:
            return (user_input_option, -1)

    def display_menu_report_choose_tournament(
        self, tounaments: List[Tournament]
    ) -> int:
        """Display a menu with all the tournament
        in order to choose it to obtain some reports."""
        items = []
        for tournament in tounaments:
            items.append(
                f"{tournament.name} (Round {len(tournament.rounds)}/{tournament.rounds_number})"
            )
        items.append("Retour au menu rapport")
        return self.display_menu_generic("Choisir un tournoi", items)

    ################################
    # Function for display message
    ################################

    def display_message(self, message: str):
        """Generic function in order to display a message on a formated screen
        include the banner."""
        self.terminal_clear()
        print(message)
        self.prompt_for_continue()

    def display_input_error(self):
        """Display a message to indicate an input error."""
        message = "Erreur dans une des saisies, veuillez recommencer"
        self.display_message(message)

    def display_tournament_done(self):
        """Display a message to indicate that the tournament is done."""
        message = "Le tournoi est terminé !"
        self.display_message(message)

    def display_tour_done(self):
        """Display a message to indicate that the tour is done."""
        message = "Le Round est terminé, plus de match à jouer"
        self.display_message(message)

    def display_tour_not_done(self):
        """Display a message to indicate that the tour is not done."""
        message = "Le Round n'est pas encore terminé"
        self.display_message(message)

    def display_save_to_database_done(self):
        """Display a message to indicate that the save to database is done."""
        message = "La sauvegarde dans la base de donnée a été effectuée dans le fichier db_chess_tournament.json"
        self.display_message(message)

    def display_load_from_database_done(self):
        """Display a message to indicate that the load from database is done."""
        message = "Le chargement de la base de donnée a été effectuée à partir du fichier db_chess_tournament.json "
        self.display_message(message)

    def display_load_from_database_error(self):
        """Display a message to indicate that the load from database cannot be process."""
        message = (
            "Le chargement de la base de donnée n'a pas pu se faire, vide? erronée?"
        )
        self.display_message(message)

    ##############################
    # Function for prompt validity
    ##############################

    def check_input_number_of_players(self, input_number: int) -> boolean:
        """check the validity when the user enter the number of players."""
        if input_number.isnumeric:
            return True
        return False

    def check_input_range(self, input_number: int) -> boolean:
        """check the validity when the user enter a range."""
        if input_number.isnumeric:
            return True
        return False

    def check_input_text(self, input_text: str) -> boolean:
        """check the validity when the user enter a text."""
        if input_text == "":
            return False
        return True

    def check_input_time_control(self, input_time_control: str) -> boolean:
        """check the validity when the user enter a time control."""
        time_control_valid_list = ["Bullet", "Blitz", "Rapid"]
        if input_time_control in time_control_valid_list:
            return True
        return False

    def check_input_validity_genre(self, input_genre: str) -> boolean:
        """check the validity when the user enter a genre."""
        genre_valid_list = ["F", "M"]
        if input_genre in genre_valid_list:
            return True
        return False

    def check_input_validity_birthday(self, birthday: str) -> boolean:
        """check the validity when the user enter a birthday."""
        format = "%m/%d/%y"
        try:
            datetime.strptime(birthday, format)
        except ValueError:
            return False
        return True

    def check_validity_items(self, items, items_check) -> boolean:
        """check the validity of some items. If all the items are valid,
        return true."""
        for i in range(len(items)):
            if items_check[i] == "check_input_number_of_players":
                if not self.check_input_number_of_players(items[i]):
                    return False
            elif items_check[i] == "check_input_range":
                if not self.check_input_range(items[i]):
                    return False
            elif items_check[i] == "check_input_text":
                if not self.check_input_text(items[i]):
                    return False
            elif items_check[i] == "check_input_time_control":
                if not self.check_input_time_control(items[i]):
                    return False
            elif items_check[i] == "check_input_validity_genre":
                if not self.check_input_validity_genre(items[i]):
                    return False
            elif items_check[i] == "check_input_validity_birthday":
                if not self.check_input_validity_birthday(items[i]):
                    return False
            else:
                return False
        return True

    #####################
    # Function for prompt
    #####################

    def prompt_generic(self, prompt_title: str, items: List[str]) -> List[str]:
        """This function is used in order to ask users to enter some specifics values."""
        self.terminal_clear()
        print(f"|{prompt_title}|")
        list_input = []
        for item in items:
            list_input.append(input(item))
        return list_input

    def prompt_with_check_type_generic(
        self, items_prompt, prompt_title, items_check
    ) -> List[str]:
        """This function asks to user some informations define on <items_prompt>,
        check if all the informations are valids, and if there is a confirmation
        the function return the list of inputs."""
        confirmation = False
        check_validity = False
        while not confirmation:
            while not check_validity:
                items = self.prompt_generic(prompt_title, items_prompt)
                if self.check_validity_items(items, items_check):
                    break
                else:
                    self.display_input_error()
            if self.prompt_for_confirmation():
                confirmation = True
        return items

    def prompt_for_add_player(self, index) -> List[str]:
        """This function asks/verify informations to add a player enter by a user.
        Returns the list of the inputs."""
        items_prompt = [
            "Prénom : ",
            "Nom : ",
            "Date de naissance (MM/JJ/AA) : ",
            "Sexe (M/F) : ",
            "Classement : ",
        ]
        items_check = [
            "check_input_text",
            "check_input_text",
            "check_input_validity_birthday",
            "check_input_validity_genre",
            "check_input_range",
        ]
        prompt_title = f"Ajouter le Joueur {index}:"
        return self.prompt_with_check_type_generic(
            items_prompt, prompt_title, items_check
        )

    def prompt_for_create_tournament(self) -> List[str]:
        """This function asks/verify informations to create a tournament enter by a user.
        Returns the list of the inputs."""
        items_prompt = [
            "Nom du tournoi : ",
            "Lieu : ",
            "Contrôle du temps (Bullet/Blitz/Rapid) : ",
            "Description : ",
        ]
        items_check = [
            "check_input_text",
            "check_input_text",
            "check_input_time_control",
            "check_input_text",
        ]
        prompt_title = "Créer un tournoi"
        return self.prompt_with_check_type_generic(
            items_prompt, prompt_title, items_check
        )

    def prompt_for_add_players(self, number_of_players) -> List[List[str]]:
        """This function asks/verify informations to add players enter by a user.
        Returns the list of the inputs."""
        list_info_players = []
        for index in range(number_of_players):
            list_info_players.append(self.prompt_for_add_player(index + 1))
        return list_info_players

    def prompt_for_continue(self):
        """This function is used to see a specific display before a clear
        screen."""
        input("Appuyer sur une touche pour continuer...")

    def prompt_for_add_tournament_done(self):
        """This function is used to see a message that a tournament is done"""
        input(
            "Ajout du tournoi terminé, veuillez appuyer sur une touche pour continuer"
        )

    def prompt_for_confirmation(self) -> boolean:
        """This function is used confirm an input."""
        user_input = ""
        while user_input != ("y" or "n"):
            user_input = input("Confirmez-vous la saisie? [y/n]")
            if user_input == "y":
                return True
            elif user_input == "n":
                return False
            print("Veuillez recommencez en choisissant un choix correct.")

    #############################################
    # Function for display information tournament
    #############################################

    def display_information_tournament(self, information: str):
        """Generic function in order to display correctly a string for
        users."""
        self.terminal_clear()
        print(information)
        self.prompt_for_continue()

    def display_all_information_tournament(self, tournament: Tournament):
        """Display all the information concerning a tournament."""
        self.display_information_tournament(
            self.get_all_information_tournament(tournament)
        )

    def display_round(self, tournament: Tournament):
        """Display all the information concerning a round."""
        self.display_information_tournament(self.get_string_round(tournament))

    def display_matchs(self, tournament: Tournament):
        """Display all the information concerning matchs."""
        self.display_information_tournament(self.get_string_matchs(tournament))

    def display_player_sorted_by_rank_score(self, players: List[Player]):
        """Display players sorted by rank and score."""
        self.display_information_tournament(
            self.get_string_player_sorted_by_rank_score(players)
        )

    def display_player_sorted_by_rank(
        self, players: List[Player], tournament_name: str = None
    ):
        """Display players sorted by rank."""
        self.display_information_tournament(
            self.get_string_player_sorted_by_rank(players, tournament_name)
        )

    def display_player_sorted_by_name(
        self, players: List[Player], tournament_name: str = None
    ):
        """Display players sorted by name."""
        self.display_information_tournament(
            self.get_string_player_sorted_by_name(players, tournament_name)
        )

    def display_tournaments_sorted_by_name(self, tournaments: List[Tournament]):
        """Display tournaments sorted by name."""
        self.display_information_tournament(
            self.get_string_tournaments_sorted_by_name(tournaments)
        )

    def display_tournament_infos(self, tournament: Tournament):
        """Display informations concerning a tournament."""
        self.display_information_tournament(
            self.get_string_tournament_infos(tournament)
        )

    def get_all_information_tournament(self, tournament: Tournament) -> str:
        """Get the string of all the information concerning a tournament."""
        display_tournament = self.get_string_tournament_infos(tournament)
        display_round = self.get_string_round(tournament)
        display_player_sorted_by_rank_score = (
            self.get_string_player_sorted_by_rank_score(tournament.players)
        )
        return display_tournament + display_round + display_player_sorted_by_rank_score

    def get_string_round(self, tournament: Tournament) -> str:
        """Get the string of all the information concerning a round."""
        rounds: List[Round] = tournament.rounds
        table = []
        table_header = ["Round", "Début", "Fin", "Match", "Statut"]
        table.append(table_header)
        for round in rounds:
            matchs_display = ""
            for match in round.matchs:
                matchs_display += (
                    f"{match.player1.first_name} {match.player1.last_name} ({match.resultplayer1})"
                    f" vs {match.player2.first_name} {match.player2.last_name} ({match.resultplayer2}) \n"
                )
            if round.finish is True:
                status_tour = "Terminé"
            else:
                status_tour = "En cours"
            table_body = [
                round.name,
                round.date_begin,
                round.date_end,
                matchs_display,
                status_tour,
            ]
            table.append(table_body)
        return str(tabulate(table, headers="firstrow", tablefmt="grid") + "\n")

    def get_string_matchs(self, tournament: Tournament) -> str:
        """Get the string of all the information concerning matchs."""
        rounds: List[Round] = tournament.rounds
        table = []
        table_header = ["Match", "Statut"]
        table.append(table_header)
        for round in rounds:
            for match in round.matchs:
                matchs_display = (
                    f"{match.player1.first_name} {match.player1.last_name} ({match.resultplayer1})"
                    f"vs {match.player2.first_name} {match.player2.last_name} ({match.resultplayer2})"
                )
                if match.finish is True:
                    status_match = "Terminé"
                else:
                    status_match = "En cours"
                table.append([matchs_display, status_match])
        return str(tabulate(table, headers="firstrow", tablefmt="grid") + "\n")

    def get_string_player_sorted_by_rank_score(self, players: List[Player]) -> str:
        """Get the string of players sorted by rank and score."""
        players_sorted_rank = sorted(players, key=lambda p: p.ranking)
        players_sorted_rank_score = sorted(
            players_sorted_rank, key=lambda p: p.score, reverse=True
        )
        table = []
        table_header = ["Joueur", "Classement", "Score"]
        table.append(table_header)
        for player in players_sorted_rank_score:
            table_body = [
                f"{player.first_name} {player.last_name}",
                player.ranking,
                player.score,
            ]
            table.append(table_body)
        return str(tabulate(table, headers="firstrow", tablefmt="grid"))

    def get_string_player_sorted_by_rank(
        self, players: List[Player], tournament_name: str
    ) -> str:
        """Get the string of players sorted by rank."""
        players_sorted_rank = sorted(players, key=lambda p: p.ranking)
        table = []
        table_header = [
            f'Joueurs du tournoi "{tournament_name}" ranger par classement',
            "Classement",
        ]
        table.append(table_header)
        for player in players_sorted_rank:
            table_body = [f"{player.first_name} {player.last_name}", player.ranking]
            table.append(table_body)
        return str(tabulate(table, headers="firstrow", tablefmt="grid"))

    def get_string_player_sorted_by_name(
        self, players: List[Player], tournament_name: str = None
    ) -> str:
        """Get the string of players sorted by name."""
        players_sorted_name = sorted(players, key=lambda p: p.first_name)
        table = []
        if tournament_name is None:
            table_header = ["Acteurs des tournois ranger par ordre alphabétique:"]
        else:
            table_header = [
                f'Joueurs du tournoi "{tournament_name}" ranger par ordre alphabétique'
            ]
        table.append(table_header)
        for player in players_sorted_name:
            table_body = [f"{player.first_name} {player.last_name}"]
            table.append(table_body)
        return str(tabulate(table, headers="firstrow", tablefmt="grid"))

    def get_string_tournaments_sorted_by_name(
        self, tournaments: List[Tournament]
    ) -> str:
        """Get the string of tournaments sorted by name."""
        tournaments_sorted_by_name = sorted(tournaments, key=lambda t: t.name)
        table = []
        table_header = ["Tournois ranger par ordre alphabétique"]
        table.append(table_header)
        for tournament in tournaments_sorted_by_name:
            table_body = [self.get_string_tournament_infos(tournament)]
            table.append(table_body)
        return str(tabulate(table, headers="firstrow", tablefmt="grid"))

    def get_string_tournament_infos(self, tournament: Tournament) -> str:
        """Get the string of informations concerning a tournament."""
        return (
            f"Nom du tournoi : {tournament.name} | Lieu : {tournament.place} | "
            f"Date début: {tournament.date_begin} | Date fin: {tournament.date_end}\n"
            f"contrôle de temps : {tournament.time_control} | Description : {tournament.description} |"
            f"Round {len(tournament.rounds)}/{tournament.rounds_number}\n"
        )

    #############################
    # Function diverse
    #############################

    def terminal_clear(self):
        """Generic function in order to clear a terminal by displaying a banner."""
        os.system("cls")
        self.display_banner()

    def display_banner(self):
        """Display a banner."""
        print(
            r"♙     ____ _                                                                    ♙"
        )
        print(
            r"♙    / ___| |__   ___  ___ ___   _ __ ___   __ _ _ __   __ _  __ _  ___ _ __    ♙"
        )
        print(
            r"♙   | |   | '_ \ / _ \/ __/ __| | '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \ '__|   ♙"
        )
        print(
            r"♙   | |___| | | |  __/\__ \__ \ | | | | | | (_| | | | | (_| | (_| |  __/ |      ♙"
        )
        print(
            r"♙    \____|_| |_|\___||___/___/ |_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|_|      ♙"
        )
        print(
            r"♙                                                            |___/              ♙"
            "\n"
        )


if __name__ == "__main__":
    view = View()
    view.display_banner()
