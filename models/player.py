from typing import List
from uuid import uuid4

class Player:
    """Player."""

    def __init__(self, first_name:str, last_name:str, birthday:str, gender:str, ranking=0 ,score=0, players_already_played_index=None, id=None):
        """Constructeur de la classe Player"""
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.ranking = ranking
        self.score = score
        self.players_already_played_index: List[int] =  [] if players_already_played_index is None else players_already_played_index
        self.id = str(uuid4()) if id is None else id

    def __repr__(self):
        """Utiliser pour avoir une représentation avec la fontion print"""
        return f"Nom : {self.first_name}, Prénom : {self.last_name}, Date de naissance : {self.birthday}, Genre : {self.gender}, Classement : {self.ranking} \n"

    def win(self):
        """ Ajoute 1 au score si le joueur gagne un match """
        self.score += 1

    def lost(self):
        """ Ajoute 0 au score si le joueur perd un match """
        self.score += 0

    def draw(self):
        """ Ajoute 0.5 au score si le joueur fait égalité """
        self.score += 0.5

    def add_already_played_index(self, index_player):
        """ Ajouter le player à la liste des joueurs déjà rencontré durant le tournoi """
        self.players_already_played_index.append(index_player)

    def serialized(self):
        serialized_player = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthday': self.birthday,
            'gender': self.gender,
            'ranking': self.ranking,
            'score': self.score,
            'players_already_played_index': self.players_already_played_index,
            'id': self.id
        }
        return serialized_player

    @classmethod
    def deserialized(cls, serialized_player):
        first_name = serialized_player['first_name']
        last_name = serialized_player['last_name']
        birthday = serialized_player['birthday']
        gender = serialized_player['gender']
        ranking = serialized_player['ranking']
        score = serialized_player['score']
        players_already_played_index = serialized_player['players_already_played_index']
        id = serialized_player['id']
        return cls(first_name,last_name,birthday,gender,ranking,score,players_already_played_index,id)
