from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt


class Seer(Role):
    def __init__(self, messages_manager=None, player_id=None, language="cn"):
        super().__init__(role_name="seer", player_id=player_id, language=language)

        if messages_manager is not None:
            self.messages_manager = messages_manager
            self.global_conversation_history = self.messages_manager.history
            self.seer_messages = self.messages_manager.seer_messages

    def get_role_prompt(self):
        game_rule_prompt = self.rule_prompt.get_game_rules_prompt()
        role_prompt = self.role_prompt.get_seer_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt

    def do_action(self, seer_player, response_prompt, phase_prompt, game_state):
        check_player = None # 预言家查验的玩家
        seer = seer_player

        # 预言家系统消息(System Message)
        self._add_message(seer.client.messages.copy()[0])
        print(f"预言家System Message：{self.seer_messages[0]}")

        # 预言家夜晚阶段提示词
        seer_night_prompt = GameRulePrompt().get_night_action_prompt(role='seer', day_count=game_state.get_day_count(), player_id=seer_player.player_id)
        self._add_message({"role": "user", "content": f"{phase_prompt}\n\n{seer_night_prompt}\n\n{response_prompt}"})
        print(f"预言家Messages：{self.seer_messages}")

        # 预言家夜晚阶段回复
        seer_response = seer.client.get_response(input_messages=self.seer_messages)['content']
        print("预言家的回复: "+seer_response)
        self._add_message({"role": "assistant", "content": seer_response})

        # 预言家选择查验的玩家
        check_player = self.extract_target(seer_response)
        print(f"预言家选择查验: {check_player}")

        return check_player
    
    def _add_message(self, message):
        self.messages_manager.add_message(role='seer', content=message)
