from .role import Role
from src.utils.rules_prompt import WerewolfPrompt

class Villager(Role):
    def __init__(self, name="villager", faction="VILLAGERS"):
        super().__init__(name, faction)
        self.role_prompt = WerewolfPrompt.get_villager_rule_prompt

    def use_ability(self):
        # 使用技能
        villager_ability_prompt = self.role_prompt
        return villager_ability_prompt
