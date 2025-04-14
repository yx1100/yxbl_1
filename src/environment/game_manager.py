import random
from collections import Counter

from prompt_toolkit import prompt
from src.utils.config import PLAYER_NUMS
from src.utils.config import MESSAGES_FILE_PATH
from src.agents.llm_agent import LLMAgent
from src.agents.human_agent import HumanAgent
from src.utils.game_enum import GameRole, GameFaction, GamePhase, MessageType, MessageRole
from src.utils.rules_prompt import GameRulePrompt
from src.utils.messages_manager import MessagesManager
from src.roles.werewolf import Werewolf
from src.roles.doctor import Doctor
from src.roles.seer import Seer
from src.roles.villager import Villager


class GameManager:
    def __init__(self):
        self.messages_manager = MessagesManager(MESSAGES_FILE_PATH)  # 初始化消息管理器

        self.init_players = self._set_players_agent()  # 游戏初始化，存活玩家列表
        self.init_players_id = [
            player.player_id for player in self.init_players]  # 存活玩家ID列表
        self.init_players_roles = [
            player.role for player in self.init_players]  # 存活角色列表

        prompt = f"""本场游戏初始玩家共有{len(self.init_players)}人，分别是{', '.join(self.init_players_id)}。"""
        print(f"主持人：{prompt}")
        print(
            f"系统信息：本场游戏玩家角色分别是：{', '.join([role.value for role in self.init_players_roles])}。\n======================\n")
        self.messages_manager.add_message(
            player_id="system",
            role=GameRole.HOST,
            day_count=0,
            phase=GamePhase.INIT,
            message_type=MessageType.PUBLIC,
            content=prompt
        )  # 这里的信息只加入了game messages，没有加入到玩家的上下文消息中

        self.day_count = 1  # 游戏天数
        self.alive_players = self.init_players.copy()  # 存活玩家列表

    def run_phase(self):
        """根据当前阶段运行相应的处理方法"""

        print(f"===== 游戏开始！=====")

        # 判断游戏是否结束
        while not self._if_game_over():  # 如果游戏没有结束
            print(f"\n==== 第 {self.day_count} 天 ====")
            self.night_phase()
        print("游戏结束！")
        return  # End the run_phase method after the game is over

    def night_phase(self):
        """处理夜晚阶段"""
        """
        1. 狼人：在场存活的狼人睁眼。如果存活的狼人数量为2，则第1个狼人根据分析，然后决定杀谁。如果第2个狼人同意第1个狼人的决定，则狼人达成共识选定受害者。如果第2个狼人不同意的第1个狼人的决定，则第2个狼人给出分析，然后决定杀谁。如果第1个狼人同意第2个狼人的决定，则狼人达成共识杀害第2个狼人选定的受害者，否则第1个狼人继续给出自己的分析和决定。以此反复5个来回，若狼人们仍无法达成共识选定受害者，则这一夜将没有人被害。如果存活的狼人数量为1，则唯一的狼人决定杀害谁。无论有没有达成共识选定受害者，狼人闭眼。
        2. 医生：医生如果还存活的话，角色为医生的存活玩家选择决定救治在场存活的哪一位玩家。系统将判断，如果医生选择的玩家和狼人杀害的玩家为同一人，则该玩家被救活，这一夜将无人死去。医生闭眼。
        3. 预言家：预言家如果还存活的话，角色为预言家的存活玩家选择查验在场存活的某一位玩家身份。系统将告诉预言家这名玩家的真实游戏身份。预言家闭眼。
        - 如果医生和预言家被杀害，在夜晚阶段仍会有医生和预言家的角色行动阶段，但不会有任何事情发生。
        """
        alive_players_id = [player.player_id for player in self.alive_players]
        alive_roles = [player.role for player in self.alive_players]

        print("\n==== 夜晚降临 ====")

        # 1. 获取夜晚阶段的提示词
        phase_prompt = GameRulePrompt().get_phase_prompt(day_count=self.day_count,
                                                         phase=GamePhase.NIGHT,
                                                         alive_players=alive_players_id)
        print(f"主 持 人：{phase_prompt}")

        self.messages_manager.add_message(
            player_id="system",
            role=GameRole.HOST,
            day_count=self.day_count,
            phase=GamePhase.NIGHT,
            message_type=MessageType.PUBLIC,
            content=phase_prompt
        )  # 这里的提示词只加入了game messages，后面在角色类方法中加入到玩家的上下文消息中

        print(f"主 持 人：当前的存活玩家有{', '.join(alive_players_id)}。")
        print(f"系统信息：玩家角色分别是{', '.join([role.value for role in alive_roles])}。")

        # 处理狼人袭击、医生救人、预言家查验等行为
        # 1. 狼人阶段
        print("\n==== 狼人阶段 ====\n")
        print("主 持 人：狼人请睁眼...")
        kill_player = None
        kill_player = Werewolf(
            alive_players=self.alive_players,
            day_count=self.day_count,
            phase=GamePhase.NIGHT,
            messages_manager=self.messages_manager
        ).do_action(phase_prompt)

        # 2. 医生阶段
        print("\n==== 医生阶段 ====\n医生请睁眼...")
        save_player = None
        if GameRole.DOCTOR in alive_roles:
            save_player = Doctor(
                alive_players=self.alive_players,
                day_count=self.day_count,
                phase=GamePhase.NIGHT,
                messages_manager=self.messages_manager
            ).do_action(phase_prompt)
        else:
            print('医生已经被杀害，跳过医生阶段...')

        # 预言家阶段
        print("\n==== 预言家阶段 ====\n预言家请睁眼...")
        check_player = None
        if GameRole.SEER in alive_roles:
            check_player = Seer(
                alive_players=self.alive_players,
                day_count=self.day_count,
                phase=GamePhase.NIGHT,
                messages_manager=self.messages_manager
            ).do_action(phase_prompt)
        else:
            print('预言家已经被杀害，跳过预言家阶段...')

        # 处理狼人杀人结果
        if kill_player == save_player:
            kill_player = None
        else:
            if kill_player is not None:
                # Find and remove the killed player from alive_players
                # Create a copy to safely iterate while removing
                for player in self.alive_players[:]:
                    if player.player_id == kill_player:
                        self.alive_players.remove(player)
                        break

        print("\n==== 夜晚总结 ====")
        if kill_player is not None:
            print("被杀玩家(公开信息)：", kill_player)
        else:
            print("昨晚没有人被杀。")
        if save_player is not None:
            print("被救玩家(系统信息)：", save_player)
        if check_player is not None:
            print("被查玩家(系统信息)：", check_player)

        print(f"存活玩家(公开信息)：{', '.join([player.player_id for player in self.alive_players])}")
        print(f"存活角色(系统信息)：{', '.join([player.role.value for player in self.alive_players])}")

        # self.update_phase()
        self.update_day()
        self.day_phase(kill_player)

    def day_phase(self, kill_player):
        """处理白天阶段"""
        """
        白天流程：
        1. 所有人睁眼。
        2. 系统宣布昨晚被杀（或救）的人是谁。如果有人被杀害，则被杀害的玩家将退出游戏不能再发言，但该名被杀害玩家的角色身份不会被披露。
        3. 按照存活玩家的ID顺序，每一名玩家将进行分析，表达自己的想法。
        4. 当所有存活玩家按顺序表达完自己的想法后，所有存活玩家将依次投票选择出一名可能是狼人的玩家。
        5. 得票数最多的玩家将被淘汰。若有2名玩家的得票数相同，将重新进行第2轮投票，存活玩家将在这2人中重新进行投票，得票数最多的玩家将被淘汰。如果第2轮投票仍未平票，则不会有玩家被淘汰，游戏进入到下一夜。
        """
        alive_players_id = [player.player_id for player in self.alive_players]
        alive_roles = [player.role.value for player in self.alive_players]

        print("\n==== 天亮了 ====\n所有玩家请睁眼...")

        last_night_info_prompt = GameRulePrompt().get_last_night_info_prompt(current_day=self.day_count,
                                                                             killed_player=kill_player,
                                                                             alive_players_id=alive_players_id)
        print(last_night_info_prompt)

        self.add_message_for_all_agents(
            role=MessageRole.USER,
            content=last_night_info_prompt)
        self.messages_manager.add_message(
            player_id="system",
            role=GameRole.HOST,
            day_count=self.day_count,
            phase=GamePhase.DAY,
            message_type=MessageType.PUBLIC,
            content=last_night_info_prompt
        )

        # 宣布夜晚死亡情况
        if kill_player is not None:
            print(f"主持人：昨晚玩家 {kill_player} 被杀害.")
        else:
            print("主持人(公开信息)：昨晚没有人被杀害.")
        print(f"存活玩家(公开信息)：{', '.join(alive_players_id)}")
        print(f"存活角色(系统信息)：{', '.join(alive_roles)}")

        # 玩家讨论
        for player in self.alive_players:
            # 根据角色类型进行发言
            if player.role == GameRole.WEREWOLF:
                discussion = Werewolf(
                    alive_players=self.alive_players,
                    day_count=self.day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).discuss(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 发言：{discussion}")

                self.add_message_for_all_agents(
                    role=MessageRole.USER,
                    content=f"第{self.day_count}天白天（DAY）阶段，玩家{player.player_id}的发言内容：{discussion}"
                )

            elif player.role == GameRole.DOCTOR:
                discussion = Doctor(
                    alive_players=self.alive_players,
                    day_count=self.day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).discuss(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 发言：{discussion}")

                self.add_message_for_all_agents(
                    role=MessageRole.USER,
                    content=f"第{self.day_count}天白天（DAY）阶段，玩家{player.player_id}的发言内容：{discussion}"
                )
            elif player.role == GameRole.SEER:
                discussion = Seer(
                    alive_players=self.alive_players,
                    day_count=self.day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).discuss(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 发言：{discussion}")

                self.add_message_for_all_agents(
                    role=MessageRole.USER,
                    content=f"第{self.day_count}天白天（DAY）阶段，玩家{player.player_id}的发言内容：{discussion}"
                )
            elif player.role == GameRole.VILLAGER:
                discussion = Villager(
                    alive_players=self.alive_players,
                    day_count=self.day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).discuss(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 发言：{discussion}")

                self.add_message_for_all_agents(
                    role=MessageRole.USER,
                    content=f"第{self.day_count}天白天（DAY）阶段，玩家{player.player_id}的发言内容：{discussion}"
                )
            else:
                raise ValueError(
                    f"Invalid role: {player.role.value}. Please check the game setup.")
        print("\n==== 玩家讨论结束 ====")

        self.vote_phase()

    def vote_phase(self):
        """处理投票阶段"""
        print("\n==== 投票阶段 ====")
        # 收集所有玩家的投票

        vote_result = []
        for player in self.alive_players:
            if player.role == GameRole.WEREWOLF:
                vote = Werewolf(
                    alive_players=self.alive_players,
                    day_count=self.day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).vote(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 投票：{vote}")
                vote_result.append(vote)
                self.add_message_for_all_agents(
                    role=MessageRole.USER,
                    content=f"第{self.day_count}天投票（VOTE）阶段，玩家{player.player_id}选择投出玩家是：{vote}。"
                )
            elif player.role == GameRole.DOCTOR:
                vote = Doctor(
                    alive_players=self.alive_players,
                    day_count=self.day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).vote(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 投票：{vote}")
                vote_result.append(vote)
                self.add_message_for_all_agents(
                    role=MessageRole.USER,
                    content=f"第{self.day_count}天投票（VOTE）阶段，玩家{player.player_id}选择投出玩家是：{vote}。"
                )
            elif player.role == GameRole.SEER:
                vote = Seer(
                    alive_players=self.alive_players,
                    day_count=self.day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).vote(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 投票：{vote}")
                vote_result.append(vote)
                self.add_message_for_all_agents(
                    role=MessageRole.USER,
                    content=f"第{self.day_count}天投票（VOTE）阶段，玩家{player.player_id}选择投出玩家是：{vote}。"
                )
            elif player.role == GameRole.VILLAGER:
                vote = Villager(
                    alive_players=self.alive_players,
                    day_count=self.day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).vote(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 投票：{vote}")
                vote_result.append(vote)
                self.add_message_for_all_agents(
                    role=MessageRole.USER,
                    content=f"第{self.day_count}天投票（VOTE）阶段，玩家{player.player_id}选择投出玩家是：{vote}。"
                )
            else:
                raise ValueError(
                    f"Invalid role: {player.role}. Please check the game setup.")
        # 处理投票结果
        print("投票结果：", vote_result)

        # 统计每个投票选项的出现次数
        vote_counts = Counter(vote_result)
        if not vote_counts:  # 处理空投票结果的情况
            print("出错！没有有效的投票结果！")
            # 根据游戏规则决定下一步，例如直接进入夜晚或宣布无人出局
            return  # 或者根据游戏逻辑进行其他处理
        # 找到最高票数
        max_votes = max(vote_counts.values())
        # 找出所有获得最高票数的玩家
        most_voted_players = [player_id for player_id,
                              count in vote_counts.items() if count == max_votes]
        print(f"主持人：被投票数最多的玩家是 {most_voted_players}。")

        # 处理投票结果
        voted_out_player = None
        if len(most_voted_players) == 1:
            # 只有一个最高票玩家，直接淘汰
            voted_out_player = most_voted_players[0]
            print(f"主持人：玩家 {voted_out_player} 被投票出局。")
            # 从存活玩家列表中移除被淘汰的玩家
            # Create a copy to safely iterate while removing
            for player in self.alive_players[:]:
                if player.player_id == voted_out_player:
                    self.alive_players.remove(player)
                    break
            # 向所有玩家广播投票结果
            self.add_message_for_all_agents(
                role=MessageRole.USER,
                content=f"第{self.day_count}天投票（VOTE）结果：玩家 {voted_out_player} 被投票出局。"
            )
        else:
            # 有多个最高票玩家（平票）
            tie_players_str = ", ".join(most_voted_players)
            print(f"主持人：出现平票情况，玩家 {tie_players_str} 得票数相同。")
            # 根据规则，可能需要重新投票或无人出局
            prompt = f"第{self.day_count}投票（VOTE）阶段出现平票情况，玩家 {tie_players_str} 得票数相同。"
            # 这里可以添加处理平票的逻辑，例如再次投票
            for id in most_voted_players:  # 从平票的id list中遍历提取出每个id元素
                for player in self.alive_players:  # 遍历存活玩家列表
                    if player.player_id == id:  # 如果存活玩家的ID和平票的ID相同
                        defense_content = player.client.get_response(
                            messages=prompt)['content']
                        print(f"Player {player.player_id}({player.role.value}) 辩护：{defense_content}")
                        break

        print("投票阶段结束。")
        # 投票阶段结束后，通常会检查游戏是否结束，然后进入夜晚
        # 这个检查通常在 run_phase 的循环开始时进行，所以这里不需要显式调用 _if_game_over

    def _if_game_over(self):
        """判断游戏是否结束"""
        werewolf_count = 0
        villager_count = 0

        for player in self.alive_players:
            if player.faction == GameFaction.WEREWOLVES:
                werewolf_count += 1
            elif player.faction == GameFaction.VILLAGERS:
                villager_count += 1

        print(f"系统信息：存活狼人数量：{werewolf_count}，存活村民数量：{villager_count}。")

        # 如果狼人数量为0，游戏结束
        if werewolf_count == 0:
            print("村民胜利！")
            return True
        # 如果狼人数量等于村民阵营的数量，游戏结束
        elif werewolf_count == villager_count:
            print("狼人胜利！")
            return True
        # 其他情况，游戏继续
        return False

    def update_day(self):
        """更新游戏天数"""
        self.day_count += 1

    def add_message_for_all_agents(self, role, content):
        for player in self.alive_players:
            player.add_message(
                role=role,
                content=content
            )

    def _set_players_agent(self, players_count=PLAYER_NUMS):
        # 设置游戏环境和玩家
        # 计算村民数量
        villagers_count = players_count - 4  # 1 doctor, 2 werewolves, 1 seer
        if villagers_count < 0:
            raise ValueError(
                "Player count must be at least 4 to have all required roles")

        # 创建角色列表
        player_role_list = [GameRole.DOCTOR] + [GameRole.WEREWOLF] * \
            2 + [GameRole.SEER] + [GameRole.VILLAGER] * villagers_count
        # 随机打乱角色列表
        random.shuffle(player_role_list)

        # 创建玩家ID列表,格式为"ID_X"。
        player_id_list = [f"ID_{i}" for i in range(1, players_count + 1)]

        # 随机选择一个ID作为人类玩家
        human_player_id = random.choice(player_id_list)

        # 创建玩家代理
        agents = []
        for player_id, role in zip(player_id_list, player_role_list):
            # 根据ID创建人类或AI代理
            if player_id == human_player_id:
                # agent = HumanAgent(player_id=player_id, role=role, human_or_ai='Human')
                agent = LLMAgent(player_id=player_id, role=role)
            else:
                agent = LLMAgent(player_id=player_id, role=role)
            agents.append(agent)

        return agents
