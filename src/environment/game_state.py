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

    def advance_phase(self):
        """推进游戏阶段：夜晚 -> 白天 -> 投票 -> 夜晚"""
        if self.phase == "night":
            self.phase = "day"
        elif self.phase == "day":
            self.phase = "vote"
        elif self.phase == "vote":
            self.phase = "night"

            self.day_count += 1  # 进入新的一天

        # 记录阶段变更
        self.history.append({
            "type": "phase_change",
            "day": self.day_count,
            "phase": self.phase
        })

        return self.phase

    def get_player_by_id(self, player_id):
        """通过ID获取玩家对象"""
        for player in self.initial_players:
            if player.player_id == player_id:
                return player
        # 只有循环结束后仍未找到，才打印消息并返回None
        print("Player not found")
        return None

    def get_alive_players(self):
        """获取所有存活玩家"""
        return [player for player in self.initial_players if player.is_alive]

    def kill_player(self, player_id, reason="unknown"):
        """处理玩家死亡"""
        player = self.get_player_by_id(player_id)
        if player and player.is_alive:
            player.is_alive = False

            # 记录死亡事件
            self.history.append({
                "type": "death",
                "day": self.day_count,
                "phase": self.phase,
                "player_id": player_id,
                "role": player.player_role,
                "faction": player.player_faction,
                "reason": reason
            })

            # 检查游戏是否结束
            self.check_game_over()
            print(f"被杀死的玩家是：{player}")
        else:
            print("Player not found")

    def check_game_over(self):
        """检查游戏是否结束"""
        alive_players = self.get_alive_players()

        # 计算存活的狼人和村民数量
        self.werewolves = [
            p for p in alive_players if p.player_faction == "WEREWOLVES"]
        self.villagers = [
            p for p in alive_players if p.player_faction == "VILLAGERS"]

        # 判断游戏结束条件
        if len(self.werewolves) == 0:
            # 狼人全部死亡，好人胜利
            self.game_is_over = True
            self.winner = "VILLAGERS"
        elif len(self.werewolves) >= len(self.villagers):
            # 狼人数量大于等于村民，狼人胜利
            self.game_is_over = True
            self.winner = "WEREWOLVES"
        else:
            self.game_is_over = False
            self.winner = None

        if self.game_is_over:
            self.record_event("game_over", {"winner": self.winner})

        return self.game_is_over

    def get_winners(self):
        """获取胜利的阵营和玩家"""
        if not self.game_is_over:
            print("游戏还未结束...")
            return None

        winning_players = [
            p for p in self.initial_players if p.player_faction == self.winner]
        return {
            "faction": self.winner,
            "players": winning_players
        }

    def reset(self):
        """重置游戏状态"""
        self.day_count = 0
        self.phase = "night"
        self.history = []
        self.winner = None
        self.game_is_over = False
        
        # 重置玩家存活状态
        for player in self.initial_players:
            player.is_alive = True
        
        # 重新计算阵营
        self.villagers = [p for p in self.initial_players if p.player_faction == "villager"]
        self.werewolves = [p for p in self.initial_players if p.player_faction == "werewolf"]

    def serialize(self):
        """将游戏状态序列化为字典"""
        return {
            "day_count": self.day_count,
            "phase": self.phase,
            "history": self.history,
            "is_over": self.is_over,
            "winner": getattr(self, "winner", None),
            "players": [
                {
                    "player_id": p.player_id,
                    "role_type": p.role.role_type,
                    "is_alive": p.is_alive
                }
                for p in self.players
            ]
        }
