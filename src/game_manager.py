class GameManager:
    def __init__(self, num_players, role_config):
        self.env = WerewolfGameEnv(num_players, role_config)
        self.agents = []
        
    def run_game(self):
        """运行完整的游戏流程"""
        pass
        
    def run_phase(self, phase):
        """运行特定游戏阶段"""
        pass