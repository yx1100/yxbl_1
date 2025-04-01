from src.agents.base_agent import BaseAgent
from src.utils.llm_client import LLMClient
from src.roles.doctor import Doctor
from src.roles.seer import Seer
from src.roles.villager import Villager
from src.roles.werewolf import Werewolf


class LLMAgent(BaseAgent):
    def __init__(self, player_id, role, faction):
        """初始化基于LLM的智能体

        Args:
            player_id: 玩家ID
            role: 角色对象(Werewolf, Villager等)
            faction: 阵营
            client: LLMClient实例
        """
        super().__init__(player_id, role, faction, human_or_ai="AI")

        role_message = ''
        # 根据角色初始化角色对象
        if role == "doctor":
            role_message = Doctor().get_role_prompt(player_id)
        elif role == "seer":
            role_message = Seer().get_role_prompt(player_id)
        elif role == "villager":
            role_message = Villager().get_role_prompt(player_id)
        elif role == "werewolf":
            role_message = Werewolf().get_role_prompt(player_id)
        else:
            raise ValueError(f"Unknown role: {role}")
        self.client = LLMClient(system_message=role_message)
