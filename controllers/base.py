from os import getcwd
from sys import path, exit

try:
    path.insert(1, getcwd())
except IndexError:
    pass

import random
from typing import List
from xmlrpc.client import Boolean, boolean
from models.player import Player
from models.round import Round
from models.match import Match
from models.tournament import Tournament
from controllers.database import Database_tournament
from views.base import View

CONST_NUMBER_PLAYER = 8


class Controller:
    """Use the view and the models to build menu for the chess manager."""

    def __init__(self, view: View):
        self.view = view
        self.tournaments: List[Tournament] = []
        self.actors: List[Player] = []
        self.tournament_active: Tournament = None
        self.round_active: Round = None
        self.match_active: Match = None

        # actors_tmp and tournament_tmp are usefull to
        # create a new tournament with new players
        self.actors_tmp: List[Player] = []
        self.tournament_tmp: Tournament = None

    #####################
    # Menu
    #####################
    def option_menu_main(self):
        """Display the menu <Menu principal> on the terminal."""
        user_input_menu_main = self.view.display_menu_main()
        if user_input_menu_main == 1:
            # Enter to the option: 1 - Tournoi
            self.option_menu_tournament()
        elif user_input_menu_main == 2:
            # Enter to the option: 2 - Sauvegarder les données
            self.option_save_database()
            self.option_menu_main()
        elif user_input_menu_main == 3:
            # Enter to the option: 3 - Charger les données
            self.option_load_database()
            self.option_menu_main()
        elif user_input_menu_main == 4:
            # Enter to the option: 4 - Rapports
            self.option_menu_reports()
        else:
            # Enter to the option: 5 - Quitter
            exit()

    def option_menu_tournament(self):
        """Display the menu <Tournoi> on the terminal."""
        user_input_menu_option_tournament = self.view.display_menu_tournament()
        if user_input_menu_option_tournament == 1:
            # Enter to the option: 1 - Créer un tournoi
            self.option_create_tournament()
            self.option_menu_tournament()
        elif user_input_menu_option_tournament == 2:
            # Enter to the option: 2 - [SIMU] Ajouter le tournoi random1
            self.add_tournament_random_1()
            self.option_menu_tournament()
        elif user_input_menu_option_tournament == 3:
            # Enter to the option: 3 - [SIMU] Ajouter le tournoi random2
            self.add_tournament_random_2()
            self.option_menu_tournament()
        elif user_input_menu_option_tournament == 4:
            # Enter to the option: 4 - Continuer un tournoi
            self.option_menu_choose_tournament()
        elif user_input_menu_option_tournament == 5:
            # Enter to the option: 5 - Retour au menu principal
            self.option_menu_main()

    def option_menu_add_players(self):
        """Display the menu <Ajouter X joueurs> on the terminal."""
        user_input_menu_add_players = self.view.display_menu_add_players(
            CONST_NUMBER_PLAYER - len(self.tournament_tmp.players)
        )
        if user_input_menu_add_players == 1:
            # Enter to the option: 1 - Ajouter un acteur
            if not self.actors:
                self.view.prompt_for_no_actors()
            else:
                self.option_menu_add_actor()
            self.option_menu_add_players()
        elif user_input_menu_add_players == 2:
            # Enter to the option: 2 - Créer un joueur
            self.option_create_a_player()
            self.option_menu_add_players()
        else:
            # Enter to the option: 3 - Quitter
            self.option_menu_tournament()

    def option_menu_add_actor(self):
        """Display the menu <Choisir un acteur> on the terminal."""
        user_input_menu_add_actor = self.view.display_menu_add_actor(self.actors_tmp)
        if user_input_menu_add_actor < len(self.actors_tmp) + 1:
            # Enter to the option: 1:X - <acteurs>
            self.option_add_actor(self.actors_tmp[user_input_menu_add_actor - 1])
        else:
            # Enter to the option: X+1 - Retour au menu d'ajout de joueur
            self.option_menu_add_players()

    def option_menu_choose_tournament(self):
        """Display the menu <Choisir un tournoi> on the terminal."""
        tournaments_in_progress = self.tournaments_in_progress()
        user_input_menu_option_tournament = self.view.display_menu_choose_tournament(
            tournaments_in_progress
        )
        if user_input_menu_option_tournament < len(tournaments_in_progress) + 1:
            # Enter to the option: 1:X - <tournois>
            self.tournament_active = tournaments_in_progress[
                user_input_menu_option_tournament - 1
            ]
            self.option_menu_tournament_action()
        else:
            # Enter to the option: Retour au menu tournoi
            self.option_menu_tournament()

    def option_menu_tournament_action(self):
        """Display the menu <Tournoi x> on the terminal."""
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
        """Display the menu <Rapports> on the terminal."""
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
        """Display the menu <Choisir un tournoi> on the terminal."""
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
        """Display the menu <Rapport détaillé sur le tournoi> on the terminal."""
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
            self.view.display_round(self.tournament_active)
            self.option_menu_reports_detailed_tournament()
        elif user_input_menu_tournament_reports == 4:
            # Enter to the option: 4 - Liste des matchss du tournoi
            self.view.display_matchs(self.tournament_active)
            self.option_menu_reports_detailed_tournament()
        else:
            # Enter to the option: 5 - Retour au menu des rapports
            self.option_menu_reports_choose_tournament()

    def option_menu_reports_tournament_players(self):
        """Display the menu <Rapport joueurs du tournoi X> on the terminal."""
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

    def option_save_database(self):
        """Save instance attributes <tournaments> and <actors>
        to database, display a message according to the successful.
        """
        result = Database_tournament.option_save_all_serialized_table_to_db(
            self.tournaments, self.actors
        )
        if result is True:
            self.view.display_save_to_database_done()
        else:
            self.view.display_save_to_database_error()

    def option_load_database(self):
        """Load the database to instance attributes <tournaments> and <actors>.
        Display a message according to the successful."""
        (tournaments_in_db, actors) = Database_tournament.option_load_from_db()
        if (tournaments_in_db, actors) == (None, None):
            self.view.display_load_from_database_error()
        else:
            self.view.display_load_from_database_done()
            self.tournaments = tournaments_in_db
            self.actors = actors

    def option_add_a_round(self):
        """Add a round and set the begin time if the active round is finish and
        if the tournament is not finish, else display a message."""
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
        """Play a match if the active tournament is not finish and set the attributes
        finish and the end time for the tournament and the rounds."""
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
                self.tournament_active.save_points_players = [
                    player.score for player in self.tournament_active.players
                ]
                self.reset_score_players(self.tournament_active.players)
                self.view.display_tournament_done()
            elif self.last_match_in_current_round(self.match_active):
                self.round_active.finish = True
                self.round_active.set_date_end()

    def option_modify_player_rank(self):
        """Option for modify a player rank in the active tournament."""
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
        """Collect all the actors in the database then display them."""
        # actors = Database_tournament.deserialized_players(
        #     Database_tournament.load_serialized_from_db("player")
        # )
        self.view.display_player_sorted_by_name(self.actors)

    def option_create_tournament(self):
        """Ask the user some informations in order to create the tournament and
        to add/create CONST_NUMBER_PLAYER players."""
        if self.all_tournaments_are_done():
            tournaments_names = [tournament.name for tournament in self.tournaments]
            list_input_infos_tournament = self.view.prompt_for_create_tournament(
                tournaments_names
            )
            self.tournament_tmp = Tournament(
                list_input_infos_tournament[0],
                list_input_infos_tournament[1],
                list_input_infos_tournament[2],
                list_input_infos_tournament[3],
            )
            self.tournament_tmp.set_date_begin()
            self.actors_tmp = self.actors.copy()
            self.actors_tmp = sorted(self.actors_tmp, key=lambda p: p.first_name)
            self.option_menu_add_players()
        else:
            self.view.prompt_for_tournaments_not_finish()

    def option_add_actor(self, actor_to_add: Player):
        """Add an actor to a tempory tournament and if the number
        of players is reached, add the tempory tournament
        to the instance attribute <tournaments>."""
        self.actors_tmp.remove(actor_to_add)
        self.tournament_tmp.players.append(actor_to_add)
        if len(self.tournament_tmp.players) == CONST_NUMBER_PLAYER:
            self.add_actors(self.tournament_tmp.players)
            self.tournaments.append(self.tournament_tmp)
            self.option_menu_tournament()

    def option_create_a_player(self):
        """Ask some informations for user to create a player.
        There are some checks concerning the input, for example
        the ranks."""
        list_info_player = self.view.prompt_for_add_player(
            self.get_all_actors_new_player_ranks()
        )
        player = Player(
            list_info_player[0],
            list_info_player[1],
            list_info_player[2],
            list_info_player[3],
            int(list_info_player[4]),
        )
        self.tournament_tmp.players.append(player)
        if len(self.tournament_tmp.players) == CONST_NUMBER_PLAYER:
            self.add_actors(self.tournament_tmp.players)
            self.tournaments.append(self.tournament_tmp)
            self.option_menu_tournament()

    ##########################
    # Function used in option
    ##########################

    def reset_score_players(self, players: List[Player]):
        """Reset all the score of players when the tournament is done."""
        for player in players:
            player.score = 0.0

    def add_actors(self, actors: List[Player]):
        """Add in the list of actor all the Player who are not in this list."""
        for actor in actors:
            if actor not in self.actors:
                self.actors.append(actor)

    def get_all_actors_new_player_ranks(self) -> List[int]:
        """Function to get all the ranks of all the actors."""
        all_actors_ranks = [actor.ranking for actor in self.actors]
        new_player_ranks = [player.ranking for player in self.tournament_tmp.players]
        all_actors_new_player_ranks = list(set(all_actors_ranks + new_player_ranks))
        all_actors_new_player_ranks.sort()
        return all_actors_new_player_ranks

    def all_tournaments_are_done(self) -> boolean:
        """Check is all tournaments are done."""
        tournaments_status = [tournament.finish for tournament in self.tournaments]
        if False in tournaments_status:
            return False
        else:
            return True

    def match_to_play(self):
        """Search the match in progress.

        Returns:
            Round: First match in the list matchs of the active round which is not finish.
        """
        if self.round_active is None:
            return None
        for match in self.round_active.matchs:
            if not match.finish:
                return match
        return None

    def round_to_play(self) -> Round:
        """Search the round in progress.

        Returns:
            Round: First round in the list rounds of the active tournament which is not finish.
        """
        for round in self.tournament_active.rounds:
            if not round.finish:
                return round
        return None

    def last_match_in_current_round(self, match: Match) -> Boolean:
        """Determine if the match is the last match in the current round.

        Args:
            match (Match): Match instance.

        Returns:
            Boolean: True if the match is the last match in the current round.
        """
        for index in range(len(self.round_active.matchs)):
            if ((self.round_active.matchs[index]) == match) and (
                index == len(self.round_active.matchs) - 1
            ):
                return True
        else:
            return False

    def last_match_in_current_in_tournament(self, match: Match) -> Boolean:
        """Determine if the match is the last match in the current tournament.

        Args:
            match (Match): Match instance.

        Returns:
            Boolean: True if the match is the last match in the current tournament.
        """
        if (
            len(self.tournament_active.rounds) == self.tournament_active.rounds_number
        ) and self.last_match_in_current_round(match):
            return True
        else:
            return False

    def tournaments_in_progress(self) -> List[Tournament]:
        """Find all the tournaments in progress.

        Returns:
            List[Tournament]: Tournaments in progress.
        """
        tournaments_in_progress = []
        for tournament in self.tournaments:
            if tournament.finish is False:
                tournaments_in_progress.append(tournament)
        return tournaments_in_progress

    ##########################
    # Function for simulation
    ##########################
    def add_tournament_random_1(self):
        """Add a random tournament with 8 players for simulation."""
        new_tournament = Tournament(
            "Random1", "Paris", "Bullet", "Description du tounoi Random1"
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
        new_tournament.set_date_begin()
        for player in new_tournament.players:
            player.ranking = random.randint(1, 1000)
        self.add_actors(new_tournament.players)
        self.tournaments.append(new_tournament)
        self.view.prompt_for_add_tournament_done()

    def add_tournament_random_2(self):
        """Add a random tournament with 8 players for simulation."""
        new_tournament = Tournament(
            "Random2", "Marseille", "Blitz", "Description du tounoi Random2"
        )
        new_tournament.add_player(Player("Bernadette ", "Guilbert", "08/27/86", "M"))
        new_tournament.add_player(Player("Xavier", "Bernier", "02/13/99", "F"))
        new_tournament.add_player(Player("Auguste ", "Olivier", "02/29/92", "F"))
        new_tournament.add_player(Player("Geneviève", "Dupuy", "12/29/89", "M"))
        new_tournament.add_player(Player("Inès-Louise", "Pasquier", "09/06/86", "M"))
        new_tournament.add_player(Player("Emmanuelle ", "Bourgeois", "06/09/01", "M"))
        new_tournament.add_player(Player("Claude ", "Meunier", "03/27/96", "M"))
        new_tournament.add_player(Player("Elisabeth ", "Denis", "05/22/85", "F"))
        new_tournament.set_date_begin()
        for player in new_tournament.players:
            player.ranking = random.randint(1, 1000)
        self.add_actors(new_tournament.players)
        self.tournaments.append(new_tournament)
        self.view.prompt_for_add_tournament_done()

    def run(self):
        """Run the main menu."""
        self.option_menu_main()


if __name__ == "__main__":
    print("test")
