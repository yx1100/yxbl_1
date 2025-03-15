class BaseAgent:
    def __init__(self, player_id, role):
        self.player_id = player_id
        self.role = role
        
    def observe(self, game_state):
        # 观察游戏状态
        
    def act(self, valid_actions):
        # 做出决策
        pass