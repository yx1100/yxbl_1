from .game_state import GameState
from .utils.constants import GamePhase, Roles

class WerewolfGameEnv:
    def __init__(self, num_players, roles_config):
        self.num_players = num_players
        self.roles_config = roles_config
        self.state = None
        self.current_phase = None
        self.day_count = 0
        
    def reset(self):
        """重置游戏环境"""
        self.state = GameState(self.num_players, self.roles_config)
        self.current_phase = GamePhase.NIGHT_WEREWOLF
        self.day_count = 1
        return self.state.get_observation()
        
    def step(self, action):
        """执行动作并返回新状态"""
        # 验证动作合法性
        if not self._is_valid_action(action):
            return self.state.get_observation(), -10, False, {"error": "Invalid action"}
        
        # 执行动作
        reward = self._execute_action(action)
        
        # 检查游戏是否结束
        done = self._check_game_over()
        
        # 如果未结束，进入下一阶段
        if not done:
            self._move_to_next_phase()
            
        return self.state.get_observation(), reward, done, {"phase": self.current_phase}
        
    def get_valid_actions(self, player_id):
        """获取当前玩家可执行的合法动作"""
        if not self.state.is_player_alive(player_id):
            return []
            
        if self.current_phase == GamePhase.NIGHT_WEREWOLF:
            if self.state.get_role(player_id) == Roles.WEREWOLF:
                return self.state.get_alive_players_except([player_id])
            return []
        # 添加其他阶段的合法动作...
        
    def _is_valid_action(self, action):
        """检查动作是否合法"""
        player_id = action.get("player_id")
        target_id = action.get("target_id")
        
        # 基本检查
        if not self.state.is_player_alive(player_id):
            return False
            
        # 根据不同阶段进行检查
        # ...
        
        return True
        
    def _execute_action(self, action):
        """执行动作并返回奖励"""
        # 根据不同阶段和角色执行不同的动作
        # ...
        
        return 0  # 默认奖励
        
    def _check_game_over(self):
        """检查游戏是否结束"""
        werewolf_count = self.state.count_alive_by_role(Roles.WEREWOLF)
        villager_count = self.state.count_alive_players() - werewolf_count
        
        if werewolf_count == 0:
            return True  # 好人胜利
        if werewolf_count >= villager_count:
            return True  # 狼人胜利
            
        return False
        
    def _move_to_next_phase(self):
        """进入下一个游戏阶段"""
        # 根据当前阶段确定下一阶段
        # ...