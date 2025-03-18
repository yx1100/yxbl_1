from src.agents.base_agent import BaseAgent
import random


class LLMAgent(BaseAgent):
    def __init__(self, player_id, role, api_client, faction, is_alive=True):
        """初始化基于LLM的智能体

        Args:
            player_id: 玩家ID
            role: 角色对象(Werewolf, Villager等)
            api_client: LLMClient实例
        """
        super().__init__(player_id, role, faction, is_alive)
        self.api_client = api_client
        self.chat_history = []  # 存储与其他玩家的对话历史
        self.knowledge = {
            "suspects": [],      # 怀疑是狼人的玩家
            "trusted": [],       # 认为是好人的玩家
            "observed_deaths": []  # 观察到的死亡情况
        }

    