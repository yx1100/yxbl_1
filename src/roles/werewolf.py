from .role import Role


class Werewolf(Role):
    def __init__(self, player_id, language="cn"):
        super().__init__(name="werewolf", player_id=player_id, language=language)

    def get_role_prompt(self):
        return self.prompt.get_werewolf_rule_prompt()

    def use_ability(self):
        # 使用技能
        pass