from src.roles.role import Role


class Werewolf(Role):
    def __init__(self, player_id, language="cn"):
        super().__init__(name="werewolf", player_id=player_id, language=language)

    def get_role_prompt(self):
        game_rule_prompt = self.prompt.get_game_rules_prompt()
        role_prompt = self.prompt.get_werewolf_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt