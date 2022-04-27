from typing import List
from models.player import Player
from models.tour import Tour
from models.match import Match


class Tournament:
    """Tournament."""

    def __init__(self, name, place, date, time_control, description):
        """Has a presentation for the tournament."""
        self.name = name
        self.place = place
        self.date = date
        self.tours_number = 4
        self.tours: List[Tour] = []
        self.players: List[Player] = []
        self.time_control = time_control
        self.description = description 

        
    def __str__(self):
        """Used in print."""
        description_tournament = f"nom du tournoi : {self.name}, Lieu : {self.place}, Voici les joueurs : \n"
        num_player=1
        for player in self.players:
            description_tournament += f"joueur {num_player} :\n" 
            description_tournament += str(player)
            num_player += 1 
        description_tournament += f"\n contrôle de temps : {self.time_control}, Description : {self.description}"
        return description_tournament

    def add_player(self, player):
        self.players.append(player)

    def add_tour(self):
        tour = Tour(f"Round {len(self.tours)+1}")
        number_of_players_in_tour = 0
        index = 0
        if (len(self.tours) == 0):
            number_of_players_in_tour = len(self.players)
            while index < number_of_players_in_tour:
                tour.add_match(Match(self.players[index],self.players[index+1]))
                index +=2 
        else:
            player_wins=[]
            for match in tour.matchs[len(tour.matchs)-1]:
                if match.get_resultplayer1 > match.get_resultplayer2:
                    player_wins.add(match.get_player1)
                else:
                    player_wins.add(match.get_player2)
            number_of_players_in_tour = len(player_wins)
            while index < number_of_players_in_tour:
                tour.add_match(Match(player_wins[index],player_wins[index+1]))
                index +=2 
        (self.tours).add(tour)