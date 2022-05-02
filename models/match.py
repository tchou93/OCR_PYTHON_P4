from imp import cache_from_source
from .player import Player

class Match:
    """Match."""

    def __init__(self, player1, player2):
        """Has a presentation for a match."""
        self.player1: Player = player1
        self.player2: Player = player2
        self.resultplayer1 = ""
        self.resultplayer2 = ""
        self.player1.add_already_played(player2)
        self.player2.add_already_played(player1)
        
    def __str__(self):
        """Used in print."""
        if (self.resultplayer1 == "Win"):
            return f"[{self.player1.first_name} VS {self.player2.first_name} = {self.player1.first_name} Win]"
        elif (self.resultplayer1 == "Lost"):
            return f"[{self.player1.first_name} VS {self.player2.first_name} = {self.player2.first_name} Win]"
        else:
            return f"[{self.player1.first_name} VS {self.player2.first_name} = Draw]"

    def set_resultplayer1(self,resultplayer1):
        self.resultplayer1 = resultplayer1
    
    def set_resultplayer2(self,resultplayer2):
        self.resultplayer2 = resultplayer2

    def get_match(self):
        return ([self.player1,self.resultplayer1],[self.player2,self.resultplayer2])

    #Faire une fonction pour gagner, perdre, égalité
    def results_match(self,result):
        if result == 0:
            self.player1.win()
            self.player2.lost()
            self.resultplayer1 = "Win"
            self.resultplayer2 = "Lost"
        elif result == 1:
            self.player1.lost()
            self.player2.win()
            self.resultplayer1 = "Lost"
            self.resultplayer2 = "Win"
        elif result == 2:
            self.player1.draw()
            self.player2.draw()
            self.resultplayer1 = "Draw"
            self.resultplayer2 = "Draw"