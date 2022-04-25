from .player import Player


class Tournament:
    """Tournament."""

    def __init__(self, name, place, date, rounds_number,rounds,  players, time_control, description ):
        """Has a presentation for the tournament."""
        self.name = name
        self.place = place
        self.date = date
        self.rounds_number = rounds_number
        self.rounds = rounds
        self.tours = 4
        self.players = players
        self.time_control = time_control
        self.description = description 

        
    def __str__(self):
        """Used in print."""
        return f"nom du tournoi : {self.name}, Lieu : {self.place}, Les joueurs : {self.players}, contrôle de temps :{self.time_control}, Description :{self.description}"