from src.agents.base_agent import BaseAgent


class HumanAgent(BaseAgent):
    def __init__(self, player_id, role, faction):
        # 调用父类的初始化方法，传入 player_id, role, faction
        super().__init__(player_id, role, faction)
