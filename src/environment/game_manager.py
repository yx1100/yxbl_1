from src.utils.config import MESSAGES_FILE_PATH
from src.utils.game_enum import GameRole, GamePhase, MessageType, MessageRole
from src.environment.game_state import GameState
from src.utils.rules_prompt import GameRulePrompt
from src.utils.messages_manager import MessagesManager
from src.roles.werewolf import Werewolf
from src.roles.doctor import Doctor
from src.roles.seer import Seer
from src.roles.villager import Villager


class GameManager:
    def __init__(self):
        self.messages_manager = MessagesManager(MESSAGES_FILE_PATH)  # 初始化消息管理器
        self.game_state = GameState()  # 初始化游戏状态

        self.init_players = self.game_state.get_initial_players()  # 游戏初始化，存活玩家列表
        self.init_players_id = self.game_state.get_players_id()  # 存活玩家ID列表
        self.init_players_roles = self.game_state.get_players_role()  # 存活角色列表

        self.day_count = self.game_state.day_count

        self.phase = self.game_state.phase  # 游戏开始时为夜晚阶段

        prompt = f"""本场游戏初始玩家共有{len(self.init_players)}人，分别是{self.init_players_id}。"""
        print(f"提示词：{prompt}")
        self.messages_manager.add_message(
            player_id="system",
            role=GameRole.HOST,
            day_count=0,
            phase=GamePhase.INIT,
            message_type=MessageType.PUBLIC,
            content=prompt
        )
        print(
            f"调试信息：玩家角色分别是：{[role.value for role in self.init_players_roles]}。\n======================\n")

        self.alive_players = self.init_players.copy()
        self.kill_player = None

    def run_phase(self):
        """根据当前阶段运行相应的处理方法"""

        # 1. 判断游戏是否结束
        self._if_game_over()
        # 2. 获取当前存活玩家
        alive_players = self.alive_players
        # 3. 获取当前天数
        current_day_count = self.day_count  # 获取当前游戏天数
        # 4. 获取当前阶段
        current_phase = self.phase  # 获取当前回合
        print(
            f"调试信息：当前是游戏第{current_day_count}天的{current_phase.value}回合。")

        if current_phase == GamePhase.NIGHT:
            self.kill_player = self.night_phase(current_day_count,
                                                alive_players)
        elif current_phase == GamePhase.DAY:
            self.day_phase(current_day_count,
                           self.kill_player,
                           alive_players)
        elif current_phase == GamePhase.VOTE:
            self.vote_phase(current_day_count, alive_players)
            # Return after processing the current phase

    def night_phase(self, day_count, alive_players):
        """处理夜晚阶段"""
        """
        1. 狼人：在场存活的狼人睁眼。如果存活的狼人数量为2，则第1个狼人根据分析，然后决定杀谁。如果第2个狼人同意第1个狼人的决定，则狼人达成共识选定受害者。如果第2个狼人不同意的第1个狼人的决定，则第2个狼人给出分析，然后决定杀谁。如果第1个狼人同意第2个狼人的决定，则狼人达成共识杀害第2个狼人选定的受害者，否则第1个狼人继续给出自己的分析和决定。以此反复5个来回，若狼人们仍无法达成共识选定受害者，则这一夜将没有人被害。如果存活的狼人数量为1，则唯一的狼人决定杀害谁。无论有没有达成共识选定受害者，狼人闭眼。
        2. 医生：医生如果还存活的话，角色为医生的存活玩家选择决定救治在场存活的哪一位玩家。系统将判断，如果医生选择的玩家和狼人杀害的玩家为同一人，则该玩家被救活，这一夜将无人死去。医生闭眼。
        3. 预言家：预言家如果还存活的话，角色为预言家的存活玩家选择查验在场存活的某一位玩家身份。系统将告诉预言家这名玩家的真实游戏身份。预言家闭眼。
        - 如果医生和预言家被杀害，在夜晚阶段仍会有医生和预言家的角色行动阶段，但不会有任何事情发生。
        """
        alive_players_id = [player.player_id for player in alive_players]
        alive_roles = [player.role for player in alive_players]

        print("\n==== 夜晚降临 ====")

        # 1. 获取夜晚阶段的提示词
        phase_prompt = GameRulePrompt().get_phase_prompt(day_count=day_count,
                                                         phase=GamePhase.NIGHT,
                                                         alive_players=alive_players_id)
        print(f"提示词：{phase_prompt}")

        self.messages_manager.add_message(
            player_id="system",
            role=GameRole.HOST,
            day_count=day_count,
            phase=GamePhase.NIGHT,
            message_type=MessageType.PUBLIC,
            content=phase_prompt
        )

        print(f"提示词：存活玩家：{alive_players_id}")
        print(f"调试信息：存活角色：{[role.value for role in alive_roles]}。")

        # 处理狼人袭击、医生救人、预言家查验等行为
        # 1. 狼人阶段
        print("\n==== 狼人阶段 ====")
        kill_player = Werewolf(
            alive_players=alive_players,
            day_count=day_count,
            phase=GamePhase.NIGHT,
            messages_manager=self.messages_manager
        ).do_action(phase_prompt)

        # 2. 医生阶段
        print("\n==== 医生阶段 ====")
        if GameRole.DOCTOR in alive_roles:
            save_player = Doctor(
                alive_players=alive_players,
                day_count=day_count,
                phase=GamePhase.NIGHT,
                messages_manager=self.messages_manager
            ).do_action(phase_prompt)
        else:
            print('医生已经被杀害，跳过医生阶段...')

        # 预言家阶段
        print("\n==== 预言家阶段 ====")
        if GameRole.SEER in alive_roles:
            check_player = Seer(
                alive_players=alive_players,
                day_count=day_count,
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
        print("被杀玩家(公开信息)：", kill_player)
        print("被救玩家(系统信息)：", save_player)
        print("被查玩家(系统信息)：", check_player)
        print("存活玩家(公开信息)：", [
              player.player_id for player in self.alive_players])
        print("存活角色(系统信息)：", [
              player.role.value for player in self.alive_players])

        self.update_phase()
        self.update_day()

        return kill_player

    def day_phase(self, day_count, kill_player, alive_players):
        """处理白天阶段"""
        """
        白天流程：
        1. 所有人睁眼。
        2. 系统宣布昨晚被杀（或救）的人是谁。如果有人被杀害，则被杀害的玩家将退出游戏不能再发言，但该名被杀害玩家的角色身份不会被披露。
        3. 按照存活玩家的ID顺序，每一名玩家将进行分析，表达自己的想法。
        4. 当所有存活玩家按顺序表达完自己的想法后，所有存活玩家将依次投票选择出一名可能是狼人的玩家。
        5. 得票数最多的玩家将被淘汰。若有2名玩家的得票数相同，将重新进行第2轮投票，存活玩家将在这2人中重新进行投票，得票数最多的玩家将被淘汰。如果第2轮投票仍未平票，则不会有玩家被淘汰，游戏进入到下一夜。
        """
        alive_players_id = [player.player_id for player in alive_players]
        alive_roles = [player.role.value for player in alive_players]

        print("\n==== 天亮了 ====")

        last_night_info_prompt = GameRulePrompt().get_last_night_info_prompt(current_day=day_count,
                                                                             killed_player=kill_player,
                                                                             alive_players_id=alive_players_id)
        print(last_night_info_prompt)

        for player in alive_players:
            player.add_message(
                role=MessageRole.USER,
                content=last_night_info_prompt
            )
        self.messages_manager.add_message(
            player_id="system",
            role=GameRole.HOST,
            day_count=day_count,
            phase=GamePhase.DAY,
            message_type=MessageType.PUBLIC,
            content=last_night_info_prompt
        )

        # 宣布夜晚死亡情况
        if kill_player is not None:
            print(f"主持人(公开信息)：昨晚玩家 {kill_player} 被杀害.")
        else:
            print("主持人(公开信息)：昨晚没有人被杀害.")
        print("存活玩家(公开信息)：", alive_players_id)
        print("存活角色(系统信息)：", alive_roles)

        # 玩家讨论
        for player in alive_players:
            # 根据角色类型进行发言
            if player.role == GameRole.WEREWOLF:
                discussion = Werewolf(
                    alive_players=alive_players,
                    day_count=day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).discuss(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 发言：{discussion}")

                for p in alive_players:
                    p.add_message(
                        role=MessageRole.USER,
                        content=f"第{day_count}天白天（DAY）阶段，玩家{player.player_id}的发言内容：{discussion}"
                    )

            elif player.role == GameRole.DOCTOR:
                discussion = Doctor(
                    alive_players=alive_players,
                    day_count=day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).discuss(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 发言：{discussion}")

                for p in alive_players:
                    p.add_message(
                        role=MessageRole.USER,
                        content=f"第{day_count}天白天（DAY）阶段，玩家{player.player_id}的发言内容：{discussion}"
                    )
            elif player.role == GameRole.SEER:
                discussion = Seer(
                    alive_players=alive_players,
                    day_count=day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).discuss(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 发言：{discussion}")

                for p in alive_players:
                    p.add_message(
                        role=MessageRole.USER,
                        content=f"第{day_count}天白天（DAY）阶段，玩家{player.player_id}的发言内容：{discussion}"
                    )
            elif player.role == GameRole.VILLAGER:
                discussion = Villager(
                    alive_players=alive_players,
                    day_count=day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).discuss(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 发言：{discussion}")
                for p in alive_players:
                    p.add_message(
                        role=MessageRole.USER,
                        content=f"第{day_count}天白天（DAY）阶段，玩家{player.player_id}的发言内容：{discussion}"
                    )
            else:
                raise ValueError(
                    f"Invalid role: {player.role.value}. Please check the game setup.")

        self.update_phase()

    def vote_phase(self, day_count, alive_players):  # TODO
        """处理投票阶段"""
        print("\n==== 投票阶段 ====")
        # 收集所有玩家的投票

        vote_result = []
        for player in alive_players:
            if player.role == GameRole.WEREWOLF:
                vote = Werewolf(
                    alive_players=alive_players,
                    day_count=day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).vote(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 投票：{vote}")
                vote_result.append(vote)
                for p in alive_players:
                    p.add_message(
                        role=MessageRole.USER,
                        content=f"第{day_count}天投票（VOTE）阶段，玩家{player.player_id}选择投出玩家是：{vote}。"
                    )
            elif player.role == GameRole.DOCTOR:
                vote = Doctor(
                    alive_players=alive_players,
                    day_count=day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).vote(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 投票：{vote}")
                vote_result.append(vote)
                for p in alive_players:
                    p.add_message(
                        role=MessageRole.USER,
                        content=f"第{day_count}天投票（VOTE）阶段，玩家{player.player_id}选择投出玩家是：{vote}。"
                    )
            elif player.role == GameRole.SEER:
                vote = Seer(
                    alive_players=alive_players,
                    day_count=day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).vote(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 投票：{vote}")
                vote_result.append(vote)
                for p in alive_players:
                    p.add_message(
                        role=MessageRole.USER,
                        content=f"第{day_count}天投票（VOTE）阶段，玩家{player.player_id}选择投出玩家是：{vote}。"
                    )
            elif player.role == GameRole.VILLAGER:
                vote = Villager(
                    alive_players=alive_players,
                    day_count=day_count,
                    phase=GamePhase.DAY,
                    messages_manager=self.messages_manager
                ).vote(player.player_id)
                print(
                    f"Player {player.player_id}({player.role.value}) 投票：{vote}")
                vote_result.append(vote)
                for p in alive_players:
                    p.add_message(
                        role=MessageRole.USER,
                        content=f"第{day_count}天投票（VOTE）阶段，玩家{player.player_id}选择投出玩家是：{vote}。"
                    )
            else:
                raise ValueError(
                    f"Invalid role: {player.role}. Please check the game setup.")
        # 处理投票结果
        print("投票结果：", vote_result)

    def _if_game_over(self):
        """判断游戏是否结束"""
        pass

    def update_day(self):
        """更新游戏天数"""
        self.day_count += 1

    def update_phase(self):
        """
        更新游戏阶段
        :param phase: 游戏阶段
        :return: None
        """
        if self.phase == GamePhase.NIGHT:
            self.phase = GamePhase.DAY
        elif self.phase == GamePhase.DAY:
            self.phase = GamePhase.VOTE
        elif self.phase == GamePhase.VOTE:
            self.phase = GamePhase.NIGHT
        else:
            raise ValueError(
                "Invalid game phase. Please check the game setup.")
