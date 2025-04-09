import sys
from src.utils.config import MESSAGES_FILE_PATH
from src.environment.game_state import GameState
from src.utils.rules_prompt import GameRulePrompt
from src.utils.messages_manager import MessagesManager
from src.roles import Werewolf
from src.roles import Doctor
from src.roles import Seer


class GameManager:
    def __init__(self):
        self.messages_manager = MessagesManager(MESSAGES_FILE_PATH)  # 初始化消息管理器
        self.game_state = GameState()  # 初始化游戏状态

        self.init_alive_players = self.game_state.get_alive_players() # 游戏初始化，存活玩家列表
        self.init_alive_players_id = [player.player_id for player in self.init_alive_players] # 存活玩家ID列表
        self.init_alive_roles = self.game_state.get_alive_players_role() # 存活角色列表

        prompt = f"""本场游戏初始玩家共有{len(self.init_alive_players)}人，分别是{self.init_alive_players_id}。"""
        print(prompt)
        self.messages_manager.add_message(
            player_id="system",
            role='Host',
            day_count=0,
            phase="INIT",
            message_type='PUBLIC',
            content=prompt
        )
        print(f"玩家角色分别是：{self.init_alive_roles}。\n======================\n")

        self.alive_players = self.init_alive_players
        self.alive_players_id = self.init_alive_players_id
        self.alive_roles = self.init_alive_roles
   
        self.kill_player = None
        self.save_player = None
        self.check_player = None

    def run_phase(self):
        """根据当前阶段运行相应的处理方法"""
        # 确保游戏状态已初始化
        if self.game_state is None:
            raise RuntimeError("Game state not initialized. Please setup game first.")

        # 1. 判断游戏是否结束
        self._if_game_over()

        # 2. 获取当前存活玩家
        alive_players = self.game_state.get_alive_players()
        alive_players_id = [player.player_id for player in alive_players]  # 获取存活玩家ID列表
        # alive_roles = self.game_state.get_alive_players_role()  # 获取存活玩家角色列表
        # 3. 获取当前天数
        current_day_count = self.game_state.get_day_count()  # 获取当前游戏天数
        print(f"当前游戏天数：{self.game_state.day_count}")
        # 4. 获取当前阶段
        current_phase = self.game_state.get_current_phase()
        print(f"当前游戏阶段：{current_phase}")
        # 5. 获取当前阶段提示词
        phase_prompt = GameRulePrompt().get_phase_prompt(day_count=current_day_count, phase=current_phase, alive_players=alive_players_id)
        print(f"当前阶段提示词：{phase_prompt}")

        self.messages_manager.add_message(
            player_id="system",
            role='Host',
            day_count=current_day_count,
            phase=current_phase,
            message_type='PUBLIC',
            content=phase_prompt
        )

        # # 执行当前阶段的逻辑
        # if current_phase == "NIGHT":
        #     self.night_phase(phase_prompt)
        # elif current_phase == "DAY":
        #     self.day_phase()
        # elif current_phase == "VOTE":
        #     self.vote_phase()

        self.night_phase(phase_prompt)

        self.day_phase()

        # 推进到下一阶段
        # self.game_state.advance_phase()

        return None

    def night_phase(self, phase_prompt):
        """处理夜晚阶段"""
        """
        1. 狼人：在场存活的狼人睁眼。如果存活的狼人数量为2，则第1个狼人根据分析，然后决定杀谁。如果第2个狼人同意第1个狼人的决定，则狼人达成共识选定受害者。如果第2个狼人不同意的第1个狼人的决定，则第2个狼人给出分析，然后决定杀谁。如果第1个狼人同意第2个狼人的决定，则狼人达成共识杀害第2个狼人选定的受害者，否则第1个狼人继续给出自己的分析和决定。以此反复5个来回，若狼人们仍无法达成共识选定受害者，则这一夜将没有人被害。如果存活的狼人数量为1，则唯一的狼人决定杀害谁。无论有没有达成共识选定受害者，狼人闭眼。
        2. 医生：医生如果还存活的话，角色为医生的存活玩家选择决定救治在场存活的哪一位玩家。系统将判断，如果医生选择的玩家和狼人杀害的玩家为同一人，则该玩家被救活，这一夜将无人死去。医生闭眼。
        3. 预言家：预言家如果还存活的话，角色为预言家的存活玩家选择查验在场存活的某一位玩家身份。系统将告诉预言家这名玩家的真实游戏身份。预言家闭眼。
        - 如果医生和预言家被杀害，在夜晚阶段仍会有医生和预言家的角色行动阶段，但不会有任何事情发生。
        """
        # 确保游戏状态已初始化
        if self.game_state is None:
            raise RuntimeError("Game state not initialized. Please setup game first.")

        print("\n==== 夜晚降临 ====")
        # 处理狼人袭击、医生救人、预言家查验等行为

        print("存活玩家：", self.alive_players_id)
        print("存活角色：", self.alive_roles)

        # 1. 狼人阶段
        print("\n==== 狼人阶段 ====")
        role_prompt = GameRulePrompt().get_response_format_prompt("werewolf")
        self.kill_player, M1, M2 = Werewolf(self.game_state, self.messages_manager).do_action(role_prompt, phase_prompt)

        # 2. 医生阶段
        print("\n==== 医生阶段 ====")
        if 'doctor' in self.alive_roles:
            role_prompt = GameRulePrompt().get_response_format_prompt("doctor")
            self.save_player = Doctor(self.game_state, self.messages_manager).do_action(role_prompt, phase_prompt)
        else:
            print('医生已经被杀害，跳过医生阶段...')

        # 预言家阶段
        print("\n==== 预言家阶段 ====")
        if 'seer' in self.alive_roles:
            role_prompt = GameRulePrompt().get_response_format_prompt("seer")
            self.check_player = Seer(self.game_state, self.messages_manager).do_action(role_prompt, phase_prompt)
        else:
            print('预言家已经被杀害，跳过预言家阶段...')

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

        self.update_alive_players()

        print("\n==== 夜晚总结 ====")
        print("存活玩家(公开信息)：", self.alive_players_id)
        print("被杀玩家(公开信息)：", self.kill_player)
        print("被救玩家(系统信息)：", self.save_player)
        print("被查玩家(系统信息)：", self.check_player)
        print("存活角色(系统信息)：", self.alive_roles)

        self._if_game_over()

        return None

    def day_phase(self):
        """处理白天阶段"""
        """
        白天流程：
        1. 所有人睁眼。
        2. 系统宣布昨晚被杀（或救）的人是谁。如果有人被杀害，则被杀害的玩家将退出游戏不能再发言，但该名被杀害玩家的角色身份不会被披露。
        3. 按照存活玩家的ID顺序，每一名玩家将进行分析，表达自己的想法。
        4. 当所有存活玩家按顺序表达完自己的想法后，所有存活玩家将依次投票选择出一名可能是狼人的玩家。
        5. 得票数最多的玩家将被淘汰。若有2名玩家的得票数相同，将重新进行第2轮投票，存活玩家将在这2人中重新进行投票，得票数最多的玩家将被淘汰。如果第2轮投票仍未平票，则不会有玩家被淘汰，游戏进入到下一夜。
        """
        # 确保游戏状态已初始化
        if self.game_state is None:
            raise RuntimeError(
                "Game state not initialized. Please setup game first.")
        
        self.game_state.update_day_count()
        print("\n==== 天亮了 ====")

        last_night_info_prompt = GameRulePrompt().get_last_night_info_prompt(current_day=self.game_state.day_count, killed_player=self.kill_player, alive_players_id=self.alive_players_id)
        print(last_night_info_prompt)

        # 宣布夜晚死亡情况
        if self.kill_player is not None:
            print(f"主持人(公开信息)：昨晚玩家 {self.kill_player} 被杀害.")
        else:
            print("主持人(公开信息)：昨晚没有人被杀害.")
        print("存活玩家(公开信息)：", self.alive_players_id)
        print("存活角色(系统信息)：", self.alive_roles)

        # 玩家讨论
        for player in self.game_state.alive_players:
            if player.role == 'werewolf':
                print(f"Player {player.player_id}({player.role}) 发言：...")
            elif player.role == 'doctor':
                print(f"Player {player.player_id}({player.role}) 发言：...")
            elif player.role == 'seer':
                print(f"Player {player.player_id}({player.role}) 发言：...")
            elif player.role == 'villager':
                print(f"Player {player.player_id}({player.role}) 发言：...")
            else:
                raise ValueError(f"Invalid role: {player.role}. Please check the game setup.")

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
            if player.role == 'werewolf':
                print(f"Player {player.player_id}({player.role}) 发言：...")
            elif player.role == 'doctor':
                print(f"Player {player.player_id}({player.role}) 发言：...")
            elif player.role == 'seer':
                print(f"Player {player.player_id}({player.role}) 发言：...")
            elif player.role == 'villager':
                print(f"Player {player.player_id}({player.role}) 发言：...")
            else:
                raise ValueError(f"Invalid role: {player.role}. Please check the game setup.")
    
            # TODO: 此处每位玩家选择一名投票对象
        # 处理投票结果

    def _if_game_over(self):
        """判断游戏是否结束"""
        alive_roles = self.game_state.get_alive_players_role()  # 获取存活玩家角色列表

        werewolf_count = alive_roles.count('werewolf')
        villager_count = len(alive_roles) - werewolf_count

        if werewolf_count == 0:
            # 狼人全部死亡，村民阵营胜利
            self.game_state.game_is_over = True
            self.game_state.winner = "VILLAGERS"
            print("\n==== 游戏结束 ====")
            print("村民阵营胜利!")
            print("游戏结束！")
            sys.exit(0)  # 0表示正常退出，其他数字表示错误代码
        elif werewolf_count >= villager_count:
            # 狼人数量等于或超过其他玩家，狼人阵营胜利
            self.game_state.game_is_over = True
            self.game_state.winner = "WEREWOLVES"
            print("\n==== 游戏结束 ====")
            print("狼人阵营胜利!")
            print("游戏结束！")
            sys.exit(0)  # 0表示正常退出，其他数字表示错误代码
        else:
            # 游戏继续
            return False
        
    def update_alive_players(self):
        """
        更新存活玩家列表
        :return: 无有效返回值，仅打印信息
        """
        self.alive_players = self.game_state.get_alive_players()
        self.alive_players_id = [player.player_id for player in self.alive_players]  # 获取存活玩家ID列表
        self.alive_roles = self.game_state.get_alive_players_role()  # 获取存活玩家角色列表
