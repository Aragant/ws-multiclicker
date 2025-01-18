class Player:
    def __init__(self, username):
        self.username = username
        self.sumScore = 0
        self.clan = None
        
    def score_increment(self):
        self.sumScore += 1