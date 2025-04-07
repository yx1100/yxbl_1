from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt, WerewolfRolePrompt


class Villager(Role):
    def __init__(self):
        super().__init__(role_name="villager", language=LANGUAGE)

    def get_role_prompt(self, player_id):
        game_rule_prompt = GameRulePrompt().get_game_rules_prompt()
        role_prompt = WerewolfRolePrompt(player_id).get_villager_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt
