from imp import cache_from_source
from .player import Player

class Match:
    """Match."""

    def __init__(self, player1, player2):
        """Has a presentation for a match."""
        self.player1: Player = player1
        self.player2: Player = player2
        self.resultplayer1 = 0
        self.resultplayer2 = 0

    def __str__(self):
        """Used in print."""
        if (self.resultplayer1 > self.resultplayer2):
            return f"[{self.player1.first_name} VS {self.player2.first_name} = {self.player1.first_name} Win]"
        elif (self.resultplayer1 < self.resultplayer2):
            return f"[{self.player1.first_name} VS {self.player2.first_name} = {self.player2.first_name} Win]"
        else:
            return f"[{self.player1.first_name} VS {self.player2.first_name} = Draw]"

    def set_resultplayer1(self,resultplayer1):
        self.resultplayer1 = resultplayer1
    
    def set_resultplayer2(self,resultplayer2):
        self.resultplayer2 = resultplayer2

    def get_match(self):
        return ([self.player1,self.resultplayer1],[self.player2,self.resultplayer2])

    # def get_resultplayer1(self):
    #     return self.resultplayer1

    # def get_resultplayer2(self):
    #     return self.resultplayer2

    # def get_player1(self):
    #     return self.player1
        
    # def get_player2(self):
    #     return self.player2
    
    def calc_results(self):
        if (self.resultplayer1 > self.resultplayer2):
            self.player1.update_score(1)
        elif (self.resultplayer1 < self.resultplayer2):
            self.player2.update_score(1)
        else:
            self.player1.update_score(0.5)
            self.player2.update_score(0.5)