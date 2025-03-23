import random
from src.environment.game_state import GameState
from src.agents.llm_agent import LLMAgent
from src.agents.human_agent import HumanAgent


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

        current_phase = self.game_state.get_current_phase()

        # 执行当前阶段的逻辑
        if current_phase == "NIGHT":
            self.night_phase()
        elif current_phase == "DAY":
            self.day_phase()
        elif current_phase == "VOTE":
            self.vote_phase()

        # 推进到下一阶段
        next_phase = self.game_state.advance_phase()
        return next_phase

    def night_phase(self):
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

        alive_players = self.game_state.get_alive_players()  # 获取存活玩家列表
        alive_roles = self.game_state.get_alive_players_role()  # 获取存活玩家角色列表

        # 狼人阶段
        werewolf_count = alive_roles.count('werewolf')  # 统计'werewolf'的数量
        if werewolf_count == 2:
            # 两个狼人
            print("两个狼人")
            self.kill_player = "ID_1"
        elif werewolf_count == 1:
            # 一个狼人
            print("一个狼人")
            self.kill_player = "ID_1"
        else:
            raise RuntimeError("Invalid werewolf count.")

        # 医生阶段
        if 'doctor' in alive_roles:
            print('一个医生')
            self.save_player = "ID_2"
        else:
            print('医生已经被杀害，跳过医生阶段...')

        # 处理狼人杀人结果
        if self.kill_player == self.save_player:
            self.kill_player = None
        else:
            # Find the player with matching player_id and remove them
            for player in self.game_state.alive_players[:]:  # Create a copy for safe iteration
                if player.player_id == self.kill_player:
                    self.game_state.alive_players.remove(player)
                    self.game_state.alive_roles.remove(player.role)
                    break
        self.save_player = None

        # 预言家阶段
        if 'seer' in alive_roles:
            print('一个预言家')
        else:
            print('预言家已经被杀害，跳过预言家阶段...')


        
        print("被杀玩家：", self.kill_player)
        print("被救玩家：", self.save_player)
        print("被查玩家：", self.check_player)
        print("存活玩家：", self.game_state.alive_players)
        print("存活玩家角色：", self.game_state.alive_roles)

        self.end_game()

        return None

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
