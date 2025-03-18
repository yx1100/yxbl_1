from src.environment.game_state import GameState


class WerewolfEnv:
    def __init__(self, player_num, role_config):
        # 初始化游戏参数
        self.player_num = player_num
        self.role_config = role_config
        # 初始化游戏状态
        self.game_state = GameState(self.players)

    def reset(self):
        """重置游戏环境"""
        # 调用GameState的reset方法
        self.game_state.reset()

        # 返回初始观察状态
        return self._get_observation()

    def step(self, action):
        # 执行动作并返回(下一状态, 奖励, 是否结束, 信息)
        pass

    def render(self):
        # 显示当前游戏状态
        pass
