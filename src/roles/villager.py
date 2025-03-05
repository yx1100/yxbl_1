import random
from ..agents.base_agent import BaseAgent

class VillagerAgent(BaseAgent):
    def __init__(self, player_id, role):
        super().__init__(player_id, role)
        self.suspicion_levels = {}  # 对其他玩家的怀疑程度
        self.trusted_players = []   # 相信的玩家
        
    def select_action(self, observation, valid_actions):
        """村民决策逻辑"""
        if not valid_actions:
            return None
            
        # 只在白天投票阶段有行动
        if observation.get("phase") == "DAY_VOTE":
            # 更新怀疑度
            self._update_suspicion(observation)
            
            # 找出最可疑的玩家
            suspicious_players = {p: level for p, level in self.suspicion_levels.items() 
                                if p in valid_actions}
                                
            if suspicious_players:
                target = max(suspicious_players, key=suspicious_players.get)
            else:
                target = random.choice(valid_actions)
                
            return {
                "player_id": self.player_id,
                "target_id": target,
                "action_type": "vote"
            }
            
        return None
        
    def _update_suspicion(self, observation):
        """更新对玩家的怀疑程度"""
        # 初始化
        for player in range(observation.get("num_players", 0)):
            if player != self.player_id and player not in self.suspicion_levels:
                self.suspicion_levels[player] = 10  # 基础怀疑度
                
        # 根据死亡信息更新
        if "deaths" in observation:
            for death in observation["deaths"]:
                # 尝试根据死亡模式分析
                if death.get("cause") == "werewolf":
                    # 分析投票模式，投死者投票的人更可疑
                    if "vote_history" in observation:
                        for vote in observation["vote_history"]:
                            if vote["target"] == death["player_id"]:
                                self.suspicion_levels[vote["voter"]] = self.suspicion_levels.get(vote["voter"], 10) + 15
                                
        # 根据公开信息更新
        if "public_info" in observation:
            for info in observation["public_info"]:
                if info["type"] == "seer_result":
                    # 预言家的信息可信度高
                    if info["is_werewolf"]:
                        self.suspicion_levels[info["target"]] = 100  # 被预言家确认为狼人
                    else:
                        self.trusted_players.append(info["target"])
                        self.suspicion_levels[info["target"]] = 0  # 被预言家确认为好人
                        
        # 根据投票历史分析
        if "vote_history" in observation:
            for vote in observation["vote_history"]:
                # 投票给可信玩家的人更可疑
                if vote["target"] in self.trusted_players:
                    self.suspicion_levels[vote["voter"]] = self.suspicion_levels.get(vote["voter"], 10) + 20