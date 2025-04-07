from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt, WerewolfRolePrompt


class Seer(Role):
    def __init__(self):
        super().__init__(role_name="seer", language=LANGUAGE)

        self.seer_messages = []  # 预言家的消息列表

    def do_action(self, alive_players, response_prompt, phase_prompt, game_state):
        # 获取当前存活玩家中的预言家玩家
        if alive_players is not None:
            seer = [player for player in alive_players if player.role == 'seer'][0]
        else:
            raise RuntimeError("预言家已经死了，无法进行操作。")

        check_player = None  # 预言家查验的玩家

        # 预言家系统消息(System Message)
        self._add_message(seer.client.messages.copy()[0])
        # print(f"预言家System Message：{self.seer_messages[0]}")

        # 预言家夜晚阶段提示词
        seer_night_prompt = GameRulePrompt().get_night_action_prompt(
            role='seer', day_count=game_state.get_day_count(), player_id=seer.player_id)
        self._add_message(
            {"role": "user", "content": f"{phase_prompt}\n\n{seer_night_prompt}\n\n{response_prompt}"})
        # print(f"预言家Messages：{self.seer_messages}")

        # 预言家夜晚阶段回复
        seer_response = seer.client.get_response(
            input_messages=self.seer_messages)['content']
        print("预言家的回复: "+seer_response)
        self._add_message({"role": "assistant", "content": seer_response})

        # 预言家选择查验的玩家
        check_player = self.extract_target(seer_response)
        print(f"预言家选择查验: {check_player}")

        return check_player

    def _add_message(self, message):
        """
        添加消息到预言家消息列表
        Args:
            message (dict): 消息内容
        """
        self.seer_messages.append(message)

    def get_role_prompt(self, player_id):
        game_rule_prompt = GameRulePrompt().get_game_rules_prompt()
        role_prompt = WerewolfRolePrompt(player_id).get_seer_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt
