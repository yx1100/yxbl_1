from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt, WerewolfRolePrompt


class Doctor(Role):
    def __init__(self):
        super().__init__(role_name="doctor", language=LANGUAGE)

        self.doctor_messages = []  # 医生的消息列表

    def do_action(self, alive_players, response_prompt, phase_prompt, game_state):
        # 获取当前存活玩家中的医生玩家
        if alive_players is not None:
            doctor = [player for player in alive_players if player.role == 'doctor'][0]
        else:
            raise RuntimeError("医生已经死了，无法进行操作。")

        save_player = None  # 医生救助的玩家

        # 医生系统消息(System Message)
        self._add_message(doctor.client.messages.copy()[0])
        # print(f"医生System Message：{self.doctor_messages[0]}")

        # 医生夜晚阶段提示词
        doctor_night_prompt = GameRulePrompt().get_night_action_prompt(role='doctor', day_count=game_state.get_day_count(), player_id=doctor.player_id)
        self._add_message({"role": "user", "content": f"{phase_prompt}\n\n{doctor_night_prompt}\n\n{response_prompt}"})
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
        """
        添加消息到医生的消息列表
        :param message: 消息内容
        """
        self.doctor_messages.append(message)

    def get_role_prompt(self, player_id):
        game_rule_prompt = GameRulePrompt().get_game_rules_prompt()
        role_prompt = WerewolfRolePrompt(player_id).get_doctor_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt
