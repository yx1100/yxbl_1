from src.roles.role import Role


class Villager(Role):
    def __init__(self, player_id, language="cn"):
        super().__init__(name="villager", player_id=player_id, language=language)

    def get_role_prompt(self):
        return self.prompt.get_villager_rule_prompt()
