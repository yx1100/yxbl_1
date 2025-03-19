from .role import Role
from src.utils.rules_prompt import WerewolfPrompt


class Doctor(Role):
    def __init__(self, name="doctor", faction="VILLAGERS"):
        super().__init__(name, faction)
        self.role_prompt = WerewolfPrompt.get_doctor_rule_prompt()

    def use_ability(self):
        # 使用技能
        doctor_ability_prompt = self.role_prompt
        return doctor_ability_prompt
