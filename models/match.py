from .player import Player

class Match:
    """Match."""

    def __init__(self, player1, player2):
        """Has a presentation for a match."""
        self.player1 = player1
        self.player2 = player2
        self.resultplayer1 = 0
        self.resultplayer2 = 0

    def __str__(self):
        """Used in print."""
        return f"Matchs entre : {self.player1} et {self.player2}, Résultat: {self.resultplayer1} contre {self.resultplayer2}"

    def add_resultplayer1(self,resultplayer1):
        self.resultplayer1 = resultplayer1
    
    def add_resultplayer2(self,resultplayer2):
        self.resultplayer2 = resultplayer2

    def get_match(self):
        return ([self.player1,self.resultplayer1],[self.player2,self.resultplayer2])

    def get_resultplayer1(self):
        return self.resultplayer1

    def get_resultplayer2(self):
        return self.resultplayer2

    def get_player1(self):
        return self.player1
        
    def get_player2(self):
        return self.player2

    def set_resultplayer1(self,result):
        self.resultplayer1 = result

    def set_resultplayer2(self,result):
        self.resultplayer2 = result