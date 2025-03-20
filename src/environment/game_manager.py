import random
from agents.llm_agent import LLMAgent
from agents.human_agent import HumanAgent


class GameManager:
    def __init__(self, player_count=4):
        self.player_count = player_count

    def setup_game(self):
        # 设置游戏环境和玩家
        # 计算村民数量
        villagers_count = self.player_count - 4  # 1 doctor, 2 werewolves, 1 seer
        if villagers_count < 0:
            raise ValueError(
                "Player count must be at least 4 to have all required roles")

        # 创建角色列表
        player_role_list = ['doctor'] + ['werewolf'] * \
            2 + ['seer'] + ['villager'] * villagers_count
        # 随机打乱角色列表
        random.shuffle(player_role_list)

        # 创建玩家ID列表,格式为"ID_X"。
        player_id_list = [f"ID_{i}" for i in range(1, self.player_count + 1)]

        # 随机选择一个ID作为人类玩家
        human_player_id = random.choice(player_id_list)

        # 创建玩家代理
        agents = []
        for player_id, role in zip(player_id_list, player_role_list):
            # 根据角色确定阵营
            faction = "WEREWOLVES" if role == "werewolf" else "VILLAGERS"

            # 根据ID创建人类或AI代理
            if player_id == human_player_id:
                # agent = HumanAgent(player_id=player_id, role=role, faction=faction)
                agent = LLMAgent(player_id=player_id,
                                 role=role, faction=faction)
            else:
                agent = LLMAgent(player_id=player_id,
                                 role=role, faction=faction)
            agents.append(agent)

        return player_role_list, player_id_list, human_player_id, agents

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
