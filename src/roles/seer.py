from src.roles.role import Role


class Seer(Role):
    def __init__(self, player_id, language="cn"):
        super().__init__(name="seer", player_id=player_id, language=language)

    def get_role_prompt(self):
        return self.prompt.get_seer_rule_prompt()

    def use_ability(self):
        # 使用技能
        pass
