from agents.base_agent import BaseAgent
from utils.llm_client import LLMClient


class LLMAgent(BaseAgent):
    def __init__(self, player_id, role, faction):
        """初始化基于LLM的智能体

        Args:
            player_id: 玩家ID
            role: 角色对象(Werewolf, Villager等)
            faction: 阵营
            api_client: LLMClient实例
            is_alive: 是否存活
        """
        super().__init__(player_id, role, faction, human_or_ai="AI")
        self.client = LLMClient(system_message=f"你是一名狼人杀游戏中的玩家。你的角色是一名{self.role}。")

        self.chat_history = []  # 存储与其他玩家的对话历史
        self.knowledge = {
            "suspects": [],      # 怀疑是狼人的玩家
            "trusted": [],       # 认为是好人的玩家
            "observed_deaths": []  # 观察到的死亡情况
        }

