import random
from src.environment.game_state import GameState
from src.utils.rules_prompt import WerewolfRolePrompt, GameRulePrompt
from src.agents.llm_agent import LLMAgent
from src.agents.human_agent import HumanAgent
import json
import re


class GameManager:
    def __init__(self, players_count=6):
        self.players_count = players_count
        self.game_state = None
        self.game_agents = []

        self.kill_player = None
        self.save_player = None
        self.check_player = None

    def setup_game(self):
        # 设置游戏环境和玩家
        # 计算村民数量
        villagers_count = self.players_count - 4  # 1 doctor, 2 werewolves, 1 seer
        if villagers_count < 0:
            raise ValueError(
                "Player count must be at least 4 to have all required roles")

        # 创建角色列表
        player_role_list = ['doctor'] + ['werewolf'] * \
            2 + ['seer'] + ['villager'] * villagers_count
        # 随机打乱角色列表
        random.shuffle(player_role_list)

        # 创建玩家ID列表,格式为"ID_X"。
        player_id_list = [f"ID_{i}" for i in range(1, self.players_count + 1)]

        # 随机选择一个ID作为人类玩家
        human_player_id = random.choice(player_id_list)

        # 创建玩家代理
        agents = []
        for player_id, role in zip(player_id_list, player_role_list):
            # 根据角色确定阵营
            faction = "WEREWOLVES" if role == "werewolf" else "VILLAGERS"

            # 根据ID创建人类或AI代理
            if player_id == human_player_id:
                # agent = HumanAgent(player_id=player_id, role=role, faction=faction)
                agent = LLMAgent(player_id=player_id,
                                 role=role, faction=faction)
            else:
                agent = LLMAgent(player_id=player_id,
                                 role=role, faction=faction)
            agents.append(agent)

        self.game_state = GameState(agents)
        self.game_agents = agents

        return self.game_agents

    def run_phase(self):
        """根据当前阶段运行相应的处理方法"""
        # 确保游戏状态已初始化
        if self.game_state is None:
            raise RuntimeError(
                "Game state not initialized. Please setup game first.")

        # 1. 判断游戏是否结束
        if self.game_state.game_is_over:
            self.end_game()
            return

        # 2. 获取当前存活玩家
        alive_players = self.game_state.get_alive_players()
        alive_players_id = [
            player.player_id for player in alive_players]  # 获取存活玩家ID列表
        alive_roles = self.game_state.get_alive_players_role()  # 获取存活玩家角色列表
        # 3. 获取当前天数
        current_day_count = self.game_state.get_day_count()  # 获取当前游戏天数
        print(f"当前游戏天数：{self.game_state.day_count}")
        # 4. 获取当前阶段
        current_phase = self.game_state.get_current_phase()
        print(f"当前游戏阶段：{current_phase}")
        # 5. 获取当前阶段提示词
        phase_prompt = GameRulePrompt().get_phase_prompt(day_count=current_day_count, phase=current_phase, alive_players=alive_players_id)
        print(f"当前阶段提示词：{phase_prompt}")

        # 执行当前阶段的逻辑
        if current_phase == "NIGHT":
            self.night_phase(alive_players, alive_roles, phase_prompt)
        elif current_phase == "DAY":
            self.day_phase()
        elif current_phase == "VOTE":
            self.vote_phase()

        # 推进到下一阶段
        next_phase = self.game_state.advance_phase()
        return next_phase

    def night_phase(self, alive_players, alive_roles, phase_prompt):
        """处理夜晚阶段"""
        """
        1. 狼人：在场存活的狼人睁眼。如果存活的狼人数量为2，则第1个狼人根据分析，然后决定杀谁。如果第2个狼人同意第1个狼人的决定，则狼人达成共识选定受害者。如果第2个狼人不同意的第1个狼人的决定，则第2个狼人给出分析，然后决定杀谁。如果第1个狼人同意第2个狼人的决定，则狼人达成共识杀害第2个狼人选定的受害者，否则第1个狼人继续给出自己的分析和决定。以此反复5个来回，若狼人们仍无法达成共识选定受害者，则这一夜将没有人被害。如果存活的狼人数量为1，则唯一的狼人决定杀害谁。无论有没有达成共识选定受害者，狼人闭眼。
        2. 医生：医生如果还存活的话，角色为医生的存活玩家选择决定救治在场存活的哪一位玩家。系统将判断，如果医生选择的玩家和狼人杀害的玩家为同一人，则该玩家被救活，这一夜将无人死去。医生闭眼。
        3. 预言家：预言家如果还存活的话，角色为预言家的存活玩家选择查验在场存活的某一位玩家身份。系统将告诉预言家这名玩家的真实游戏身份。预言家闭眼。
        - 如果医生和预言家被杀害，在夜晚阶段仍会有医生和预言家的角色行动阶段，但不会有任何事情发生。
        """
        # 确保游戏状态已初始化
        if self.game_state is None:
            raise RuntimeError(
                "Game state not initialized. Please setup game first.")

        print("\n==== 夜晚降临 ====")
        # 处理狼人袭击、医生救人、预言家查验等行为

        print("存活玩家：", [player.player_id for player in alive_players])
        # 狼人玩家
        werewolf_players = [
            player for player in alive_players if player.role == 'werewolf']
        print("狼人玩家:", [player.player_id for player in werewolf_players])
        # 医生玩家
        doctor_player = [
            player for player in alive_players if player.role == 'doctor'][0]
        # 预言家玩家
        seer_player = [
            player for player in alive_players if player.role == 'seer'][0]

        response_prompt = GameRulePrompt().get_response_format_prompt()
        # 狼人阶段
        # 两个狼人协商决策
        if len(werewolf_players) == 2:
            werewolf_1 = werewolf_players[0]
            werewolf_2 = werewolf_players[1]
            # 获取狼人1和狼人2的初始消息列表
            werewolf_1_messages = werewolf_1.client.messages.copy()
            werewolf_2_messages = werewolf_2.client.messages.copy()
            print(f"狼人1号System Message：{werewolf_1_messages}")
            print(f"狼人2号System Message：{werewolf_2_messages}")

            # 添加当前阶段提示
            werewolf_1_night_prompt = GameRulePrompt().get_night_action_prompt(role='werewolf', day_count=self.game_state.get_day_count(), player_id=werewolf_players[0].player_id)
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
            wolf1_target = self.extract_kill_target(werewolf_1_response)
            print(f"狼人1想要杀害: {wolf1_target}")

            # 初始化变量
            consensus = False
            final_target = None
            rounds = 0
            max_rounds = 4

            while not consensus and rounds < max_rounds:
                # 添加狼人1的决定给狼人2
                werewolf_2_messages.append({"role": "user", "content":
                                            f"""{phase_prompt}\n\n你的同伴狼人决定杀害 {wolf1_target}。你同意这个决定吗？如果同意，请说明你的理由；如果不同意，请分析并提出你认为应该杀害的目标。\n\n{response_prompt}"""})

                # 狼人2回应
                werewolf_2_response = werewolf_2.client.get_response(
                    input_messages=werewolf_2_messages)['content']
                print(f"狼人2的回复: {werewolf_2_response}")
                werewolf_2_messages.append(
                    {"role": "assistant", "content": werewolf_2_response})

                # 检查狼人2是否同意
                if self.check_agreement(werewolf_2_response):
                    # 同意，达成共识
                    consensus = True
                    final_target = wolf1_target
                    print(f"狼人2同意杀害: {final_target}")
                    break
                else:
                    # 不同意，提出自己的目标
                    wolf2_target = self.extract_kill_target(
                        werewolf_2_response)
                    print(f"狼人2不同意，想要杀害: {wolf2_target}")

                    # 狼人1回应狼人2的目标
                    werewolf_1_messages.append({"role": "user", "content":
                                                f"你原本决定杀害 {wolf1_target}，但你的同伴狼人不同意，他/她想要杀害 {wolf2_target}。你同意这个新决定吗？如果同意，请说明你的理由；如果不同意，请再次分析并坚持你的目标或提出新的目标。\n\n{response_prompt}"})

                    werewolf_1_response = werewolf_1.client.get_response(
                        input_messages=werewolf_1_messages)['content']
                    werewolf_1_messages.append(
                        {"role": "assistant", "content": werewolf_1_response})

                    # 检查狼人1是否同意狼人2的决定
                    if self.check_agreement(werewolf_1_response):
                        # 同意，达成共识
                        consensus = True
                        final_target = wolf2_target
                        print(f"狼人1同意狼人2的决定，杀害: {final_target}")
                        break
                    else:
                        # 不同意，更新狼人1的目标
                        wolf1_target = self.extract_kill_target(
                            werewolf_1_response)
                        print(f"狼人1不同意，坚持或改为杀害: {wolf1_target}")

                rounds += 1

            # 检查是否达成共识
            if consensus:
                self.kill_player = final_target
                print(f"狼人达成共识，决定杀害: {self.kill_player}")
            else:
                self.kill_player = None
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
            self.kill_player = self.extract_kill_target(werewolf_response)
            print(f"狼人决定杀害: {self.kill_player}")
        else:
            raise RuntimeError("Invalid werewolf count.")

        # 医生阶段
        if 'doctor' in alive_roles:
            print('一个医生')
            doctor_agent_prompt = doctor_player.client.messages
            doctor_response = doctor_player.client.get_response(
                input_messages=doctor_agent_prompt)['content']

            print("医生:", doctor_agent_prompt)

            self.save_player = "ID_2"
        else:
            print('医生已经被杀害，跳过医生阶段...')

        # 处理狼人杀人结果
        if self.kill_player == self.save_player:
            self.kill_player = None
        else:
            # Find the player with matching player_id and remove them
            # Create a copy for safe iteration
            for player in self.game_state.alive_players[:]:
                if player.player_id == self.kill_player:
                    self.game_state.alive_players.remove(player)
                    self.game_state.alive_roles.remove(player.role)
                    break
        # self.save_player = None

        # 预言家阶段
        if 'seer' in alive_roles:
            print('一个预言家')
            seer_agent_prompt = seer_player.client.messages
            seer_response = seer_player.client.get_response(
                input_messages=seer_agent_prompt)['content']

            print("预言家:", seer_agent_prompt)

            self.check_player = "ID_3"
        else:
            print('预言家已经被杀害，跳过预言家阶段...')

        print("被杀玩家：", self.kill_player)
        print("被救玩家：", self.save_player)
        print("被查玩家：", self.check_player)
        print(
            "存活玩家：", [player.player_id for player in self.game_state.alive_players])
        print("存活玩家角色：", self.game_state.alive_roles)

        self.end_game()

        return None

    def extract_kill_target(self, response):
        """从狼人的回复中提取杀人目标"""
        try:
            # 尝试解析JSON
            data = json.loads(response)

            # 检查action字段是否存在
            if 'action' in data:
                action = data['action']

                # 使用正则表达式提取"kill ID_X"中的ID_X部分
                match = re.search(r'kill (ID_\d+)', action)
                if match:
                    return match.group(1)
        except:
            # JSON解析失败，尝试直接从文本中提取
            pass

        # 如果JSON解析失败或没有找到目标，尝试直接从文本中提取
        match = re.search(r'kill (ID_\d+)', response)
        if match:
            return match.group(1)
        # 如果没找到，随机选择一个存活玩家
        alive_player_ids = [p.player_id for p in self.game_state.alive_players]
        valid_targets = [
            pid for pid in alive_player_ids if pid not in wolf_ids]
        if valid_targets:
            return random.choice(valid_targets)
        return None

    def check_agreement(self, response):
        """检查回复中是否表示同意"""
        # 简单实现：检查是否包含"同意"、"赞成"等关键词
        agreement_keywords = ["同意", "赞成", "支持", "认可", "没问题", "可以"]
        for keyword in response:
            if keyword in response:
                return True
        return False

    def day_phase(self):
        """处理白天阶段"""
        """
        白天流程：
        1. 所有人睁眼。
        2. 系统宣布昨晚被杀（或救）的人是谁。如果有人被杀害，则被杀害的玩家将退出游戏不能再发言，但改名被杀害玩家的角色身份不会被披露。
        3. 按照存活玩家的ID顺序，每一名玩家将进行分析，表达自己的想法。
        4. 当所有存活玩家按顺序表达完自己的想法后，所有存活玩家将依次投票选择出一名可能是狼人的玩家。
        5. 得票数最多的玩家将被淘汰。若有2名玩家的得票数相同，将重新进行第2轮投票，存活玩家将在这2人中重新进行投票，得票数最多的玩家将被淘汰。如果第2轮投票仍未平票，则不会有玩家被淘汰，游戏进入到下一夜。
        """
        # 确保游戏状态已初始化
        if self.game_state is None:
            raise RuntimeError(
                "Game state not initialized. Please setup game first.")

        print("\n==== 天亮了 ====")
        # 宣布夜晚死亡情况
        if self.kill_player is not None:
            print(f"昨晚 {self.kill_player} 被杀害.")
        else:
            print("昨晚没有人被杀害.")

        # 玩家讨论
        for player in self.game_state.alive_players:
            print(f"Player {player.player_id} 发言：...")
            # TODO: 此处应该调用玩家的发言方法

    def vote_phase(self):
        """处理投票阶段"""
        # 确保游戏状态已初始化
        if self.game_state is None:
            raise RuntimeError(
                "Game state not initialized. Please setup game first.")

        print("\n==== 投票阶段 ====")
        # 收集所有玩家的投票

        for player in self.game_state.alive_players:
            print(f"Player {player.player_id} 发言：...")
            # TODO: 此处每位玩家选择一名投票对象
        # 处理投票结果

    def if_game_over(self):
        """判断游戏是否结束"""

        def if_game_over(self):
            """判断游戏是否结束"""
            alive_roles = self.game_state.get_alive_players_role()  # 获取存活玩家角色列表

            werewolf_count = alive_roles.count('werewolf')
            villager_count = len(alive_roles) - werewolf_count

            if werewolf_count == 0:
                # 狼人全部死亡，村民阵营胜利
                self.game_state.game_is_over = True
                self.game_state.winner = "VILLAGERS"
                return True
            elif werewolf_count >= villager_count:
                # 狼人数量等于或超过其他玩家，狼人阵营胜利
                self.game_state.game_is_over = True
                self.game_state.winner = "WEREWOLVES"
                return True
            else:
                # 游戏继续
                return False

    def end_game(self):
        """处理游戏结束"""
        print("\n==== 游戏结束 ====")
        if self.game_state.winner == "werewolf":
            print("狼人阵营胜利!")
        elif self.game_state.winner == "villager":
            print("村民阵营胜利!")
        else:
            print("游戏平局!")
        print("游戏结束！")
