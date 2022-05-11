"""Define the main controller."""
from operator import truediv
from re import A
from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match
from models.tournament import Tournament
from views.base import View
import random
from tinydb import TinyDB

class Controller:
    """Main controller."""

    def __init__(self,view: View):
        self.view  = view
        self.tournaments:List[Tournament] = []
        self.tournament_active:Tournament = None
        self.tournament_simu:Tournament = None
        self.tour_active:Tour = None
        self.match_active:Match = None
        self.db = TinyDB('db_chess_tournament.json')
    #####################
    # Function for menu
    #####################
    def option_menu_main(self):
        # Menu principal
        user_input_menu_main = self.view.display_menu_main()
        if (user_input_menu_main == 1):
            # 1 - Tournoi
            self.option_menu_tournament()
        elif (user_input_menu_main == 2):
            # 2 - Sauvegarder les données
            self.clear_all_tab_in_db()
            self.option_save_all_serialized_table_to_db()
            self.option_menu_main()
        elif (user_input_menu_main == 3):
            # 3 - Charger les données
            self.option_load_from_db() #To be update
            self.option_menu_main()
        elif (user_input_menu_main == 4):
            # 4 - Rapports
            self.option_menu_reports()
        elif (user_input_menu_main == 5):
            # 5 – [TEST]
            self.simu1()
            self.option_menu_main()

    def option_menu_tournament(self):
        # Menu Tournoi
        user_input_menu_option_tournament= self.view.display_menu_tournament()
        if (user_input_menu_option_tournament == 1):
            # 1 - Créer un tournoi
            self.option_create_tournament()
            self.option_menu_tournament()
        elif (user_input_menu_option_tournament == 2):
            # 2 - Choisir un tournoi
            self.option_menu_choose_tournament()
        else:
            # 3 - Retour au menu principal
            self.option_menu_main()

    def option_menu_choose_tournament(self):
        # Menu choisir un tournoi
        tournaments_in_progress = self.tournaments_in_progress()
        user_input_menu_option_tournament = self.view.display_menu_choose_tournament(tournaments_in_progress)
        if user_input_menu_option_tournament < len(tournaments_in_progress) + 1:
            # 1:X - <tournoi>
            self.option_tournament_selected(tournaments_in_progress[user_input_menu_option_tournament-1])
            self.option_menu_tournament_action()
        else:
            # Retour au menu tournoi
            self.option_menu_tournament()

    def option_menu_tournament_action(self):
        user_input_menu_tournament_action = self.view.display_menu_tournament_action(self.tournament_active)
        self.view.display_all_information_tournament(self.tournament_active)
        self.tour_active = self.tour_to_play()
        self.match_active = self.match_to_play()
        if user_input_menu_tournament_action == 1:
            self.option_add_a_round()
            self.option_menu_tournament_action()
        elif (user_input_menu_tournament_action == 2):
            self.option_play_match()
            self.option_menu_tournament_action()
        elif (user_input_menu_tournament_action == 3):
            self.option_modify_player_rank()
        else:
            self.option_menu_tournament()
            
    def option_menu_reports(self):
        # Menu Rapports
        user_input_menu_option_reports= self.view.display_menu_reports()
        if (user_input_menu_option_reports == 1):
            # 1 - Rapport détaillé sur un tournoi
            self.option_menu_reports_choose_tournament()
        elif (user_input_menu_option_reports == 2):
            # 2 - Liste des tournois
            self.view.display_tournaments_sorted_by_name(self.tournaments)
            self.view.prompt_for_continue()
            self.option_menu_reports()
        elif (user_input_menu_option_reports == 3):
            # 3 - Liste des acteurs
            self.option_reports_all_actors()
            self.view.prompt_for_continue()
            self.option_menu_reports()
        else:
            # 4 - Retour au menu principal
            self.option_menu_main()

    def option_menu_reports_choose_tournament(self):
        # Menu Choisir un tournoi
        user_input_menu_reports_all_tournament= self.view.display_menu_report_choose_tournament(self.tournaments)
        if user_input_menu_reports_all_tournament < len(self.tournaments) + 1:
            # 1:X - <Nom des tournois>
            self.tournament_active = self.tournaments[user_input_menu_reports_all_tournament-1]
            self.option_menu_reports_detailed_tournament()
        else:
            # X+1 - Retour au menu tournoi
            self.option_menu_reports()

    def option_menu_reports_detailed_tournament(self):
        # Menu Rapport détaillé sur le tournoi
        user_input_menu_tournament_reports= self.view.display_menu_tournament_reports(self.tournament_active.name)
        if (user_input_menu_tournament_reports == 1):
            # 1 - Joueurs du tournoi
            self.option_menu_reports_tournament_players()
        elif (user_input_menu_tournament_reports == 2):
            # 2 - Liste des tours du tournoi
            self.view.display_tour(self.tournament_active)
            self.view.prompt_for_continue()
            self.option_menu_reports_detailed_tournament()
        else:
            # 3 - Retour au menu des rapports
            self.option_menu_reports_choose_tournament()

    def option_menu_reports_tournament_players(self):
        # Menu Rapport joueurs du tournoi X
        user_input_menu_players_in_tournament_reports= self.view.display_menu_players_in_tournament_reports(self.tournament_active.name)
        if (user_input_menu_players_in_tournament_reports == 1):
            # 1 - Liste de tous les joueurs par ordre alphabétique
            self.view.display_player_sorted_by_name(self.tournament_active.players,self.tournament_active.name)
            self.view.prompt_for_continue()
            self.option_menu_reports_tournament_players()
        elif (user_input_menu_players_in_tournament_reports == 2):
            # 2- Liste de tous les joueurs par classement
            self.view.display_player_sorted_by_rank(self.tournament_active.players,self.tournament_active.name)
            self.view.prompt_for_continue()
            self.option_menu_reports_tournament_players()
        else:
            # 3- Retour au menu des rapports détaillés du tournoi X
            self.option_menu_reports_detailed_tournament()





  
    #######################
    # Function for options
    #######################

    def option_add_a_round(self):
        if self.tournament_active.finish == False:
            if self.tour_active == None:
                self.tournament_active.add_tour()
            else:
                self.view.display_tour_not_done()
                self.view.prompt_for_continue()
        else:
            self.view.display_tournament_done()
            self.view.prompt_for_continue()

    def option_play_match(self):
        if self.match_active is None:
            self.view.display_tour_done()
            self.view.prompt_for_continue()
        else:
            self.match_active.results_match(self.view.display_menu_add_score(self.match_active))
            self.match_active.finish = True
            if (self.last_match_in_current_in_tournament(self.match_active)):
                self.tour_active.finish = True
                self.tournament_active.finish = True
                self.tour_active.set_finish_time()
                self.tournament_active.set_date_end()
            elif self.last_match_in_current_tour(self.match_active):
                self.tour_active.finish = True
                self.tour_active.set_finish_time()
            elif self.first_match_in_current_tour(self.match_active):
                self.tour_active.set_start_time()
    def option_modify_player_rank(self):
        user_input_menu_player_rank = self.view.display_menu_modify_player_rank(self.tournament_active)
        if user_input_menu_player_rank[0] < (len(self.tournament_active.players) + 1):
            self.tournament_active.players[user_input_menu_player_rank[0]-1].ranking = user_input_menu_player_rank[1]
            self.option_modify_player_rank()
        else:
            self.option_menu_tournament_action()

    def match_to_play(self):
        if self.tour_active is None:
            return None
        for match in self.tour_active.matchs:
            if not match.finish:
                return match
        return None

    def tour_to_play(self):
        for tour in self.tournament_active.tours:
            if not tour.finish:
                return tour
        return None

    def first_match_in_current_tour(self,match:Match):
        return (self.tour_active.matchs[0]) == match

    def last_match_in_current_tour(self,match:Match):
        for index in range(len(self.tour_active.matchs)):
            if ((self.tour_active.matchs[index]) == match) and (index == len(self.tour_active.matchs)-1):
                return True
        else:
            return False

    def last_match_in_current_in_tournament(self,match:Match):
        if (len(self.tournament_active.tours) == self.tournament_active.tours_number) and self.last_match_in_current_tour(match):
            return True
        else:
            return False

    def option_reports_all_actors(self):
        actors = self.deserialized_players(self.load_serialized_from_db("player"))
        self.view.display_player_sorted_by_name(actors)

    def option_create_tournament(self):
        # list_input_infos_tournament = self.view.prompt_for_create_tournament()
        # new_tournament = Tournament(list_input_infos_tournament[0],list_input_infos_tournament[1],list_input_infos_tournament[2],list_input_infos_tournament[3])
        
        # list_info_players = self.view.prompt_for_add_players(int(list_input_infos_tournament[4]))
        # for list_info_player in list_info_players:
        #     player = Player(list_info_player[0], list_info_player[1], list_info_player[2], list_info_player[3],list_info_player[4])
        #     new_tournament.add_player(player)
        # self.tournaments.append(new_tournament)
        # self.view.terminal_clear()
        # self.view.display_player_rank_score(new_tournament)
        # self.view.prompt_for_continue()

        self.simu_create_tournament2()
        self.simu_update_ranks(self.tournaments[0].players)

    def tournaments_in_progress(self):
        tournaments_in_progress = []
        for tournament in self.tournaments:
            if tournament.finish == False:
                tournaments_in_progress.append(tournament) 
        return tournaments_in_progress

    def option_tournament_selected(self, tournament_selected):
        self.tournament_active = tournament_selected        

    ########################
    # Function for data base
    ########################

    def serialized_items(self, items):
        serialized = []
        for item in items:
            serialized.append(item.serialized())
        return serialized

    def deserialized_players(self, serialized_players):
        players = []
        for serialized_player in serialized_players:
            players.append(Player.deserialized(serialized_player))
        return players

    def deserialized_matchs(self, serialized_matchs, players: List[Player]):
        matchs = []
        for serialized_match in serialized_matchs:
            matchs.append(Match.deserialized(serialized_match, players))
        return matchs

    def deserialized_tours(self, serialized_tours, matchs: List[Match]):
        tours = []
        for serialized_tour in serialized_tours:
            tours.append(Tour.deserialized(serialized_tour, matchs))
        return tours

    def deserialized_tournaments(self, serialized_tournaments, tours: List[Tour], players: List[Player]):
        tournaments = []
        for serialized_tournament in serialized_tournaments:
            tournaments.append(Tournament.deserialized(serialized_tournament, tours, players))
        return tournaments

    def option_save_serialized_table_to_db(self, serialized_items, table_name):
        self.save_serialized_in_db(serialized_items,table_name)

    def save_serialized_in_db(self, serialized_items,table_name):
        table_items = self.db.table(table_name)
        # table_items.truncate()	# clear the table first
        table_items.insert_multiple(serialized_items)
    
        #     players = self.deserialized_players(self.load_serialized_from_db("player"))
        # matchs = self.deserialized_matchs(self.load_serialized_from_db("match"), players)
        # tours = self.deserialized_tours(self.load_serialized_from_db("tour"), matchs)
        # tournaments = self.deserialized_tournaments(self.load_serialized_from_db("tournament"), tours, players)
        
    def clear_all_tab_in_db(self):
        self.db.drop_tables()

    def load_serialized_from_db(self,table_name):
        load_table = self.db.table(table_name)
        return load_table.all()

    # def option_load_from_db(self, table_name):
    #     self.players_in_db = self.deserialized_items(self.load_serialized_from_db(table_name))
    #     self.view.terminal_clear()
    #     self.view.display_player_rank_score_2(self.players_in_db)
    #     self.view.prompt_for_continue()

    def option_load_from_db(self):
        try:
            players = self.deserialized_players(self.load_serialized_from_db("player"))
            matchs = self.deserialized_matchs(self.load_serialized_from_db("match"), players)
            tours = self.deserialized_tours(self.load_serialized_from_db("tour"), matchs)
            tournaments = self.deserialized_tournaments(self.load_serialized_from_db("tournament"), tours, players)
            self.view.display_all_information_tournament(tournaments[0])
            self.tournaments = tournaments
            self.view.display_load_from_database_done()
            self.view.prompt_for_continue()
        except IndexError:
            self.view.display_load_from_database_error()
            self.view.prompt_for_continue()

    def option_save_all_serialized_table_to_db(self):
        self.option_save_serialized_table_to_db(self.serialized_items(self.tournaments), "tournament") #To be update
        for tournament in self.tournaments:
            self.option_save_serialized_table_to_db(self.serialized_items(tournament.tours), "tour") #To be update
            self.option_save_serialized_table_to_db(self.serialized_items(tournament.players), "player") #To be update
            for tour in tournament.tours:
                self.option_save_serialized_table_to_db(self.serialized_items(tour.matchs), "match") #To be update
        self.view.display_save_to_database_done()
        self.view.prompt_for_continue()
        # players = self.deserialized_players(players_serialized)
        # matchs = self.
        # tours_serialized
        # tournaments

    ##########################
    # Function for SIMU part
    ##########################
    def simu1(self):
        self.simu_create_tournament1()
        self.display_simu()

        self.simu_add_players()
        self.display_simu()

        self.simu_update_ranks(self.tournament_simu.players)
        self.display_simu()

        for index in range(4):
            self.tournament_simu.add_tour()
            self.display_simu()
            self.simu_play_tour(self.tournament_simu.tours[index]) 
            self.tournament_simu.tours[index].finish = True
            self.display_simu()
        self.tournament_simu.set_date_end()
        self.tournament_simu = None

    def simu_create_tournament1(self):
        tournament = Tournament("Tournoi Demo 1","Paris","Bullet","Description du tounoi de demonstration 1")
        self.tournament_simu = tournament

    def simu_create_tournament2(self):
        tournament = Tournament("Tournoi Demo 2","Paris","Bullet","Description du tounoi de demonstration 1")
        tournament.add_player(Player("Tan1", "TRAN1", "04/10/1985", "M"))
        tournament.add_player(Player("Tan2", "TRAN2", "05/10/1985", "F"))
        tournament.add_player(Player("Tan5", "TRAN5", "08/10/1985", "F"))
        tournament.add_player(Player("Tan6", "TRAN6", "09/10/1985", "M"))
        tournament.add_player(Player("Tan7", "TRAN7", "10/10/1985", "M"))
        tournament.add_player(Player("Tan", "TRAN", "03/10/1985", "M"))
        tournament.add_player(Player("Tan3", "TRAN3", "06/10/1985", "M"))
        tournament.add_player(Player("Tan4", "TRAN4", "07/10/1985", "F"))
        self.tournaments.append(tournament)


    def simu_add_players(self):   
        self.tournament_simu.add_player(Player("Tan1", "TRAN1", "04/10/1985", "M"))
        self.tournament_simu.add_player(Player("Tan2", "TRAN2", "05/10/1985", "F"))
        self.tournament_simu.add_player(Player("Tan5", "TRAN5", "08/10/1985", "F"))
        self.tournament_simu.add_player(Player("Tan6", "TRAN6", "09/10/1985", "M"))
        self.tournament_simu.add_player(Player("Tan7", "TRAN7", "10/10/1985", "M"))
        self.tournament_simu.add_player(Player("Tan", "TRAN", "03/10/1985", "M"))
        self.tournament_simu.add_player(Player("Tan3", "TRAN3", "06/10/1985", "M"))
        self.tournament_simu.add_player(Player("Tan4", "TRAN4", "07/10/1985", "F"))

    def simu_update_ranks(self,players: List[Player]):
        for player in players:
            player.ranking = (random.randint(1,1000))

    def simu_play_match(self,match: Match):   
        match.results_match(random.randint(1,3))
        match.finish = True

    def simu_play_tour(self, tour:Tour):  
        tour.set_start_time()
        for match in tour.matchs:
            self.simu_play_match(match)
        tour.finish = True
        tour.set_finish_time()

    def display_simu(self):
        self.view.terminal_clear()
        self.view.display_all_information_tournament(self.tournament_simu)
        self.view.prompt_for_continue()

    def run(self):
        self.option_menu_main()

