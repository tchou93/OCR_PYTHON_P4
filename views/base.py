"""Base view."""

class View:
    """Chess game view."""

    def prompt_for_player(self, number):
        """Prompt for a name."""
        info_player = {}
        print(f"Taper les informations pour le joueur {number} : ")
        info_player["fist_name"] = input("tapez le fist_name : ")
        info_player["last_name"] = input("tapez le last_name : ")
        info_player["birthday"] = input("tapez le birthday : ")
        info_player["gender"] = input("tapez le gender : ")
        return info_player

    def prompt_for_tournament(self):
        """Prompt for a tournament."""
        info_tournament = {}
        print(f"Taper les informations pour le tournoi: ")
        info_tournament["name"] = input("tapez le name : ")
        info_tournament["place"] = input("tapez la place : ")
        info_tournament["date"] = input("tapez la date: ")
        info_tournament["time_control"] = input("tapez le time_control: ")
        info_tournament["description"] = input("tapez la description: ")
        return info_tournament 

    def prompt_for_result_match(self, player1, player2):
        print(f"Entrer le résultat du match entre le joueur {player1} et le joueur {player2}  ")
        result = input(f"Le joueur {player1} ")

    def show_ranking(self):
        pass

    def show_games(self):
        pass

    def show_reports(self):
        pass

    def prompt_for_data_save(self):
        pass

    def prompt_for_data_load(self):
        pass
