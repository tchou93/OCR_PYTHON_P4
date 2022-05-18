import random
from typing import List
from models.player import Player
from models.round import Round
from models.match import Match
from models.tournament import Tournament
from controllers.database import Database_tournament
from views.base import View


class Controller:
    def __init__(self, view: View):
        self.view = view
        self.tournaments: List[Tournament] = []
        self.tournament_active: Tournament = None
        self.tournament_simu: Tournament = None
        self.round_active: Round = None
        self.match_active: Match = None

    #####################
    # Menu
    #####################
    def option_menu_main(self):
        """Display the menu <Menu principal> on the terminal"""
        user_input_menu_main = self.view.display_menu_main()
        if user_input_menu_main == 1:
            # Enter to the option: 1 - Tournoi
            self.option_menu_tournament()
        elif user_input_menu_main == 2:
            # Enter to the option: 2 - Sauvegarder les données
            Database_tournament.clear_all_tab_in_db()
            Database_tournament.option_save_all_serialized_table_to_db(self.tournaments)
            self.option_menu_main()
        elif user_input_menu_main == 3:
            # Enter to the option: 3 - Charger les données
            tournaments_in_db = Database_tournament.option_load_from_db()
            if tournaments_in_db is not None:
                self.tournaments = tournaments_in_db
            self.option_menu_main()
        elif user_input_menu_main == 4:
            # Enter to the option: 4 - Rapports
            self.option_menu_reports()

    def option_menu_tournament(self):
        """Display the menu <Tournoi> on the terminal"""
        user_input_menu_option_tournament = self.view.display_menu_tournament()
        if user_input_menu_option_tournament == 1:
            # Enter to the option: 1 - Créer un tournoi
            self.option_create_tournament()
            self.option_menu_tournament()
        elif user_input_menu_option_tournament == 2:
            # Enter to the option: 2 - Ajouter le tournoi random1
            self.add_tournament_random_1()
            self.option_menu_tournament()
        elif user_input_menu_option_tournament == 3:
            # Enter to the option: 3 - Ajouter le tournoi random2
            self.add_tournament_random_2()
            self.option_menu_tournament()
        elif user_input_menu_option_tournament == 4:
            # Enter to the option: 4 - Choisir un tournoi
            self.option_menu_choose_tournament()
        else:
            # Enter to the option: 5 - Retour au menu principal
            self.option_menu_main()

    def option_menu_choose_tournament(self):
        """Display the menu <Choisir un tournoi> on the terminal"""
        tournaments_in_progress = self.tournaments_in_progress()
        user_input_menu_option_tournament = self.view.display_menu_choose_tournament(
            tournaments_in_progress
        )
        if user_input_menu_option_tournament < len(tournaments_in_progress) + 1:
            # Enter to the option: 1:X - <tournoi>
            self.tournament_active = tournaments_in_progress[
                user_input_menu_option_tournament - 1
            ]
            self.option_menu_tournament_action()
        else:
            # Enter to the option: Retour au menu tournoi
            self.option_menu_tournament()

    def option_menu_tournament_action(self):
        """Display the menu <Tournoi x> on the terminal"""
        user_input_menu_tournament_action = self.view.display_menu_tournament_action(
            self.tournament_active
        )
        self.round_active = self.round_to_play()
        self.match_active = self.match_to_play()
        if user_input_menu_tournament_action == 1:
            # Enter to the option: 1 - Ajouter un round
            self.option_add_a_round()
            self.option_menu_tournament_action()
        elif user_input_menu_tournament_action == 2:
            # Enter to the option: 2 - Jouer un match
            self.option_play_match()
            self.option_menu_tournament_action()
        elif user_input_menu_tournament_action == 3:
            # Enter to the option: 3 - Modifier le classement d'un joueur
            self.option_modify_player_rank()
        else:
            # Enter to the option: 4 - Retour au menu tournoi
            self.option_menu_tournament()

    def option_menu_reports(self):
        """Display the menu <Rapports> on the terminal"""
        user_input_menu_option_reports = self.view.display_menu_reports()
        if user_input_menu_option_reports == 1:
            # Enter to the option: 1 - Rapport détaillé sur un tournoi
            self.option_menu_reports_choose_tournament()
        elif user_input_menu_option_reports == 2:
            # Enter to the option: 2 - Liste des tournois
            self.view.display_tournaments_sorted_by_name(self.tournaments)
            self.option_menu_reports()
        elif user_input_menu_option_reports == 3:
            # Enter to the option: 3 - Liste des acteurs
            self.option_reports_all_actors()
            self.option_menu_reports()
        else:
            # Enter to the option: 4 - Retour au menu principal
            self.option_menu_main()

    def option_menu_reports_choose_tournament(self):
        """Display the menu <Choisir un tournoi> on the terminal"""
        user_input_menu_reports_all_tournament = (
            self.view.display_menu_report_choose_tournament(self.tournaments)
        )
        if user_input_menu_reports_all_tournament < len(self.tournaments) + 1:
            # Enter to the option: 1:X - <Nom des tournois>
            self.tournament_active = self.tournaments[
                user_input_menu_reports_all_tournament - 1
            ]
            self.option_menu_reports_detailed_tournament()
        else:
            # Enter to the option: X+1 - Retour au menu tournoi
            self.option_menu_reports()

    def option_menu_reports_detailed_tournament(self):
        """Display the menu <Rapport détaillé sur le tournoi> on the terminal"""
        user_input_menu_tournament_reports = self.view.display_menu_tournament_reports(
            self.tournament_active.name
        )
        if user_input_menu_tournament_reports == 1:
            # Enter to the option: 1 - Récapitulatif de tout le tournoi
            self.view.display_all_information_tournament(self.tournament_active)
            self.option_menu_reports_detailed_tournament()
        elif user_input_menu_tournament_reports == 2:
            # Enter to the option: 2 - Joueurs du tournoi
            self.option_menu_reports_tournament_players()
        elif user_input_menu_tournament_reports == 3:
            # Enter to the option: 3 - Liste des rounds du tournoi
            self.view.display_tour(self.tournament_active)
            self.option_menu_reports_detailed_tournament()
        elif user_input_menu_tournament_reports == 4:
            # Enter to the option: 4 - Liste des matchss du tournoi
            self.view.display_matchs(self.tournament_active)
            self.option_menu_reports_detailed_tournament()
        else:
            # Enter to the option: 5 - Retour au menu des rapports
            self.option_menu_reports_choose_tournament()

    def option_menu_reports_tournament_players(self):
        """Display the menu <Rapport joueurs du tournoi X> on the terminal"""
        user_input_menu_players_in_tournament_reports = (
            self.view.display_menu_players_in_tournament_reports(
                self.tournament_active.name
            )
        )
        if user_input_menu_players_in_tournament_reports == 1:
            # Enter to the option: 1 - Liste de tous les joueurs par ordre alphabétique
            self.view.display_player_sorted_by_name(
                self.tournament_active.players, self.tournament_active.name
            )
            self.option_menu_reports_tournament_players()
        elif user_input_menu_players_in_tournament_reports == 2:
            # Enter to the option: 2- Liste de tous les joueurs par classement
            self.view.display_player_sorted_by_rank(
                self.tournament_active.players, self.tournament_active.name
            )
            self.option_menu_reports_tournament_players()
        else:
            # Enter to the option: 3- Retour au menu des rapports détaillés du tournoi X
            self.option_menu_reports_detailed_tournament()

    #######################
    # Option
    #######################

    def option_add_a_round(self):
        if self.tournament_active.finish is False:
            if self.round_active is None:
                self.tournament_active.add_round()
                self.tournament_active.rounds[
                    len(self.tournament_active.rounds) - 1
                ].set_date_begin()
            else:
                self.view.display_tour_not_done()
        else:
            self.view.display_tournament_done()

    def option_play_match(self):
        if self.tournament_active.finish is True:
            self.view.display_tournament_done()
        elif self.match_active is None:
            self.view.display_tour_done()
        else:
            self.match_active.results_match(
                self.view.display_menu_add_score(self.match_active)
            )
            self.match_active.finish = True
            if self.last_match_in_current_in_tournament(self.match_active):
                self.round_active.finish = True
                self.tournament_active.finish = True
                self.round_active.set_date_end()
                self.tournament_active.set_date_end()
                self.view.display_tournament_done()
            elif self.last_match_in_current_tour(self.match_active):
                self.round_active.finish = True
                self.round_active.set_date_end()

    def option_modify_player_rank(self):
        user_input_menu_player_rank = self.view.display_menu_modify_player_rank(
            self.tournament_active
        )
        if user_input_menu_player_rank[0] < (len(self.tournament_active.players) + 1):
            self.tournament_active.players[
                user_input_menu_player_rank[0] - 1
            ].ranking = user_input_menu_player_rank[1]
            self.option_modify_player_rank()
        else:
            self.option_menu_tournament_action()

    def option_reports_all_actors(self):
        actors = Database_tournament.deserialized_players(
            Database_tournament.load_serialized_from_db("player")
        )
        self.view.display_player_sorted_by_name(actors)

    def option_create_tournament(self):
        list_input_infos_tournament = self.view.prompt_for_create_tournament()
        new_tournament = Tournament(
            list_input_infos_tournament[0],
            list_input_infos_tournament[1],
            list_input_infos_tournament[2],
            list_input_infos_tournament[3],
        )

        list_info_players = self.view.prompt_for_add_players(8)
        for list_info_player in list_info_players:
            player = Player(
                list_info_player[0],
                list_info_player[1],
                list_info_player[2],
                list_info_player[3],
                list_info_player[4],
            )
            new_tournament.add_player(player)
        new_tournament.set_date_begin()
        self.tournaments.append(new_tournament)
        self.view.terminal_clear()
        self.view.display_player_sorted_by_rank_score(new_tournament.players)
        # !!!!!!!!!!!!!! TBD !!!!!!!!!!!!!!
        # Faire en sorte qu'on puisse ressortir de cette option
        # Faire en sorte qu'on puisse ajouter un joueur si la BD est chargé

    #######################
    # Option
    #######################

    # Option for the menu "option_menu_tournament_action"
    def match_to_play(self):
        if self.round_active is None:
            return None
        for match in self.round_active.matchs:
            if not match.finish:
                return match
        return None

    def round_to_play(self):
        for round in self.tournament_active.rounds:
            if not round.finish:
                return round
        return None

    # Option for the menu "option_play_match"
    def last_match_in_current_tour(self, match: Match):
        for index in range(len(self.round_active.matchs)):
            if ((self.round_active.matchs[index]) == match) and (
                index == len(self.round_active.matchs) - 1
            ):
                return True
        else:
            return False

    def last_match_in_current_in_tournament(self, match: Match):
        if (
            len(self.tournament_active.rounds) == self.tournament_active.rounds_number
        ) and self.last_match_in_current_tour(match):
            return True
        else:
            return False

    # Option for the menu "option_menu_choose_tournament"
    def tournaments_in_progress(self):
        tournaments_in_progress = []
        for tournament in self.tournaments:
            if tournament.finish is False:
                tournaments_in_progress.append(tournament)
        return tournaments_in_progress

    ##########################
    # Function for simulation
    ##########################
    def add_tournament_random_1(self):
        new_tournament = Tournament(
            "Tournoi Random1", "Paris", "Bullet", "Description du tounoi Random1"
        )
        new_tournament.add_player(Player("Inès-Corinne", "Voisin", "03/19/85", "M"))
        new_tournament.add_player(Player("Léon", "Aubry", "02/04/00", "F"))
        new_tournament.add_player(Player("Michelle ", "Hardy", "09/10/98", "F"))
        new_tournament.add_player(
            Player("Denise Martineau", "Renault", "02/26/90", "M")
        )
        new_tournament.add_player(Player("Auguste", "Regnier", "04/12/95", "M"))
        new_tournament.add_player(Player("Anne-Agathe", "Guerin", "01/01/88", "M"))
        new_tournament.add_player(Player("Henriette ", "Deschamps", "08/03/01", "M"))
        new_tournament.add_player(
            Player("Jacqueline Riou", "Lemaitre", "04/23/89", "F")
        )
        for player in new_tournament.players:
            player.ranking = random.randint(1, 1000)
        new_tournament.set_date_begin()
        self.tournaments.append(new_tournament)
        self.view.prompt_for_add_tournament_done()

    def add_tournament_random_2(self):
        new_tournament = Tournament(
            "Tournoi Random2", "Marseille", "Blitz", "Description du tounoi Random2"
        )
        new_tournament.add_player(Player("Bernadette ", "Guilbert", "08/27/86", "M"))
        new_tournament.add_player(Player("Xavier", "Bernier", "02/13/99", "F"))
        new_tournament.add_player(Player("Auguste ", "Olivier", "02/29/92", "F"))
        new_tournament.add_player(Player("Geneviève", "Dupuy", "12/29/89", "M"))
        new_tournament.add_player(Player("Inès-Louise", "Pasquier", "09/06/86", "M"))
        new_tournament.add_player(Player("Emmanuelle ", "Bourgeois", "06/09/01", "M"))
        new_tournament.add_player(Player("Claude ", "Meunier", "03/27/96", "M"))
        new_tournament.add_player(Player("Elisabeth ", "Denis", "05/22/85", "F"))
        for player in new_tournament.players:
            player.ranking = random.randint(1, 1000)
        new_tournament.set_date_begin()
        self.tournaments.append(new_tournament)
        self.view.prompt_for_add_tournament_done()

    def run(self):
        self.option_menu_main()
