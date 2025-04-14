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

        self.villager_nums = len(self.villager_players)  # 获取村民数量
        if self.villager_nums == 2:
            # TODO 目前先固定村民数量为2，后期再考虑修改
            self.villager_1 = self.villager_players[0]  # 村民1
            self.villager_2 = self.villager_players[1]  # 村民2

            self.villager_1_id = self.villager_1.player_id  # 村民1的ID
            self.villager_2_id = self.villager_2.player_id  # 村民2的ID

        elif self.villager_nums == 1:
            self.villager = self.villager_players[0]  # 村民1

            self.villager_id = self.villager.player_id  # 村民1的ID

    def discuss(self, player_id):
        prompt = GameRulePrompt().get_day_discuss_prompt(self.day_count, player_id, self.role_name)
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
        villager_response = villager.client.get_response(
            messages=villager.messages)['content']
        return villager_response

    def vote(self, player_id):
        prompt = GameRulePrompt().get_vote_prompt(self.day_count, player_id, self.role_name)
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
        villager_response = villager.client.get_response(
            messages=villager.messages)['content']
        vote_target = self.extract_target(villager_response)
        return vote_target

    def _add_message(self, player_id, message_type, message_role, message):
        """
        添加消息到医生的消息列表
        :param message: 消息内容
        """
        villager = next(
            (p for p in self.alive_players if p.player_id == player_id), None)
        villager.add_message(role=message_role, content=message)
        
        self.messages_manager.add_message(
            player_id=player_id,
            role=self.role_name,
            day_count=self.day_count,
            phase=self.current_phase,
            message_type=message_type,
            content=message)
