import numpy as np

class BaseAgent:
    def __init__(self, player_id, role):
        self.player_id = player_id
        self.role = role
        self.memory = []  # 存储历史观察和动作
        
    def select_action(self, observation, valid_actions):
        """选择行动"""
        raise NotImplementedError
        
    def update_policy(self, state, action, reward, next_state):
        """更新策略"""
        pass
        
    def remember(self, observation, action, reward, next_observation, done):
        """存储经验"""
        self.memory.append((observation, action, reward, next_observation, done))