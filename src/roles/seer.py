from .role import Role
from src.utils.rules_prompt import WerewolfPrompt


class Seer(Role):
    def __init__(self, name="seer", faction="VILLAGERS"):
        super().__init__(name, faction)
        self.role_prompt = WerewolfPrompt.get_seer_rule_prompt()

    def use_ability(self):
        # 使用技能
        seer_ability_prompt = self.role_prompt
        return seer_ability_prompt
