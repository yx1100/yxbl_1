from roles.role import Role


class Doctor(Role):
    def __init__(self, player_id, language="cn"):
        super().__init__(name="doctor", player_id=player_id, language=language)

    def get_role_prompt(self):
        return self.prompt.get_doctor_rule_prompt()

    def use_ability(self, target_id):
        pass
