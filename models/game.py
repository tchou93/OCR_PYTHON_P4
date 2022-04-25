from .player import Player

class Game:
    """Game."""

    def __init__(self, player1, player2, resultplayer1, resultplayer2):
        """Has a presentation for a game."""
        self.player1
        self.player2
        self.resultplayer1
        self.resultplayer2

    def __str__(self):
        """Used in print."""
        return f"Matchs entre : {self.player1} et {self.player2}, Résultat: {self.resultplayer1} contre {self.resultplayer2}"

    def get_game(self):
        return ([self.player1,self.resultplayer1],[self.player2,self.resultplayer2])
