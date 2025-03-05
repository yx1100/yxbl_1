import random
from .utils.constants import Roles

class GameState:
    def __init__(self, num_players, roles_config):
        self.num_players = num_players
        self.roles = self._assign_roles(roles_config)
        self.alive_players = list(range(num_players))
        self.vote_history = []
        self.public_information = {}  # 所有玩家可见信息
        self.private_information = {}  # 每个玩家特有信息
        
    def _assign_roles(self, roles_config):
        """分配角色"""
        all_roles = []
        for role, count in roles_config.items():
            all_roles.extend([role] * count)
            
        if len(all_roles) != self.num_players:
            raise ValueError("Role configuration doesn't match player count")
            
        random.shuffle(all_roles)
        return all_roles
        
    def is_player_alive(self, player_id):
        """检查玩家是否存活"""
        return player_id in self.alive_players
        
    def get_role(self, player_id):
        """获取玩家角色"""
        return self.roles[player_id]
        
    def get_alive_players_except(self, exclude_ids):
        """获取除指定ID外的所有存活玩家"""
        return [p for p in self.alive_players if p not in exclude_ids]
        
    def count_alive_players(self):
        """统计存活玩家数量"""
        return len(self.alive_players)
        
    def count_alive_by_role(self, role):
        """统计特定角色的存活数量"""
        return sum(1 for p in self.alive_players if self.roles[p] == role)
        
    def kill_player(self, player_id):
        """杀死指定玩家"""
        if player_id in self.alive_players:
            self.alive_players.remove(player_id)
            return True
        return False
        
    def record_vote(self, voter, target):
        """记录投票"""
        self.vote_history.append({"day": len(self.vote_history) + 1, 
                                 "voter": voter, 
                                 "target": target})
                                 
    def get_observation(self):
        """获取当前状态的观察"""
        # 返回一个适合输入给智能体的状态表示
        return {
            "alive_players": self.alive_players,
            "public_information": self.public_information,
            # 其他信息...
        }
    
        # 添加到game_state.py中
    def get_role_specific_observation(self, player_id):
        """为不同角色提供特定观察"""
        base_obs = self.get_observation()  # 基本观察
        role = self.get_role(player_id)
        
        if role == Roles.WEREWOLF:
            # 狼人知道其他狼人
            werewolves = [i for i, r in enumerate(self.roles) if r == Roles.WEREWOLF and i in self.alive_players]
            base_obs["werewolves"] = werewolves
            
        elif role == Roles.SEER:
            # 预言家知道已查验的玩家
            if player_id in self.private_information:
                base_obs["checked_players"] = self.private_information[player_id].get("checked_players", {})
                
        return base_obs