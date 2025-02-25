class WerewolfGameEnv:
    def __init__(self, num_players, roles_config):
        self.state = GameState()
        self.players = []
        self.current_phase = None
        
    def reset(self):
        """重置游戏环境"""
        pass
        
    def step(self, action):
        """执行动作并返回新状态"""
        return next_state, reward, done, info
        
    def get_valid_actions(self, player_id):
        """获取当前玩家可执行的合法动作"""
        pass