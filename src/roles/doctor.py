from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt


class Doctor(Role):
    def __init__(self, player_id=None, language="cn"):
        super().__init__(role_name="doctor", player_id=player_id, language=language)

    def get_role_prompt(self):
        game_rule_prompt = self.rule_prompt.get_game_rules_prompt()
        role_prompt = self.role_prompt.get_doctor_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt
    
    def do_action(self, doctor_player, response_prompt, phase_prompt, game_state):
        save_player = None
        doctor = doctor_player
        doctor_messages = doctor.client.messages.copy()
        print(f"医生System Message：{doctor_messages}")

        doctor_night_prompt = GameRulePrompt().get_night_action_prompt(role='doctor', day_count=game_state.get_day_count(), player_id=doctor_player.player_id)
        doctor_messages.append(
                {"role": "user", "content": f"{phase_prompt}\n\n{doctor_night_prompt}\n\n{response_prompt}"})
        print(f"医生Messages：{doctor_messages}")

        doctor_response = doctor.client.get_response(
            input_messages=doctor_messages)['content']
        print("医生的回复: "+doctor_response)
        doctor_messages.append(
            {"role": "assistant", "content": doctor_response})

        save_player = self.extract_target(doctor_response)
        print(f"医生选择救助: {save_player}")

        return save_player