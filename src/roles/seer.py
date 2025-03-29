import json
import re
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt


class Seer(Role):
    def __init__(self, player_id=None, language="cn"):
        super().__init__(role_name="seer", player_id=player_id, language=language)

    def get_role_prompt(self):
        game_rule_prompt = self.rule_prompt.get_game_rules_prompt()
        role_prompt = self.role_prompt.get_seer_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt

    def do_action(self, seer_player, response_prompt, phase_prompt, game_state):
        check_player = None
        seer = seer_player
        seer_messages = seer.client.messages.copy()
        print(f"预言家System Message：{seer_messages}")

        seer_night_prompt = GameRulePrompt().get_night_action_prompt(role='seer', day_count=game_state.get_day_count(), player_id=seer_player.player_id)
        seer_messages.append(
                {"role": "user", "content": f"{phase_prompt}\n\n{seer_night_prompt}\n\n{response_prompt}"})
        print(f"预言家Messages：{seer_messages}")

        seer_response = seer.client.get_response(
            input_messages=seer_messages)['content']
        print("预言家的回复: "+seer_response)
        seer_messages.append(
            {"role": "assistant", "content": seer_response})

        check_player = self.extract_target(seer_response)
        print(f"预言家选择查验: {check_player}")

        return check_player