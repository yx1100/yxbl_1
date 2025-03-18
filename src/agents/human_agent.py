from agents.base_agent import BaseAgent

class HumanAgent(BaseAgent):
    def __init__(self, player_id, role, faction):
        # 调用父类的初始化方法，传入 player_id, role, faction
        super().__init__(player_id, role, faction, human_or_ai="Human")
        
    def observe(self, game_state):
        # 观察游戏状态，可以覆盖父类方法
        pass
        
    def act(self, valid_actions):
        # 做出决策，可以覆盖父类方法
        pass
