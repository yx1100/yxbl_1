from src.agents.base_agent import BaseAgent
from src.utils.llm_client import LLMClient
from src.utils.rules_prompt import GameRulePrompt


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
        role_message = GameRulePrompt().get_role_prompt(role=role, player_id=player_id)
        self.client = LLMClient(system_message=role_message)
