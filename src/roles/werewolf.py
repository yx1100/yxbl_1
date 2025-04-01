from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt


class Werewolf(Role):
    def __init__(self, alive_players=None, messages_manager=None, language="cn"):
        super().__init__(role_name="werewolf", language=language)

        # 安全处理alive_players
        self.werewolf_players = []
        if alive_players is not None:
            self.werewolf_players = [player for player in alive_players if player.role == 'werewolf']
            print("狼人玩家：", [player.player_id for player in self.werewolf_players])

        # 安全处理messages_manager
        if messages_manager is not None:
            self.messages_manager = messages_manager
            self.global_conversation_history = self.messages_manager.history
            self.werewolf_1_messages = self.messages_manager.werewolf1_messages
            self.werewolf_2_messages = self.messages_manager.werewolf2_messages

    def get_role_prompt(self):
        game_rule_prompt = self.rule_prompt.get_game_rules_prompt()
        role_prompt = self.role_prompt.get_werewolf_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt

    def do_action(self, response_prompt, phase_prompt, game_state):
        kill_player = None

        # 两个狼人协商决策
        if len(self.werewolf_players) == 2:
            werewolf_1 = self.werewolf_players[0]
            werewolf_2 = self.werewolf_players[1]

            werewolf_1_id = werewolf_1.player_id
            werewolf_2_id = werewolf_2.player_id
            
            # 获取狼人1和狼人2的初始消息列表
            self._add_message('werewolf1', werewolf_1.client.messages.copy()[0])
            self._add_message('werewolf2', werewolf_2.client.messages.copy()[0])
            print(f"狼人1号System Message：{self.werewolf_1_messages}")
            print(f"狼人2号System Message：{self.werewolf_2_messages}\n")

            # 添加当前阶段提示
            werewolf_1_night_prompt = GameRulePrompt().get_night_action_prompt(role='werewolf', day_count=game_state.get_day_count(), player_id=werewolf_1.player_id)
            self._add_message('werewolf1', {"role": "user", "content": f"{phase_prompt}\n{werewolf_1_night_prompt}\n你的狼人同伙是玩家{werewolf_2_id}。\n{response_prompt}"})
            print(f"狼人1号Messages：{self.werewolf_1_messages}")

            # 狼人1先做决定
            werewolf_1_response = werewolf_1.client.get_response(input_messages=self.werewolf_1_messages)['content']
            print("狼人1号的回复: "+werewolf_1_response)
            self._add_message('werewolf1', {"role": "assistant", "content": werewolf_1_response})

            # 解析狼人1的目标
            wolf1_target = self.extract_target(werewolf_1_response)
            print(f"狼人1想要杀害: {wolf1_target}")

            # 初始化变量
            consensus = False
            final_target = None
            rounds = 0
            max_rounds = 4

            while not consensus and rounds < max_rounds:
                # 添加狼人1的决定给狼人2
                werewolf_2_night_prompt = GameRulePrompt().get_night_action_prompt(role='werewolf', day_count=game_state.get_day_count(), player_id=werewolf_2.player_id)
                self._add_message('werewolf2', {"role": "user", "content": f"""{phase_prompt}\n{werewolf_2_night_prompt}\n你的狼人同伙是玩家{werewolf_1_id}。\n你的狼人同伙玩家{werewolf_1_id}决定杀害 {wolf1_target}。理由是：{werewolf_1_response}。\n你同意这个决定吗？如果同意，请说明你的理由；如果不同意，请分析并提出你认为应该杀害的目标。\n{response_prompt}"""})
                print(f"狼人2号Messages：{self.werewolf_2_messages}")
                # 狼人2回应
                werewolf_2_response = werewolf_2.client.get_response(input_messages=self.werewolf_2_messages)['content']
                print(f"狼人2的回复: {werewolf_2_response}")
                self._add_message('werewolf2', {"role": "assistant", "content": werewolf_2_response})

                # 解析狼人1的目标
                wolf2_target = self.extract_target(werewolf_2_response)

                # 检查狼人2是否同意
                if wolf2_target == wolf1_target:
                    # 狼人2同意狼人1的决定
                    # 同意，达成共识
                    consensus = True
                    final_target = wolf1_target
                    print(f"狼人2同意杀害: {final_target}")
                    break
                else:
                    print(f"狼人2不同意，想要杀害: {wolf2_target}")
                    # 狼人1回应狼人2的目标
                    self._add_message('werewolf1', {"role": "user", "content": f"你原本决定杀害 {wolf1_target}，但你的同伴狼人{werewolf_2_id}不同意，他/她想要杀害 {wolf2_target}，理由是：{werewolf_2_response}。你同意这个新决定吗？如果同意，请说明你的理由；如果不同意，请再次分析并坚持你的目标或提出新的目标。\n{response_prompt}"})
                    print(f"狼人1号Messages：{self.werewolf_1_messages}")

                    werewolf_1_response = werewolf_1.client.get_response(input_messages=self.werewolf_1_messages)['content']
                    print(f"狼人1的回复: {werewolf_1_response}")
                    self._add_message('werewolf1', {"role": "assistant", "content": werewolf_1_response})

                    wolf1_target = self.extract_target(werewolf_1_response)
                    # 检查狼人1是否同意狼人2的决定
                    if wolf1_target == wolf2_target:
                        # 同意，达成共识
                        consensus = True
                        final_target = wolf2_target
                        print(f"狼人1同意狼人2的决定，杀害: {final_target}")
                        break
                    else:
                        # 不同意，更新狼人1的目标
                        print(f"狼人1不同意，坚持或改为杀害: {wolf1_target}")

                rounds += 1

            # 检查是否达成共识
            if consensus:
                kill_player = final_target
                print(f"狼人达成共识，决定杀害: {kill_player}")
            else:
                kill_player = None
                print("狼人无法达成共识，今晚没有人被杀害")
        elif len(self.werewolf_players) == 1:
            # 一个狼人直接决定
            if ...:
                player = 'werewolf1'
                werewolf = self.werewolf_players[0]
                werewolf_messages = self.messages_manager.werewolf1_messages
            else:
                player = 'werewolf2'
                werewolf = self.werewolf_players[0]
                werewolf_messages = self.messages_manager.werewolf1_messages
            # 添加当前阶段提示词
            werewolf_night_prompt = GameRulePrompt().get_night_action_prompt(role='werewolf', day_count=game_state.get_day_count(), player_id=werewolf.player_id)
            self._add_message(player, {"role": "user", "content": f"{phase_prompt}\n{werewolf_night_prompt}\n{response_prompt}"})

            werewolf_response = werewolf.client.get_response(input_messages=werewolf_messages)['content']
            print("唯一的狼人的回复: "+werewolf_response)
            self._add_message(player, {"role": "assistant", "content": werewolf_response})

            werewolf_response = werewolf.client.get_response(
                input_messages=werewolf_messages)['content']
            print(f": {werewolf_response}")

            # 提取狼人想要杀的目标
            kill_player = self.extract_target(werewolf_response)
            print(f"狼人决定杀害: {kill_player}")
        else:
            raise RuntimeError("Invalid werewolf count.")

        return kill_player
    
    def _add_message(self, player, message):
        self.messages_manager.add_message(role=f'{player}', content=message)
