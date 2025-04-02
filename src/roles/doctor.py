from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt, WerewolfRolePrompt


class Doctor(Role):
    def __init__(self, alive_players=None, messages_manager=None, language="cn"):
        super().__init__(role_name="doctor", language=language)

        # 安全处理alive_players
        self.doctor_player = []
        if alive_players is not None:
            self.doctor_player = [
                player for player in alive_players if player.role == 'doctor'][0]

        if messages_manager is not None:
            self.messages_manager = messages_manager
            self.global_conversation_history = self.messages_manager.history
            self.doctor_messages = self.messages_manager.doctor_messages

    def get_role_prompt(self, player_id):
        game_rule_prompt = GameRulePrompt().get_game_rules_prompt()
        role_prompt = WerewolfRolePrompt(player_id).get_doctor_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt

    def do_action(self, response_prompt, phase_prompt, game_state):
        save_player = None  # 医生救助的玩家
        doctor = self.doctor_player

        # 医生系统消息(System Message)
        self._add_message(doctor.client.messages.copy()[0])
        # print(f"医生System Message：{self.doctor_messages[0]}")

        # 医生夜晚阶段提示词
        doctor_night_prompt = GameRulePrompt().get_night_action_prompt(role='doctor',
                                                                       day_count=game_state.get_day_count(), player_id=doctor.player_id)
        self._add_message(
            {"role": "user", "content": f"{phase_prompt}\n\n{doctor_night_prompt}\n\n{response_prompt}"})
        # print(f"医生Messages：{self.doctor_messages}")

        # 医生夜晚阶段回复
        doctor_response = doctor.client.get_response(
            input_messages=self.doctor_messages)['content']
        print("医生的回复: "+doctor_response)
        self._add_message({"role": "assistant", "content": doctor_response})

        # 医生选择救助的玩家
        save_player = self.extract_target(doctor_response)
        print(f"医生选择救助: {save_player}")

        return save_player

    def _add_message(self, message):
        self.messages_manager.add_message(role='doctor', content=message)
