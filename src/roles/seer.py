import random
from ..agents.base_agent import BaseAgent
from ..utils.constants import Roles

class SeerAgent(BaseAgent):
    def __init__(self, player_id, role):
        super().__init__(player_id, role)
        self.checked_players = {}  # 记录已查验的玩家
        self.suspicious_players = []  # 记录可疑玩家
        
    def select_action(self, observation, valid_actions):
        """预言家决策逻辑"""
        if not valid_actions:
            return None
            
        # 过滤掉已经查验过的玩家
        unchecked = [p for p in valid_actions if p not in self.checked_players]
        
        if not unchecked:  # 如果所有人都查验过了
            target = random.choice(valid_actions)
        elif self.suspicious_players:  # 优先查验可疑玩家
            suspects = [p for p in self.suspicious_players if p in unchecked]
            target = suspects[0] if suspects else random.choice(unchecked)
        else:  # 随机选择未查验的玩家
            target = random.choice(unchecked)
            
        return {
            "player_id": self.player_id,
            "target_id": target,
            "action_type": "check"
        }
        
    def update_knowledge(self, target_id, is_werewolf):
        """更新知识库"""
        self.checked_players[target_id] = is_werewolf
        
        if is_werewolf:
            if target_id not in self.suspicious_players:
                self.suspicious_players.append(target_id)
                
    def analyze_votes(self, vote_history):
        """分析投票模式寻找可疑玩家"""
        vote_patterns = {}
        
        for vote in vote_history:
            voter = vote["voter"]
            target = vote["target"]
            
            # 如果投票目标是已知好人，记为可疑行为
            if target in self.checked_players and not self.checked_players[target]:
                if voter not in self.suspicious_players and voter not in self.checked_players:
                    self.suspicious_players.append(voter)