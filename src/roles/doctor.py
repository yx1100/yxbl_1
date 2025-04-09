from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt


class Doctor(Role):
    def __init__(self, game_state, messages_manager):
        super().__init__(role_name="doctor", language=LANGUAGE)

        self.game_state = game_state  # 游戏状态
        self.messages_manager = messages_manager  # 消息管理器

        self.alive_players = self.game_state.get_alive_players()  # 获取存活玩家
        self.day_count = self.game_state.get_day_count()  # 获取当前游戏天数
        self.current_phase = self.game_state.get_current_phase()  # 获取当前阶段

        # 获取当前存活玩家中的医生玩家
        self.doctor = []
        if self.alive_players is not None:
            self.doctor = [
                player for player in self.alive_players if player.role == self.role_name][0]
        else:
            raise RuntimeError("医生已经死了，无法进行操作。")

        self.doctor_id = self.doctor.player_id  # 医生的ID
        self.doctor_messages = []  # 医生的消息列表

    def do_action(self, response_prompt, phase_prompt):
        save_player = None  # 医生救助的玩家

        doctor = self.doctor  # 医生玩家
        doctor_id = self.doctor_id

        # 医生系统消息(System Message)
        self._add_message(player_id=doctor_id,
                          message_type='ROLE',
                          message=doctor.client.messages.copy()[0])
        # print(f"医生System Message：{self.doctor_messages[0]}")

        # 医生夜晚阶段提示词
        doctor_night_prompt = GameRulePrompt().get_night_action_prompt(
            role=self.role_name, day_count=self.day_count, player_id=doctor_id)
        self._add_message(player_id=doctor_id,
                          message={"role": "user", "content": f"{phase_prompt}\n\n{doctor_night_prompt}\n\n{response_prompt}"})
        # print(f"医生Messages：{self.doctor_messages}")

        # 医生夜晚阶段回复
        doctor_response = doctor.client.get_response(
            input_messages=self.doctor_messages)['content']
        print("医生的回复: "+doctor_response)
        self._add_message(player_id=doctor_id, 
                          message={"role": "assistant", "content": doctor_response})

        # 医生选择救助的玩家
        save_player = self.extract_target(doctor_response)
        print(f"医生选择救助: {save_player}")

        return save_player

    def _add_message(self, player_id, message_type='PRIVATE', message=None):
        """
        添加消息到医生的消息列表
        :param message: 消息内容
        """
        self.doctor_messages.append(message)
        self.messages_manager.add_message(
            player_id=player_id,
            role=self.role_name,
            day_count=int(self.day_count),
            phase=self.current_phase,
            message_type=message_type,
            content=message)
