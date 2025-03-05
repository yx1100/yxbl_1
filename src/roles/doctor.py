import random
from ..agents.base_agent import BaseAgent
from ..utils.constants import Roles

class DoctorAgent(BaseAgent):
    def __init__(self, player_id, role):
        super().__init__(player_id, role)
        self.last_saved = None  # 记录上一次救的玩家
        self.self_save_count = 0  # 记录自救次数
        self.max_self_save = 1  # 最多自救一次
        self.target_value = {}  # 不同玩家的保护价值
        
    def select_action(self, observation, valid_actions):
        """医生决策逻辑"""
        if not valid_actions:
            return None
            
        # 评估保护价值
        target_values = self._evaluate_protection_value(observation, valid_actions)
        
        # 避免连续两晚救同一个人
        if self.last_saved in target_values:
            target_values[self.last_saved] *= 0.5
            
        # 确定是否可以自救
        can_self_save = (self.player_id in valid_actions and 
                         self.self_save_count < self.max_self_save)
                         
        # 根据情况选择目标
        if not target_values:
            # 没有评估结果，随机选择或自救
            if can_self_save:
                target = self.player_id
                self.self_save_count += 1
            else:
                potential_targets = [t for t in valid_actions if t != self.last_saved]
                target = random.choice(potential_targets) if potential_targets else random.choice(valid_actions)
        else:
            # 考虑自救情况
            if can_self_save:
                target_values[self.player_id] = max(target_values.values()) * 1.2  # 自救优先级提高
                
            # 选择价值最高的目标
            target = max(target_values, key=target_values.get)
            if target == self.player_id:
                self.self_save_count += 1
                
        self.last_saved = target
        
        return {
            "player_id": self.player_id,
            "target_id": target,
            "action_type": "save"
        }
        
    def _evaluate_protection_value(self, observation, valid_targets):
        """评估保护价值"""
        values = {}
        
        for target in valid_targets:
            # 避免连续两晚救同一人
            if target == self.last_saved:
                continue
                
            value = 10  # 基础价值
            
            # 已知角色的价值评估
            if "known_roles" in observation and target in observation["known_roles"]:
                role = observation["known_roles"][target]
                if role == Roles.SEER:
                    value += 30  # 预言家非常重要
                elif role == Roles.DOCTOR and target == self.player_id:
                    value += 25  # 自己也很重要
                    
            # 基于发言和行为的价值评估
            if "vote_history" in observation:
                # 计算每个玩家收到的票数，多人投票的可能是狼人
                vote_counts = {}
                for vote in observation["vote_history"]:
                    if vote["target"] not in vote_counts:
                        vote_counts[vote["target"]] = 0
                    vote_counts[vote["target"]] += 1
                
                # 经常被投票的人可能更需要保护
                if target in vote_counts and vote_counts[target] > 1:
                    value += 10 * vote_counts[target]
                
            values[target] = value
            
        return values