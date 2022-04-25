class Player:
    """Player."""

    def __init__(self, fist_name, last_name, birthday, gender, ranking):
        """Has a presentation for the player."""
        self.fist_name = fist_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender
        self.ranking = ranking

    def __str__(self):
        """Used in print."""
        return f"nom : {self.fist_name}, prenom : {self.last_name}, Date de naissance : {self.birthday}, Genre :{self.gender}, Classement :{self.ranking}"