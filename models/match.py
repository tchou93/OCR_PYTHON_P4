from imp import cache_from_source
from .player import Player

class Match:
    """Match."""

    def __init__(self, player1: Player, player2: Player):
        """Has a presentation for a match."""
        self.player1 = player1
        self.player2 = player2
        self.player1.add_already_played(player2)
        self.player2.add_already_played(player1)
        self.resultplayer1 = "-"
        self.resultplayer2 = "-"
        self.finish = False
        
    def __repr__(self):
        """Used in print."""
        return f"[{self.player1.first_name} {self.player1.last_name},{self.resultplayer1}],[{self.player2.first_name} {self.player2.last_name},{self.resultplayer2}]"

    def results_match(self,result):
        """
            Selon le résultat du match rentré en paramètre, la fonction met à jour le score
            de chaque joueur et rempli leurs champs de résultat.
        """
        if result == 1:
            self.player1.win()
            self.player2.lost()
            self.resultplayer1 = "Win"
            self.resultplayer2 = "Lost"
        elif result == 2:
            self.player1.lost()
            self.player2.win()
            self.resultplayer1 = "Lost"
            self.resultplayer2 = "Win"
        elif result == 3:
            self.player1.draw()
            self.player2.draw()
            self.resultplayer1 = "Draw"
            self.resultplayer2 = "Draw"
        self.finish = True