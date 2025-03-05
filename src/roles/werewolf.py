import random
from ..agents.base_agent import BaseAgent
from ..utils.constants import Roles

class WerewolfAgent(BaseAgent):
    def __init__(self, player_id, role):
        super().__init__(player_id, role)
        self.known_werewolves = []  # 记录知道的其他狼人
        self.kill_history = []  # 记录攻击历史
        self.target_preference = {}  # 目标偏好
        
    def select_action(self, observation, valid_actions):
        """狼人决策逻辑"""
        if not valid_actions:
            return None
            
        # 初始化其他狼人信息（如果是第一次）
        if not self.known_werewolves and "werewolves" in observation:
            self.known_werewolves = [w for w in observation["werewolves"] if w != self.player_id]
            
        # 分析目标价值
        target_values = self._evaluate_targets(observation, valid_actions)
        
        # 选择价值最高的目标
        if target_values:
            target = max(target_values, key=target_values.get)
        else:
            target = random.choice(valid_actions)
            
        self.kill_history.append(target)
        
        return {
            "player_id": self.player_id,
            "target_id": target,
            "action_type": "kill"
        }
    
    def _evaluate_targets(self, observation, valid_targets):
        """评估目标价值"""
        target_values = {}
        
        for target in valid_targets:
            value = 10  # 基础价值
            
            # 避免攻击已知的狼人
            if target in self.known_werewolves:
                continue
                
            # 如果有关于目标角色的信息
            if "known_roles" in observation and target in observation["known_roles"]:
                role = observation["known_roles"][target]
                if role == Roles.SEER:
                    value += 30  # 预言家是高价值目标
                elif role == Roles.DOCTOR:
                    value += 25  # 医生也是高价值目标
                    
            # 根据投票行为调整价值
            if "vote_history" in observation:
                for vote in observation["vote_history"]:
                    if vote["voter"] == target and vote["target"] in self.known_werewolves:
                        value += 15  # 增加投票过狼人的玩家价值
                        
            target_values[target] = value
            
        return target_values