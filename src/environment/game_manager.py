class GameManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def run_phase(self):
        """根据当前阶段运行相应的处理方法"""
        current_phase = self.game_state.phase
        
        if current_phase == "night":
            self.night_phase()
        elif current_phase == "day":
            self.day_phase()
        elif current_phase == "vote":
            self.vote_phase()
            
        # 检查游戏是否结束
        if self.game_state.game_is_over:
            return self.end_game()
            
        # 推进到下一阶段
        next_phase = self.game_state.advance_phase()
        return next_phase

    def night_phase(self):
        """处理夜晚阶段"""
        print("\n==== 夜晚降临 ====")
        # 处理狼人袭击、医生救人、预言家查验等行为
        
        # 注意：这里不直接修改phase，而是等run_phase调用advance_phase

    def day_phase(self):
        """处理白天阶段"""
        print("\n==== 天亮了 ====")
        # 宣布夜晚死亡情况
        # 玩家讨论
        
        # 注意：这里不直接修改phase

    def vote_phase(self):
        """处理投票阶段"""
        print("\n==== 投票阶段 ====")
        # 收集所有玩家的投票
        # 处理投票结果
        
        # 注意：这里不直接修改phase
        
    def end_game(self):
        """处理游戏结束"""
        print("\n==== 游戏结束 ====")
        if self.game_state.winner == "werewolf":
            print("狼人阵营胜利!")
        else:
            print("村民阵营胜利!")
