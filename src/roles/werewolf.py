import random
from ..agents.base_agent import BaseAgent

class WerewolfAgent(BaseAgent):
    def select_action(self, observation, valid_actions):
        """狼人决策逻辑"""
        if not valid_actions:
            return None
            
        # 简单策略：随机选择一个目标
        # 可以替换为更复杂的策略，如基于历史行为的策略
        target = random.choice(valid_actions)
        
        return {
            "player_id": self.player_id,
            "target_id": target,
            "action_type": "kill"
        }