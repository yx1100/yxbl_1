from src.utils.game_enum import MessageRole
from src.agents.base_agent import BaseAgent
from src.utils.llm_client import LLMClient
from src.utils.rules_prompt import GameRulePrompt


class LLMAgent(BaseAgent):
    def __init__(self, player_id, role, human_or_ai="AI"):
        """初始化基于LLM的智能体

        Args:
            player_id: 玩家ID
            role: 角色对象(Werewolf, Villager等)
            human_or_ai: Agent类型，默认为"AI"

        Attributes:
            player_id: 玩家ID
            role: 角色(werewolf, doctor, seer, villager)
            human_or_ai: Agent类型，默认为"AI"
            client: LLM客户端
            messages: LLM messages数组
        """
        super().__init__(player_id, role, human_or_ai)

        # 初始化LLM客户端
        self.client = LLMClient()

        # 初始化LLM messages数组
        self.messages = []
        role_system_message = GameRulePrompt().get_role_prompt(
            role=role, player_id=player_id)  # 根据角色获取对应角色的Agent system message
        # 设置系统消息（System Message）。将系统消息添加到messages数组中
        self.add_message(role=MessageRole.SYSTEM, content=role_system_message)

    def add_message(self, role: MessageRole, content: str):
        """
        添加消息到消息列表

        Args:
            role: 消息角色
            content: 消息内容
        """
        self.messages.append({"role": role.value, "content": content})

    def get_messages(self):
        """
        获取LLM messages数组
        """
        return self.messages