class GameState:
    def __init__(self):
        self.players = []  # 玩家列表
        self.day_count = 0  # 游戏天数
        self.phase = "night"  # 当前阶段
        self.history = []  # 游戏历史记录