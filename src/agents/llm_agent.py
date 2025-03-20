from agents.base_agent import BaseAgent
from utils.llm_client import LLMClient
from roles.doctor import Doctor
from roles.seer import Seer
from roles.villager import Villager
from roles.werewolf import Werewolf


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

        role_message = ''
        # 根据角色初始化角色对象
        if role == "doctor":
            role_message = Doctor(player_id).get_role_prompt()
        elif role == "seer":
            role_message = Seer(player_id).get_role_prompt()
        elif role == "villager":
            role_message = Villager(player_id).get_role_prompt()
        elif role == "werewolf":
            role_message = Werewolf(player_id).get_role_prompt()
        else:
            raise ValueError(f"Unknown role: {role}")
        self.client = LLMClient(system_message=role_message)

        self.chat_history = []  # 存储与其他玩家的对话历史
        self.knowledge = {
            "suspects": [],      # 怀疑是狼人的玩家
            "trusted": [],       # 认为是好人的玩家
            "observed_deaths": []  # 观察到的死亡情况
        }

