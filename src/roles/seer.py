from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt


class Seer(Role):
    def __init__(self, game_state, messages_manager):
        super().__init__(role_name="seer", language=LANGUAGE)

        self.game_state = game_state  # 游戏状态
        self.messages_manager = messages_manager  # 消息管理器

        self.alive_players = self.game_state.get_alive_players()  # 获取存活玩家
        self.day_count = self.game_state.get_day_count()  # 获取当前游戏天数
        self.current_phase = self.game_state.get_current_phase()  # 获取当前阶段

        # 获取当前存活玩家中的预言家玩家
        self.seer = []
        if self.alive_players is not None:
            self.seer = [
                player for player in self.alive_players if player.role == self.role_name][0]
        else:
            raise RuntimeError("预言家已经死了，无法进行操作。")
        
        self.seer_id = self.seer.player_id
        self.seer_messages = []  # 预言家的消息列表

    def do_action(self, response_prompt, phase_prompt):
        check_player = None  # 预言家查验的玩家

        seer = self.seer  # 预言家玩家
        seer_id = self.seer_id

        # 预言家系统消息(System Message)
        self._add_message(player_id=seer_id,
                          message_type='ROLE',
                          message=seer.client.messages.copy()[0])
        # print(f"预言家System Message：{self.seer_messages[0]}")

        # 预言家夜晚阶段提示词
        seer_night_prompt = GameRulePrompt().get_night_action_prompt(
            role='seer', day_count=self.day_count, player_id=seer_id)
        self._add_message(player_id=seer_id,
                          message={"role": "user", "content": f"{phase_prompt}\n\n{seer_night_prompt}\n\n{response_prompt}"})
        # print(f"预言家Messages：{self.seer_messages}")

        # 预言家夜晚阶段回复
        seer_response = seer.client.get_response(
            input_messages=self.seer_messages)['content']
        print("预言家的回复: "+seer_response)
        self._add_message(player_id=seer_id, 
                          message={"role": "assistant", "content": seer_response})

        # 预言家选择查验的玩家
        check_player = self.extract_target(seer_response)
        print(f"预言家选择查验: {check_player}")

        return check_player

    def _add_message(self, player_id, message_type='PRIVATE', message=None):
        """
        添加消息到预言家的消息列表
        :param message: 消息内容
        """
        self.seer_messages.append(message)
        self.messages_manager.add_message(
            player_id=player_id,
            role=self.role_name,
            day_count=int(self.day_count),
            phase=self.current_phase,
            message_type=message_type,
            content=message)
