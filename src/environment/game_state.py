import random
from src.utils.config import PLAYER_NUMS
from src.utils.game_enum import GameFaction, GameRole, GamePhase
from src.agents.llm_agent import LLMAgent
from src.agents.human_agent import HumanAgent


class GameState:
    """
    游戏状态类：管理狼人杀游戏的所有状态信息，包括玩家、阵营、游戏阶段等
    """

    def __init__(self):
        """
        初始化游戏状态
        :param players: 游戏玩家列表
        """

        players = self._set_players_agent()
        self.initial_players = players.copy()  # 初始玩家列表（使用复制避免引用问题）
        self.alive_players = players.copy()  # 存活玩家列表（初始时与初始玩家相同）

        self.current_day_count = 1  # 游戏天数，从第1天开始
        # 当前游戏阶段，可选值为"NIGHT"(夜晚), "DAY"(白天), "VOTE"(投票)
        self.phase = GamePhase.NIGHT

        self.winner = None  # 获胜阵营，可选值"VILLAGER"(村民), "WEREWOLF"(狼人)
        self.game_is_over = False  # 游戏结束标志

    def _set_players_agent(self, players_count=PLAYER_NUMS):
        # 设置游戏环境和玩家
        # 计算村民数量
        villagers_count = players_count - 4  # 1 doctor, 2 werewolves, 1 seer
        if villagers_count < 0:
            raise ValueError(
                "Player count must be at least 4 to have all required roles")

        # 创建角色列表
        player_role_list = [GameRole.DOCTOR] + [GameRole.WEREWOLF] * \
            2 + [GameRole.SEER] + [GameRole.VILLAGER] * villagers_count
        # 随机打乱角色列表
        random.shuffle(player_role_list)

        # 创建玩家ID列表,格式为"ID_X"。
        player_id_list = [f"ID_{i}" for i in range(1, players_count + 1)]

        # 随机选择一个ID作为人类玩家
        human_player_id = random.choice(player_id_list)

        # 创建玩家代理
        agents = []
        for player_id, role in zip(player_id_list, player_role_list):
            # 根据角色确定阵营
            faction = GameFaction.WEREWOLVES if role == GameRole.WEREWOLF else GameFaction.VILLAGERS

            # 根据ID创建人类或AI代理
            if player_id == human_player_id:
                # agent = HumanAgent(player_id=player_id, role=role, human_or_ai='Human')
                agent = LLMAgent(player_id=player_id, role=role)
            else:
                agent = LLMAgent(player_id=player_id, role=role)
            agents.append(agent)

        return agents

    def get_alive_players(self):
        """
        获取存活玩家列表
        :return: 存活玩家列表
        """
        return self.alive_players

# # test
# agents = GameState()._set_players_agent()
# print(agents)
