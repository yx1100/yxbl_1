class GameState:
    def __init__(self):
        self.alive_players = []
        self.role_distribution = {}
        self.vote_history = []
        self.public_information = {}
        self.private_information = {}