from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt
from src.utils.game_enum import GameRole, MessageType, MessageRole


class Doctor(Role):
    def __init__(self, alive_players, day_count, phase, messages_manager):
        super().__init__(role_name=GameRole.DOCTOR, language=LANGUAGE)

        self.messages_manager = messages_manager  # 消息管理器

        self.alive_players = alive_players  # 获取存活玩家
        self.day_count = day_count  # 获取当前游戏天数
        self.current_phase = phase  # 获取当前阶段

        # 获取当前存活玩家中的医生玩家
        self.doctor = []
        if self.alive_players is not None:
            self.doctor = [
                player for player in self.alive_players if player.role == self.role_name][0]
        else:
            raise RuntimeError("医生已经死了，无法进行操作。")

        self.doctor_id = self.doctor.player_id  # 医生的ID

    def do_action(self, phase_prompt):
        save_player = None  # 医生救助的玩家

        doctor = self.doctor  # 医生玩家
        doctor_id = self.doctor_id

        # 医生夜晚阶段提示词
        doctor_night_prompt = GameRulePrompt().get_night_action_prompt(
            role=self.role_name,
            day_count=self.day_count,
            player_id=doctor_id)
        self._add_message(player_id=doctor_id,
                          message_type=MessageType.PRIVATE,
                          message_role=MessageRole.USER,
                          message=f"{phase_prompt}\n{doctor_night_prompt}")
        # print(f"医生Messages：{self.doctor_messages}")

        # 医生夜晚阶段回复
        doctor_response = doctor.client.get_response(
            messages=doctor.messages)['content']
        print("医生的回复: "+doctor_response)
        self._add_message(player_id=doctor_id,
                          message_type=MessageType.PRIVATE,
                          message_role=MessageRole.ASSISTANT,
                          message=doctor_response)

        # 医生选择救助的玩家
        save_player = self.extract_target(doctor_response)
        print(f"医生选择救助: {save_player}")

        return save_player

    def discuss(self, player_id):
        prompt = f"现在是第{self.day_count}天的白天（DAY）讨论阶段。请结合游戏规则，根据的你玩家角色{GameRole.DOCTOR.value}和已有游戏信息进行分析讨论。讨论的内容可以包括但不限于：‘你认为谁是狼人？’、‘谁在说真话，谁又在为了生存而撒谎？’你可以说真话也可以撒谎。请注意，讨论阶段是狼人（WEREWOLVES）阵营和村民（VILLAGERS）阵营之间的博弈阶段，你可以选择隐瞒自己的身份或试图揭露其他玩家的身份。请根据游戏规则进行讨论。仅输出你想要表达的讨论内容，不要输出任何其他信息。"
        doctor = next(
            (p for p in self.alive_players if p.player_id == player_id), None)
        if not doctor:
            raise ValueError(
                f"Player with ID {player_id} not found in alive players")
        self._add_message(
            player_id=player_id,
            message_type=MessageType.PRIVATE,
            message_role=MessageRole.USER,
            message=prompt)
        doctor_response = doctor.client.get_response(
            messages=doctor.messages)['content']
        return doctor_response

    def _add_message(self, player_id, message_type, message_role, message):
        """
        添加消息到医生的消息列表
        :param message: 消息内容
        """
        self.doctor.add_message(role=message_role, content=message)
        self.messages_manager.add_message(
            player_id=player_id,
            role=self.role_name,
            day_count=self.day_count,
            phase=self.current_phase,
            message_type=message_type,
            content=message)
