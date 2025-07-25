from src.utils.config import LANGUAGE
from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt
from src.utils.game_enum import GameRole, MessageType, MessageRole


class Werewolf(Role):
    def __init__(self, alive_players, day_count, phase, messages_manager):
        super().__init__(role_name=GameRole.WEREWOLF, language=LANGUAGE)

        self.messages_manager = messages_manager  # 消息管理器

        self.alive_players = alive_players  # 获取存活玩家
        self.day_count = day_count  # 获取当前游戏天数
        self.current_phase = phase  # 获取当前阶段

        # 获取狼人玩家列表
        self.werewolf_players = []
        if self.alive_players is not None:
            self.werewolf_players = [
                player for player in self.alive_players if player.role == self.role_name]
            # print(
            #     "狼人玩家：", [player.player_id for player in self.werewolf_players])
        else:
            raise RuntimeError("No alive werewolf players found.")

        self.werewolf_nums = len(self.werewolf_players)  # 获取狼人数量
        for i, werewolf in enumerate(self.werewolf_players):
            setattr(self, f"werewolf_{i+1}", werewolf)
            setattr(self, f"werewolf_{i+1}_id", werewolf.player_id)
    
    def do_action(self, phase_prompt):
        kill_player = None

        # 两个狼人协商决策
        if self.werewolf_nums == 2:
            werewolf_1 = self.werewolf_1  # Agent类型
            werewolf_2 = self.werewolf_2  # Agent类型

            werewolf_1_id = self.werewolf_1_id  # str类型
            werewolf_2_id = self.werewolf_2_id  # str类型

            # 添加夜晚阶段提示
            werewolf_1_night_prompt = GameRulePrompt().get_night_action_prompt(
                role=self.role_name,
                day_count=self.day_count,
                player_id=werewolf_1_id,
                werewolf_partners=werewolf_2_id)
            self._add_message(
                player_id=werewolf_1_id,
                message_type=MessageType.PRIVATE,
                message_role=MessageRole.USER,
                message=f"{phase_prompt}\n{werewolf_1_night_prompt}")

            # 狼人1先做决定
            werewolf_1_response = werewolf_1.client.get_response(
                messages=werewolf_1.messages)['content']
            print(f"狼人1号({werewolf_1_id})的回复: {werewolf_1_response}")
            self._add_message(
                player_id=werewolf_1_id,
                message_type=MessageType.PRIVATE,
                message_role=MessageRole.ASSISTANT,
                message=werewolf_1_response)

            # 解析狼人1的目标
            wolf1_target = self.extract_target(werewolf_1_response)
            print(f"狼人1号({werewolf_1_id})想要杀害: {wolf1_target}")

            # 初始化变量
            consensus = False
            final_target = None
            rounds = 0
            max_rounds = 4

            while not consensus and rounds < max_rounds:
                # 添加狼人1的决定给狼人2
                werewolf_2_night_prompt = GameRulePrompt().get_night_action_prompt(
                    role=self.role_name,
                    day_count=self.day_count,
                    player_id=werewolf_2_id,
                    werewolf_partners=werewolf_1_id)
                self._add_message(
                    player_id=werewolf_2_id,
                    message_type=MessageType.PRIVATE,
                    message_role=MessageRole.USER,
                    message=f"""{phase_prompt}\n{werewolf_2_night_prompt}\n你的狼人同伙玩家{werewolf_1_id}决定杀害 {wolf1_target}。理由是：{werewolf_1_response}。\n你同意这个决定吗？如果同意，请说明你的理由；如果不同意，请分析并提出你认为应该杀害的目标。""")

                # 狼人2回应
                werewolf_2_response = werewolf_2.client.get_response(
                    messages=werewolf_2.messages)['content']
                print(f"狼人2号({werewolf_2_id})的回复: {werewolf_2_response}")
                self._add_message(
                    player_id=werewolf_2_id,
                    message_type=MessageType.PRIVATE,
                    message_role=MessageRole.ASSISTANT,
                    message=werewolf_2_response)

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
                    self._add_message(
                        player_id=werewolf_1_id,
                        message_role=MessageRole.USER,
                        message=f"你原本决定杀害 {wolf1_target}，但你的同伴狼人{werewolf_2_id}不同意，他/她想要杀害 {wolf2_target}，理由是：{werewolf_2_response}。你同意这个新决定吗？如果同意，请说明你的理由；如果不同意，请再次分析并坚持你的目标或提出新的目标。")
                    print(f"狼人1号Messages：{werewolf_1.messages}")

                    werewolf_1_response = werewolf_1.client.get_response(
                        messages=werewolf_1.messages)['content']
                    print(f"狼人1的回复: {werewolf_1_response}")
                    self._add_message(
                        player_id=werewolf_1_id,
                        message_type=MessageType.PRIVATE,
                        message_role=MessageRole.ASSISTANT,
                        message=werewolf_1_response)

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

            return kill_player
        # 只有一个狼人
        elif self.werewolf_nums == 1:
            # 一个狼人直接决定
            werewolf = self.werewolf_1  # Agent类型
            werewolf_id = self.werewolf_1_id  # str类型

            # 添加夜晚阶段提示
            werewolf_night_prompt = GameRulePrompt().get_night_action_prompt(
                role=self.role_name,
                day_count=self.day_count,
                player_id=werewolf_id)
            self._add_message(
                player_id=werewolf_id,
                message_type=MessageType.PRIVATE,
                message_role=MessageRole.USER,
                message=f"{phase_prompt}\n{werewolf_night_prompt}")

            # 唯一狼人做决定
            werewolf_response = werewolf.client.get_response(
                messages=werewolf.messages)['content']
            print("唯一狼人的回复: "+werewolf_response)
            self._add_message(
                player_id=werewolf_id,
                message_type=MessageType.PRIVATE,
                message_role=MessageRole.ASSISTANT,
                message=werewolf_response)

            # 解析狼人的目标
            kill_player = self.extract_target(werewolf_response)
            print(f"狼人想要杀害: {kill_player}")

            return kill_player

    def discuss(self, player_id):
        prompt = GameRulePrompt().get_day_discuss_prompt(self.day_count, player_id, self.role_name)
        # Find the player in alive_players that matches the given player_id
        werewolf = next(
            (p for p in self.alive_players if p.player_id == player_id), None)
        if not werewolf:
            raise ValueError(
                f"Player with ID {player_id} not found in alive players")

        self._add_message(
            player_id=player_id,
            message_type=MessageType.PRIVATE,
            message_role=MessageRole.USER,
            message=prompt)
        werewolf_response = werewolf.client.get_response(
            messages=werewolf.messages)['content']
        self._add_message(
            player_id=player_id,
            message_type=MessageType.PRIVATE,
            message_role=MessageRole.USER,
            message=werewolf_response)
        return werewolf_response

    def vote(self, player_id):
        prompt = GameRulePrompt().get_vote_prompt(self.day_count, player_id, self.role_name)
        werewolf = next(
            (p for p in self.alive_players if p.player_id == player_id), None)
        if not werewolf:
            raise ValueError(
                f"Player with ID {player_id} not found in alive players")

        self._add_message(
            player_id=player_id,
            message_type=MessageType.PRIVATE,
            message_role=MessageRole.USER,
            message=prompt)
        werewolf_response = werewolf.client.get_response(
            messages=werewolf.messages)['content']
        self._add_message(
            player_id=player_id,
            message_type=MessageType.PRIVATE,
            message_role=MessageRole.USER,
            message=werewolf_response)
        print("狼人投票的思考与决定: "+werewolf_response)
        vote_target = self.extract_target(werewolf_response)
        return vote_target

    def _add_message(self, player_id, message_type, message_role, message):
        werewolf = next(
            (p for p in self.alive_players if p.player_id == player_id), None)
        werewolf.add_message(role=message_role, content=message)

        self.messages_manager.add_message(
            player_id=player_id,
            role=self.role_name,
            day_count=self.day_count,
            phase=self.current_phase,
            message_type=message_type,
            content=message
        )
