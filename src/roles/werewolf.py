from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt
from src.utils.game_enum import GameRole, MessageType


class Werewolf(Role):
    def __init__(self, alive_players, day_count, phase, messages_manager):
        super().__init__(role_name=GameRole.WEREWOLF, language=LANGUAGE)

        # self.game_state = game_state  # 游戏状态
        self.messages_manager = messages_manager  # 消息管理器

        alive_players = alive_players  # 获取存活玩家
        self.day_count = day_count  # 获取当前游戏天数
        self.current_phase = phase  # 获取当前阶段

        self.werewolf_players = []
        if alive_players is not None:
            self.werewolf_players = [
                player for player in alive_players if player.role == self.role_name]
            print(
                "狼人玩家：", [player.player_id for player in self.werewolf_players])
        else:
            raise RuntimeError("No alive werewolf players found.")

        self.werewolf_1 = self.werewolf_players[0]  # 狼人1
        self.werewolf_2 = self.werewolf_players[1]  # 狼人2

        self.werewolf_1_id = self.werewolf_1.player_id  # 狼人1的ID
        self.werewolf_2_id = self.werewolf_2.player_id  # 狼人2的ID

        self.werewolf_1_messages = self.werewolf_1.messages
        self.werewolf_2_messages = self.werewolf_2.messages

    def do_action(self, response_prompt, phase_prompt):
        kill_player = None

        # 两个狼人协商决策
        if len(self.werewolf_players) == 2:
            werewolf_1 = self.werewolf_1
            werewolf_2 = self.werewolf_2

            werewolf_1_id = self.werewolf_1_id
            werewolf_2_id = self.werewolf_2_id

            # TODO: 获取狼人1和狼人2的System Message
            self._add_message(player='werewolf_1',
                              player_id=werewolf_1_id,
                              message_type=MessageType.PRIVATE,
                              message=self.werewolf_1_messages[0]['content'])
            self._add_message(player='werewolf_2',
                              player_id=werewolf_2_id,
                              message_type=MessageType.PRIVATE,
                              message=self.werewolf_2_messages[0]['content'])
            # print(f"狼人1号System Message：{self.werewolf_1_messages}")
            # print(f"狼人2号System Message：{self.werewolf_2_messages}\n")

            # 添加当前阶段提示
            werewolf_1_night_prompt = GameRulePrompt().get_night_action_prompt(
                role=self.role_name, day_count=self.day_count, player_id=werewolf_1_id)
            self._add_message(player='werewolf_1',
                              player_id=werewolf_1_id,
                              message={"role": "user", "content": f"{phase_prompt}\n{werewolf_1_night_prompt}\n你的狼人同伙是玩家{werewolf_2_id}。\n{response_prompt}"})
            # print(f"狼人1号Messages：{self.werewolf_1_messages}")

            # 狼人1先做决定
            werewolf_1_response = werewolf_1.client.get_response(
                input_messages=self.werewolf_1_messages)['content']
            print("狼人1号的回复: "+werewolf_1_response)
            self._add_message(player='werewolf_1',
                              player_id=werewolf_1_id,
                              message={"role": "assistant", "content": werewolf_1_response})

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
                werewolf_2_night_prompt = GameRulePrompt().get_night_action_prompt(
                    role=self.role_name, day_count=self.day_count, player_id=werewolf_2_id)
                self._add_message(player='werewolf_2',
                                  player_id=werewolf_2_id,
                                  message={"role": "user", "content": f"""{phase_prompt}\n{werewolf_2_night_prompt}\n你的狼人同伙是玩家{werewolf_1_id}。\n你的狼人同伙玩家{werewolf_1_id}决定杀害 {wolf1_target}。理由是：{werewolf_1_response}。\n你同意这个决定吗？如果同意，请说明你的理由；如果不同意，请分析并提出你认为应该杀害的目标。\n{response_prompt}"""})
                # print(f"狼人2号Messages：{self.werewolf_2_messages}")
                # 狼人2回应
                werewolf_2_response = werewolf_2.client.get_response(
                    input_messages=self.werewolf_2_messages)['content']
                print(f"狼人2的回复: {werewolf_2_response}")
                self._add_message(player='werewolf_2',
                                  player_id=werewolf_2_id,
                                  message={"role": "assistant", "content": werewolf_2_response})

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
                    self._add_message(player='werewolf_1',
                                      player_id=werewolf_1_id,
                                      message={"role": "user", "content": f"你原本决定杀害 {wolf1_target}，但你的同伴狼人{werewolf_2_id}不同意，他/她想要杀害 {wolf2_target}，理由是：{werewolf_2_response}。你同意这个新决定吗？如果同意，请说明你的理由；如果不同意，请再次分析并坚持你的目标或提出新的目标。\n{response_prompt}"})
                    print(f"狼人1号Messages：{self.werewolf_1_messages}")

                    werewolf_1_response = werewolf_1.client.get_response(
                        input_messages=self.werewolf_1_messages)['content']
                    print(f"狼人1的回复: {werewolf_1_response}")
                    self._add_message(player='werewolf_1',
                                      player_id=werewolf_1_id,
                                      message={"role": "assistant", "content": werewolf_1_response})

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

            return kill_player, self.werewolf_1_messages, self.werewolf_2_messages
        # 只有一个狼人
        elif len(self.werewolf_players) == 1:
            # 一个狼人直接决定
            pass

            return kill_player

    def _add_message(self, player, player_id, message_type=MessageType.PRIVATE, message=None):
        if player == 'werewolf_1':
            self.werewolf_1_messages.append(message)
        elif player == 'werewolf_2':
            self.werewolf_2_messages.append(message)

        self.messages_manager.add_message(
            player_id=player_id,
            role=self.role_name,
            day_count=self.day_count,
            phase=self.current_phase,
            message_type=message_type,
            content=message
        )
