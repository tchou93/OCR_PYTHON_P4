class Player:
    """Player."""

    def __init__(self, first_name, last_name, birthday, gender):
        """Has a presentation for the player."""
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.ranking = 0
        self.score = 0
        self.players_name_already_played = []

    def __str__(self):
        """Used in print."""
        return f"Nom : {self.first_name}, Prénom : {self.last_name}, Date de naissance : {self.birthday}, Genre : {self.gender}, Classement : {self.ranking} \n"

    def set_ranking(self, newrank):
        self.ranking = newrank

    def win(self):
        self.score += 1

    def lost(self):
        self.score += 0

    def draw(self):
        self.score += 0.5

    def get_score(self):
        return self.score

    def add_already_played(self, player):
        self.players_name_already_played.append(player)

