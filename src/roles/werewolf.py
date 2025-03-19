from .role import Role
from src.utils.rules_prompt import WerewolfPrompt


class Werewolf(Role):
    def __init__(self, name="werewolf", faction="WEREWOLVES"):
        super().__init__(name, faction)
        self.role_prompt = WerewolfPrompt.get_werewolf_rule_prompt()

    def use_ability(self):
        # 使用技能
        werewolf_ability_prompt = self.role_prompt
        return werewolf_ability_prompt