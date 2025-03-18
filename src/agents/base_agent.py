class BaseAgent:
    def __init__(self, player_id, role, faction):
        self.player_id = player_id
        self.role = role
        self.faction = faction
        self.is_alive = True
        
    def observe(self, game_state):
        # 观察游戏状态
        pass
        
    def act(self, valid_actions):
        # 做出决策
        pass