class BaseAgent:
    def __init__(self, player_id, role, human_or_ai="AI"):
        self.player_id = player_id
        self.role = role
        self.human_or_ai=human_or_ai