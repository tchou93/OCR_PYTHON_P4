"""Define the main controller."""
from operator import truediv
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

    #####################
    # Function for menu
    #####################
    def option_menu_main(self):
        user_input_menu_main = self.view.display_menu_main()
        if (user_input_menu_main == 1):
            self.option_tournament()
        elif (user_input_menu_main == 2):
            self.option_menu_main() #TBD
        elif (user_input_menu_main == 3):
            self.option_menu_main() #TBD
        elif (user_input_menu_main == 4):
            self.option_reports()
        elif (user_input_menu_main == 5):
            self.simu1()
            self.option_menu_main()

    def option_save_players_in_db(self):
        self.save_serialized_players_in_db(self.serialized_players_in_tournament(self.tournaments[0]))
        self.display_save_in_database_done()
        self.prompt_for_continue()

    def option_tournament(self):
        user_input_menu_option_tournament= self.view.display_menu_tournament()
        if (user_input_menu_option_tournament == 1):
            self.option_create_tournament()
            self.option_tournament()
        elif (user_input_menu_option_tournament == 2):
            self.option_choose_tournament()
        else:
            self.option_menu_main()

    def option_reports(self):
        user_input_menu_option_reports= self.view.display_menu_reports()
        if (user_input_menu_option_reports == 1):
            self.option_reports_detailed_tournament()
        elif (user_input_menu_option_reports == 2):
            self.option_reports() #TBD
        else:
            self.option_menu_main()

    def option_reports_detailed_tournament(self):
        user_input_menu_tournament_reports= self.view.display_menu_tournament_reports()
        if (user_input_menu_tournament_reports == 1):
            self.option_reports_detailed_tournament() #TBD
        elif (user_input_menu_tournament_reports == 2):
            self.option_reports_detailed_tournament() #TBD
        elif (user_input_menu_tournament_reports == 3):
            self.option_reports_detailed_tournament() #TBD
        else:
            self.option_reports()
            
    def option_choose_tournament(self):
        tournaments_in_progress = self.tournaments_in_progress()
        user_input_menu_option_tournament = self.view.display_menu_choose_tournament(tournaments_in_progress)
        if user_input_menu_option_tournament < len(tournaments_in_progress) + 1:
            self.option_tournament_selected(tournaments_in_progress[user_input_menu_option_tournament-1])
            self.option_tournament_action()
        else:
            self.option_tournament()

    def option_tournament_action(self):
        user_input_menu_tournament_action = self.view.display_menu_tournament_action(self.tournament_active)
        self.view.display_all_information_tournament(self.tournament_active)
        if user_input_menu_tournament_action == 1:
            self.option_add_a_round()
            self.option_tournament_action()
        elif (user_input_menu_tournament_action == 2):
            self.option_play_match()
            self.option_tournament_action()
        elif (user_input_menu_tournament_action == 3):
            self.option_modify_player_rank()
        else:
            self.option_tournament()

    def option_modify_player_rank(self):
        user_input_menu_player_rank = self.view.display_menu_modify_player_rank(self.tournament_active)
        if user_input_menu_player_rank[0] < (len(self.tournament_active.players) + 1):
            self.tournament_active.players[user_input_menu_player_rank[0]-1].ranking = user_input_menu_player_rank[1]
            self.option_modify_player_rank()
        else:
            self.option_tournament_action()

    def option_add_a_round(self):
        if self.tournament_active.finish == False:
            new_tour_active=self.tournament_active.add_tour()
            if self.tour_active == new_tour_active:
                self.view.display_tour_not_done()
                self.view.prompt_for_continue()
            else:
                self.tour_active = new_tour_active
            # self.simu_play_tour(self.tournament_active.tours[len(self.tournament_active.tours)-1]) #TBD
        else:
            self.view.display_tournament_done()
            self.view.prompt_for_continue()

    def option_play_match(self):
        match_to_play = self.match_to_play()
        if match_to_play is None:
            self.view.display_tour_done()
            self.view.prompt_for_continue()
        else:
            match_to_play.results_match(self.view.display_menu_add_score(match_to_play))
            match_to_play.finish = True
            if (self.last_match_in_current_in_tournament(match_to_play)):
                self.tour_active.finish = True
                self.tournament_active.finish = True
                self.tour_active.set_finish_time()
                self.tournament_active.set_date_end()
            elif self.last_match_in_current_tour(match_to_play):
                self.tour_active.finish = True
                self.tour_active.set_finish_time()
            elif self.first_match_in_current_tour(match_to_play):
                self.tour_active.set_start_time()
      
  
    def match_to_play(self):
        for match in self.tour_active.matchs:
            if not match.finish:
                return match
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
    #######################
    # Function for options
    #######################

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
        self.simu_add_players2()
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

    def serialized_players_in_tournament(self, tournament : Tournament):
        serialized_players = []
        players = tournament.players
        for player in players:
            serialized_players.append(player.serialized)
        return serialized_players

    def deserialized_players(self, serialized_players) -> List[Player]:
        players = []
        for serialized_player in serialized_players:
            players.append(Player.deserialized(serialized_player))
        return players

    def save_serialized_players_in_db(self, serialized_players):
        db = TinyDB('db_chess_tournament.json')
        players_table = db.table('players')
        players_table.truncate()	# clear the table first
        players_table.insert_multiple(serialized_players)

    def load_serialized_players_from_db(self):
        db = TinyDB('db_chess_tournament.json')
        players_table = db.table('players')
        return players_table.all()

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
        tournament = Tournament("Tournoi Démo 1","Paris","Bullet","Description du tounoi de démonstration 1")
        self.tournament_simu = tournament

    def simu_create_tournament2(self):
        tournament = Tournament("Tournoi Démo 2","Paris","Bullet","Description du tounoi de démonstration 1")
        self.tournaments.append(tournament)

    def simu_add_players2(self): 
        self.tournaments[0].add_player(Player("Tan1", "TRAN1", "04/10/1985", "M"))
        self.tournaments[0].add_player(Player("Tan2", "TRAN2", "05/10/1985", "F"))
        self.tournaments[0].add_player(Player("Tan5", "TRAN5", "08/10/1985", "F"))
        self.tournaments[0].add_player(Player("Tan6", "TRAN6", "09/10/1985", "M"))
        self.tournaments[0].add_player(Player("Tan7", "TRAN7", "10/10/1985", "M"))
        self.tournaments[0].add_player(Player("Tan", "TRAN", "03/10/1985", "M"))
        self.tournaments[0].add_player(Player("Tan3", "TRAN3", "06/10/1985", "M"))
        self.tournaments[0].add_player(Player("Tan4", "TRAN4", "07/10/1985", "F"))

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

