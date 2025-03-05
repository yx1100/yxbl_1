from .environment import WerewolfGameEnv
from .utils.constants import Roles, GamePhase
from .roles.werewolf import WerewolfAgent
from .roles.villager import VillagerAgent
from .roles.seer import SeerAgent
from .roles.doctor import DoctorAgent  # 导入医生智能体

class GameManager:
    def __init__(self, num_players, role_config):
        self.env = WerewolfGameEnv(num_players, role_config)
        self.agents = self._create_agents()
        self.current_phase = None
        
    def _create_agents(self):
        """根据角色创建对应的智能体"""
        agents = []
        observation = self.env.reset()
        
        for i in range(self.env.num_players):
            role = self.env.state.get_role(i)
            if role == Roles.WEREWOLF:
                agents.append(WerewolfAgent(i, role))
            elif role == Roles.SEER:
                agents.append(SeerAgent(i, role))
            elif role == Roles.DOCTOR:
                agents.append(DoctorAgent(i, role))
            else:
                agents.append(VillagerAgent(i, role))
                
        return agents
        
    def run_game(self, max_days=10):
        """运行完整的游戏流程"""
        observation = self.env.reset()
        done = False
        day = 1
        
        while not done and day <= max_days:
            print(f"=== 第 {day} 天 ===")
            
            # 运行每个阶段
            while self.env.current_phase != GamePhase.DAY_ANNOUNCE and not done:
                phase_actions = self.run_phase()
                for action in phase_actions:
                    if action:
                        new_observation, reward, done, info = self.env.step(action)
                        if done:
                            break
            
            # 白天阶段
            while self.env.current_phase != GamePhase.NIGHT_WEREWOLF and not done:
                phase_actions = self.run_phase()
                for action in phase_actions:
                    if action:
                        new_observation, reward, done, info = self.env.step(action)
                        if done:
                            break
            
            day += 1
            
        self._announce_winner()
        
    def run_phase(self):
        """运行特定游戏阶段，收集所有智能体的动作"""
        current_phase = self.env.current_phase
        phase_actions = []
        
        for agent in self.agents:
            player_id = agent.player_id
            
            # 检查是否是当前玩家的行动阶段
            if self.env.state.is_player_alive(player_id):
                valid_actions = self.env.get_valid_actions(player_id)
                
                if valid_actions:
                    observation = self.env.state.get_observation()
                    action = agent.select_action(observation, valid_actions)
                    phase_actions.append(action)
                    
        return phase_actions
        
    def _announce_winner(self):
        """宣布胜利方"""
        werewolf_count = self.env.state.count_alive_by_role(Roles.WEREWOLF)
        
        if werewolf_count == 0:
            print("好人阵营胜利！")
        else:
            print("狼人阵营胜利！")