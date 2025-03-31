from src.roles.role import Role
from src.utils.rules_prompt import GameRulePrompt


class Werewolf(Role):
    def __init__(self, player_id=None, language="cn"):
        super().__init__(role_name="werewolf", player_id=player_id, language=language)

    def get_role_prompt(self):
        game_rule_prompt = self.rule_prompt.get_game_rules_prompt()
        role_prompt = self.role_prompt.get_werewolf_rule_prompt()

        prompt = f"""全局游戏规则提示：\n###{game_rule_prompt}###\n\n角色游戏规则提示：\n###{role_prompt}###"""

        return prompt

    def do_action(self, werewolf_players, response_prompt, phase_prompt, game_state):
        # 狼人阶段
        # 两个狼人协商决策
        kill_player = None
        if len(werewolf_players) == 2:
            werewolf_1 = werewolf_players[0]
            werewolf_2 = werewolf_players[1]
            # 获取狼人1和狼人2的初始消息列表
            werewolf_1_messages = werewolf_1.client.messages.copy()
            werewolf_2_messages = werewolf_2.client.messages.copy()
            print(f"狼人1号System Message：{werewolf_1_messages}")
            print(f"狼人2号System Message：{werewolf_2_messages}\n")

            # 添加当前阶段提示
            werewolf_1_night_prompt = GameRulePrompt().get_night_action_prompt(role='werewolf',
                                                                               day_count=game_state.get_day_count(), player_id=werewolf_players[0].player_id)
            werewolf_1_messages.append(
                {"role": "user", "content": f"{phase_prompt}\n\n{werewolf_1_night_prompt}\n\n{response_prompt}"})
            print(f"狼人1号Messages：{werewolf_1_messages}")

            # 狼人1先做决定
            werewolf_1_response = werewolf_1.client.get_response(
                input_messages=werewolf_1_messages)['content']
            print("狼人1号的回复: "+werewolf_1_response)
            werewolf_1_messages.append(
                {"role": "assistant", "content": werewolf_1_response})

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
                werewolf_2_messages.append({"role": "user", "content":
                                            f"""{phase_prompt}\n你的同伴狼人决定杀害 {wolf1_target}。理由是：{werewolf_1_response}。\n你同意这个决定吗？如果同意，请说明你的理由；如果不同意，请分析并提出你认为应该杀害的目标。\n\n{response_prompt}"""})

                print(f"狼人2号Messages：{werewolf_2_messages}")
                # 狼人2回应
                werewolf_2_response = werewolf_2.client.get_response(
                    input_messages=werewolf_2_messages)['content']
                print(f"狼人2的回复: {werewolf_2_response}")
                werewolf_2_messages.append(
                    {"role": "assistant", "content": werewolf_2_response})

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
                    werewolf_1_messages.append({"role": "user", "content":
                                                f"你原本决定杀害 {wolf1_target}，但你的同伴狼人不同意，他/她想要杀害 {wolf2_target}，理由是：{werewolf_2_response}。你同意这个新决定吗？如果同意，请说明你的理由；如果不同意，请再次分析并坚持你的目标或提出新的目标。\n\n{response_prompt}"})

                    werewolf_1_response = werewolf_1.client.get_response(
                        input_messages=werewolf_1_messages)['content']
                    werewolf_1_messages.append(
                        {"role": "assistant", "content": werewolf_1_response})

                    # 检查狼人1是否同意狼人2的决定
                    if wolf1_target == wolf2_target:
                        # 同意，达成共识
                        consensus = True
                        final_target = wolf2_target
                        print(f"狼人1同意狼人2的决定，杀害: {final_target}")
                        break
                    else:
                        # 不同意，更新狼人1的目标
                        wolf1_target = self.extract_target(
                            werewolf_1_response)
                        print(f"狼人1不同意，坚持或改为杀害: {wolf1_target}")

                rounds += 1

            # 检查是否达成共识
            if consensus:
                kill_player = final_target
                print(f"狼人达成共识，决定杀害: {kill_player}")
            else:
                kill_player = None
                print("狼人无法达成共识，今晚没有人被杀害")
        elif len(werewolf_players) == 1:
            # 一个狼人直接决定
            werewolf = werewolf_players[0]
            werewolf_messages = werewolf.client.messages.copy()
            werewolf_messages.append({"role": "user", "content": phase_prompt})

            werewolf_response = werewolf.client.get_response(
                input_messages=werewolf_messages)['content']
            print(f"唯一的狼人的回复: {werewolf_response}")

            # 提取狼人想要杀的目标
            kill_player = self.extract_target(werewolf_response)
            print(f"狼人决定杀害: {kill_player}")
        else:
            raise RuntimeError("Invalid werewolf count.")
        
        return kill_player