from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt
from src.utils.game_enum import GameRole, MessageType, MessageRole

class Villager(Role):
    def __init__(self, alive_players, day_count, phase, messages_manager):
        super().__init__(role_name=GameRole.VILLAGER, language=LANGUAGE)

        self.messages_manager = messages_manager  # 消息管理器

        self.alive_players = alive_players  # 获取存活玩家
        self.day_count = day_count  # 获取当前游戏天数
        self.current_phase = phase  # 获取当前阶段

        # 获取当前存活玩家中的医生玩家
        self.villager_players = []
        if self.alive_players is not None:
            self.villager_players = [
                player for player in self.alive_players if player.role == self.role_name]
        else:
            raise RuntimeError("村民已经全死了，无法进行操作。")

        self.villager_nums = len(self.villager_players)  # 获取狼人数量
        if self.villager_nums == 2:
            # TODO 目前先固定村民数量为2，后期再考虑修改
            self.villager_1 = self.villager_players[0]  # 狼人1
            self.villager_2 = self.villager_players[1]  # 狼人2

            self.villager_1_id = self.villager_1.player_id  # 狼人1的ID
            self.villager_2_id = self.villager_2.player_id  # 狼人2的ID

        elif self.villager_nums == 1:
            self.villager = self.villager_players[0]  # 狼人1

            self.villager_id = self.villager.player_id  # 狼人1的ID

    def discuss(self, player_id):
        prompt = f"现在是第{self.day_count}天的白天（DAY）讨论阶段。请结合游戏规则，根据的你玩家角色{GameRole.VILLAGER.value}和已有游戏信息进行分析讨论。讨论的内容可以包括但不限于：‘你认为谁是狼人？’、‘谁在说真话，谁又在为了生存而撒谎？’你可以说真话也可以撒谎。请注意，讨论阶段是狼人（WEREWOLVES）阵营和村民（VILLAGERS）阵营之间的博弈阶段，你可以选择隐瞒自己的身份或试图揭露其他玩家的身份。请根据游戏规则进行讨论。仅输出你想要表达的讨论内容，不要输出任何其他信息。"
        villager = next(
            (p for p in self.alive_players if p.player_id == player_id), None)
        if not villager:
            raise ValueError(
                f"Player with ID {player_id} not found in alive players")
        self._add_message(
            player_id=player_id,
            message_type=MessageType.PRIVATE,
            message_role=MessageRole.USER,
            message=prompt)
        doctor_response = villager.client.get_response(
            messages=villager.messages)['content']
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
