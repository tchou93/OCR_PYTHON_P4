from typing import List

class Player:
    """Player."""

    def __init__(self, first_name:str, last_name:str, birthday:str, gender:str, ranking=0 ,score=0):
        """Constructeur de la classe Player"""
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.ranking = ranking
        self.score = score
        self.players_already_played : List[Player]= []

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

    def add_already_played(self, player):
        """ Ajouter le player à la liste des joueurs déjà rencontré durant le tournoi """
        self.players_already_played.append(player)

    def serialized(self, player):
        serialized_player = {
            'first_name' : player.first_name,
            'last_name' : player.last_name,
            'birthday': player.birthday,
            'gender' : player.gender,
            'ranking' : player.ranking
        }
        return serialized_player 

    def deserialized(self, serialized_player):
        first_name = serialized_player['first_name']
        last_name = serialized_player['last_name']
        birthday = serialized_player['birthday']
        gender = serialized_player['gender']
        ranking = serialized_player['ranking']
        return Player(first_name,last_name,birthday,gender,ranking)