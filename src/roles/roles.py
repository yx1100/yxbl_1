class WerewolfAgent(BaseAgent):
    def select_action(self, state, valid_actions):
        """狼人特定的决策逻辑"""
        pass

# filepath: src/roles/villager.py
class VillagerAgent(BaseAgent):
    def select_action(self, state, valid_actions):
        """村民特定的决策逻辑"""
        pass

# filepath: src/roles/seer.py
class SeerAgent(BaseAgent):
    def select_action(self, state, valid_actions):
        """预言家特定的决策逻辑"""
        pass