from .player import Player
from typing import List
from uuid import uuid4

class Match:
    """Match."""

    def __init__(self, player1: Player, player2: Player, resultplayer1 = "-", resultplayer2 = "-", finish = False, id=None):
        """Has a presentation for a match."""
        self.player1 = player1
        self.player2 = player2
        self.resultplayer1 = resultplayer1
        self.resultplayer2 = resultplayer2
        self.finish = finish
        self.id = str(uuid4()) if id is None else id
        
    def __repr__(self):
        """Used in print."""
        return f"[{self.player1.first_name} {self.player1.last_name},{self.resultplayer1}],[{self.player2.first_name} {self.player2.last_name},{self.resultplayer2}]"

    def get_match(self):
        return ([self.player1,self.resultplayer1],[self.player2,self.resultplayer2])

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

    def serialized(self):
        serialized_match = {
            'player1_id' : self.player1.id,
            'player2_id' : self.player2.id,
            'resultplayer1' : self.resultplayer1,
            'resultplayer2' : self.resultplayer2,
            'finish' : self.finish,
            'id' : self.id
        }
        return serialized_match

    def deserialized(serialized_match, players: List[Player]):
        for player in players:
            if player.id == serialized_match['player1_id']:
                player1 = player
            elif player.id == serialized_match['player2_id']:
                player2 = player
        resultplayer1 = serialized_match['resultplayer1']
        resultplayer2 = serialized_match['resultplayer2']
        finish = serialized_match['finish']
        id = serialized_match['id']
        return Match(
            player1,
            player2,
            resultplayer1,
            resultplayer2,
            finish,
            id
            )


    # def serialized(self):
    #     serialized_player = {
    #         'first_name' : self.first_name,
    #         'last_name' : self.last_name,
    #         'birthday': self.birthday,
    #         'gender' : self.gender,
    #         'ranking' : self.ranking
    #     }
    #     return serialized_player 

    # def deserialized(serialized_player):
    #     first_name = serialized_player['first_name']
    #     last_name = serialized_player['last_name']
    #     birthday = serialized_player['birthday']
    #     gender = serialized_player['gender']
    #     ranking = serialized_player['ranking']
    #     return Player(first_name,last_name,birthday,gender,ranking)