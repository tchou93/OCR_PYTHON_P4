"""Define the main controller."""
from typing import List
from models.player import Player
from models.tour import Tour
from models.tournament import Tournament
import random
import os

class Controller:
    """Main controller."""

    def __init__(self,view):
        self.view  = view
        self.tournaments:List[Tournament] = []

    def create_tournament(self):
        print("Bienvenue à la création du tournoi: ")
        print("Merci de rentrer les informations: ")
        infos_tournament = [
            "Nom du tournoi : ",
            "Lieu : ",
            "Date (JJ/MM/AA) : ",
            "Contrôle du temps (Bullet/Blitz/Rapid) : ",
            "Description : "
        ]
        list_input_infos_tournament = []
        for info_tournament in infos_tournament:
            list_input_infos_tournament.append(input(info_tournament))
        print(list_input_infos_tournament)
        tournament = Tournament(list_input_infos_tournament[0],list_input_infos_tournament[1],list_input_infos_tournament[2],list_input_infos_tournament[3],list_input_infos_tournament[4])
        self.tournaments.append(tournament)
        print("Le tournoi a été crée : ")
        print(str(tournament))

    def add_players(self):
        while 1:
            os.system("cls") 
            print("-------------------------------------------------------------")
            if (len(self.tournaments[0].players) == 0):
                print("Pas encore de joueur")
            else:
                print("Liste des joueurs :")
                for player in self.tournaments[0].players:
                    print(player)
            print("[1] Ajouter un joueur")
            print("[2] Quittez")
            print("-------------------------------------------------------------")    
            user_input = input("Choix: ")
            if int(user_input) == 1:
                infos_player = [
                "fist_name : ",
                "last_name : ",
                "birthday (JJ/MM/AA) : ",
                "Sexe (M/F) : "
                ]
                list_input_infos_player = []
                for info_player in infos_player:
                    list_input_infos_player.append(input(info_player))
                player = Player(list_input_infos_player[0], list_input_infos_player[1], list_input_infos_player[2], list_input_infos_player[3])
                self.tournaments[0].add_player(player)
            elif int(user_input) == 2:
                break

    def start_tournament(self):
        if len(self.tournaments) == 0:
            self.create_tournament_simu()
            tournament = self.tournaments[0]
        else:
            tournament = self.tournaments[0]
        if tournament.finished != True:
            os.system("cls")
            print(f"Bienvenue sur le tournoi {tournament.name} :")
            for number_of_tour in range(4):
                print(f"[1] Commencer un nouveau Round")
                print(f"[2] Mettre à jour les classements")
                print(f"[3] Afficher le Round")
                user_input = input()
                if int(user_input) == 3:
                    print(tournament.tours[len(tournament.tours)-1])
                elif int(user_input) == 2:
                    while 1:
                        index = 1
                        for player in tournament.players:
                            print(f"{index} : {player.first_name} {player.last_name} Classement: {player.ranking}")
                            index += 1
                        print("100 : Quittez")
                        user_input_name_player = input("Choisir le joueur ou quitter: ")
                        if(int(user_input_name_player) == 100):
                            break
                        user_input_rank_player = input("Choisir le nouveau rang: ")
                        tournament.players[int(user_input_name_player)-1].ranking = int(user_input_rank_player)
                    print(f"Mise à jour terminé")
                elif int(user_input) == 1:
                    os.system("cls")
                    print(f"Le Round {number_of_tour+1} commence ...")
                    tournament.add_tour()
                    print(f"Le Round {number_of_tour+1} est terminé ...")  
                    self.update_players()
            print(f"Merci le tournoi est terminé")
            tournament.finished = True
        else:
            while 1:
                print(f"Le tournoi {tournament.name} est déjà terminé!")
                print(f"[1] Afficher les Rounds")
                print(f"[2] Quittez")
                user_input = input()
                if int(user_input) == 1:
                    os.system("cls")
                    tournament.print_tournament()
                elif int(user_input) == 2:
                    break

    def update_players(self):
        tournament = self.tournaments[0]
        for match in tournament.tours[len(tournament.tours)-1].matchs:
            match.results_match(random.randint(0,2))

    def tournament_simu(self):
        #Test for tournament without View
        self.create_tournament_simu()
        tournament1 = self.tournaments[0]

        #Set some random ranks
        for player in tournament1.players:
            player.set_ranking(random.randint(1,10000))

        #Create all the tours and simulate the winners of each match]
        print(f"Bienvenue sur le tournoi {tournament1.name} :")
        for number_of_tour in range(4):
            print(f"Le Round {number_of_tour+1} commence :")
            tournament1.add_tour()
            for match in tournament1.tours[len(tournament1.tours)-1].matchs:
                match.results_match(random.randint(0,2))
            print(tournament1)
            print(f"Le Round {number_of_tour+1} est terminé :")  
            print(f"[1] Mettre à jour les classements")
            print(f"[2] Continuer avec le prochain Round")
            user_input = input()
            if int(user_input) == 1:
                while 1:
                    index = 1
                    for player in tournament1.players:
                        print(f"{index} : {player.first_name} {player.last_name} Classement: {player.ranking}")
                        index += 1
                    print("100 : Quittez")
                    user_input_name_player = input("Choisir le joueur ou quitter: ")
                    if(int(user_input_name_player) == 100):
                        break
                    user_input_rank_player = input("Choisir le nouveau rang: ")
                    tournament1.players[int(user_input_name_player)-1].ranking = int(user_input_rank_player)
                print(f"Mise à jour terminé")
            elif int(user_input) == 2:
                continue
        
        print(f"Merci le tournoi est terminé")

    def create_tournament_simu(self):
        tournament = Tournament("Tournoi1","Sevran","28/04/2022","control1","description 1")
        player1 = Player("Tan", "TRAN", "03/10/1985", "M")
        player2 = Player("Tan1", "TRAN1", "04/10/1985", "A")
        player3 = Player("Tan2", "TRAN2", "05/10/1985", "B")
        player4 = Player("Tan3", "TRAN3", "06/10/1985", "C")
        player5 = Player("Tan4", "TRAN4", "07/10/1985", "D")
        player6 = Player("Tan5", "TRAN5", "08/10/1985", "E")
        player7 = Player("Tan6", "TRAN6", "09/10/1985", "F")
        player8 = Player("Tan7", "TRAN7", "10/10/1985", "G")
        tournament.add_player(player1)
        tournament.add_player(player4)
        tournament.add_player(player8)
        tournament.add_player(player2)
        tournament.add_player(player3)
        tournament.add_player(player5)
        tournament.add_player(player6)
        tournament.add_player(player7)
        self.tournaments.append(tournament)

    def menu(self):
        choix_min = 1
        choix_exit = 100
        while 1:
           os.system("cls") 
           print("-----------------------------------------------------------------")
           print("Bienvenue dans le gestionnaire de tournoi :")
           print(f"{choix_min}: Simulation d'un tournoi")
           print(f"{choix_min+1}: Step1: Création d'un tournoi ")
           print(f"{choix_min+2}: Step2: Ajout de joueurs")
           print(f"{choix_min+3}: Step3: Commencer le tournoi")
           print(f"{choix_exit}: Quittez.")
           print("------------------------------------------------------------------")
           choix = input("Veuillez choisir l'option voulu: ")
           choix = int(choix)
           if choix == (choix_exit):
                break
           elif choix==choix_min:
                os.system("cls")
                print("-------------------------------------------------------------")
                print("Simulation d'un tournoi avec deux tours")
                print("-------------------------------------------------------------")  
                self.tournament_simu()
           elif choix==choix_min+1:
                os.system("cls")
                print("-----------------------------------------------------")
                print("Création d'un tournoi")
                print("-----------------------------------------------------")
                self.create_tournament()
           elif choix==choix_min+2:
                os.system("cls")
                print("-----------------------------------------------------")
                print("Ajout d'un joueur")
                print("-----------------------------------------------------")
                self.add_players()
           elif choix==choix_min+3:
                os.system("cls")
                print("-----------------------------------------------------")
                print("Jouer un round")
                print("-----------------------------------------------------")
                self.start_tournament()
    