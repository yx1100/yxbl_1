class BaseAgent:
    def __init__(self, player_id, role):
        self.player_id = player_id
        self.role = role
        
    def select_action(self, state, valid_actions):
        """选择行动"""
        raise NotImplementedError
        
    def update_policy(self, state, action, reward, next_state):
        """更新策略"""
        raise NotImplementedError