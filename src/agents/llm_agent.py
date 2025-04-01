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
            role_message = Doctor(player_id=player_id).get_role_prompt()
        elif role == "seer":
            role_message = Seer(player_id=player_id).get_role_prompt()
        elif role == "villager":
            role_message = Villager(player_id=player_id).get_role_prompt()
        elif role == "werewolf":
            role_message = Werewolf(player_id=player_id).get_role_prompt()
        else:
            raise ValueError(f"Unknown role: {role}")
        self.client = LLMClient(system_message=role_message)
