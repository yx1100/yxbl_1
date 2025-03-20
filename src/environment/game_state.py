class GameState:
    def __init__(self, players):
        self.initial_players = players  # 初始玩家列表
        self.roles = {}  # 玩家角色信息
        self.villagers = []  # 村民阵营玩家
        self.werewolves = []  # 狼人阵营玩家

        self.day_count = 0  # 游戏天数
        self.phase = "night"  # 当前阶段，可选值为"night", "day", "vote"

        self.history = []  # 游戏历史记录
        self.winner = None  # 获胜阵营，可选值"villager", "werewolf"
        self.game_is_over = False  # 游戏结束标志
