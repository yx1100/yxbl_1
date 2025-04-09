import random
from src.utils.config import PLAYER_NUMS
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
        self.roles = []  # 所有玩家的角色信息列表
        self.alive_roles = []  # 存活玩家的角色信息列表
        self.alive_players_id = []  # 存活玩家的ID列表
        self.villagers_players = []  # 村民阵营玩家列表
        self.werewolves_players = []  # 狼人阵营玩家列表

        # 遍历所有玩家，记录角色信息并按阵营分类
        for player in players:
            self.roles.append(player.role)
            if player.faction == 'VILLAGERS':
                self.villagers_players.append(player)
            elif player.faction == 'WEREWOLVES':
                self.werewolves_players.append(player)
            else:
                raise ValueError(
                    f"Invalid faction: {player.faction} for player {player.name if hasattr(player, 'name') else player}")

        self.day_count = 1  # 游戏天数，从第1天开始
        self.phase = "NIGHT"  # 当前游戏阶段，可选值为"NIGHT"(夜晚), "DAY"(白天), "VOTE"(投票)

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
        player_role_list = ['doctor'] + ['werewolf'] * \
            2 + ['seer'] + ['villager'] * villagers_count
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
            faction = "WEREWOLVES" if role == "werewolf" else "VILLAGERS"

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
        获取当前存活玩家列表
        :return: 存活玩家列表
        注意：此方法会更新self.alive_players属性
        """
        alive_players = []
        for player in self.alive_players:
            if player.is_alive:
                alive_players.append(player)
        self.alive_players = alive_players  # 更新存活玩家列表
        return self.alive_players

    def get_players_role(self):
        """
        获取所有玩家角色信息
        :return: 角色信息列表
        """
        return self.roles

    def get_alive_players_role(self):
        """
        获取存活玩家角色信息
        :return: 存活玩家角色信息列表
        """
        alive_roles = []
        for player in self.alive_players:
            alive_roles.append(player.role)
        self.alive_roles = alive_roles
        return self.alive_roles

    def get_alive_players_id(self):
        """
        获取存活玩家角色信息
        :return: 存活玩家角色信息列表
        """
        alive_ids = []
        for player in self.alive_players:
            alive_ids.append(player.player_id)
        self.alive_players_id = alive_ids
        return self.alive_players_id

    def get_VILLAGERS_players(self):
        """
        获取村民阵营玩家列表
        :return: 村民阵营玩家列表
        """
        return self.villagers_players

    def get_WEREWOLVES_players(self):
        """
        获取狼人阵营玩家列表
        :return: 狼人阵营玩家列表
        """
        return self.werewolves_players

    def get_day_count(self):
        """
        获取当前游戏天数
        :return: 当前游戏天数
        """
        return self.day_count

    def update_day_count(self):
        """
        更新游戏天数（增加一天）
        :return: 无有效返回值，仅打印信息
        """
        if self.game_is_over is True:
            print("游戏已结束")  # 游戏已结束时不更新天数
        else:
            self.day_count = self.day_count + 1
            print("====================")
            print(f"\n当前是：第 {self.day_count} 天。新的一天开始...")

    def get_current_phase(self):
        return self.phase

    def advance_phase(self):
        """推进到下一阶段"""
        if self.phase == "NIGHT":
            self.phase = "DAY"
        elif self.phase == "DAY":
            self.phase = "VOTE"
        elif self.phase == "VOTE":
            self.phase = "NIGHT"
            self.update_day_count()
        return self.phase

    def get_winner_faction(self):
        if self.game_is_over is False:
            return print("游戏尚未结束")
        else:
            return print(f"游戏获胜方是：{self.winner}")

