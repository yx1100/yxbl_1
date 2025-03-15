from .role import Role

class Villager(Role):
    def __init__(self, player_id, name="村民"):
        super().__init__(player_id, name)
        self.role_type = "villager"
        self.team = "villager"  # 好人阵营
        
    def use_ability(self, target=None):
        """村民没有特殊能力，此方法仅为接口统一
        
        Returns:
            dict: 包含能力使用结果的字典
        """
        return {
            "success": False, 
            "message": "村民没有特殊能力"
        }