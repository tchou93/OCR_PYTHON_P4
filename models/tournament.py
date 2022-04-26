from typing import List
from player import Player
from tour import Tour
from match import Match


class Tournament:
    """Tournament."""

    def __init__(self, name, place, date, time_control, description ):
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
        return f"nom du tournoi : {self.name}, Lieu : {self.place}, Les joueurs : {self.players}, contrôle de temps :{self.time_control}, Description :{self.description}"

    def add_player(self, player):
        self.players.add(player)

    def add_tour(self, tour):
        number_of_tour_players = 0
        index = 0
        if (len(self.tours) == 0):
            number_of_tour_players = len(self.players)
            while index < number_of_tour_players:
                Match(self.players[index],self.players[index+1])
                index +=2 
        else:
            number_of_tour_players = self.tours[len(self.tours)-1]
            self.tours


        # self.tours.add(tour)