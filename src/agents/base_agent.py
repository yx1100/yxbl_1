from src.utils.game_enum import GameRole, GameFaction

class BaseAgent:
    def __init__(self, player_id, role, human_or_ai="AI"):
        self.player_id = player_id
        self.role = role
        self.faction = GameFaction.VILLAGERS if role in [GameRole.DOCTOR, GameRole.SEER, GameRole.VILLAGER] else GameFaction.WEREWOLVES
        self.human_or_ai=human_or_ai