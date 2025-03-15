from .role import Role

class Seer(Role):
    def __init__(self, player_id, name="预言家"):
        super().__init__(player_id, name)
        self.role_type = "seer"
        self.team = "villager"  # 好人阵营
        
    def use_ability(self, target):
        """预言家能力：查验一名玩家的身份
        
        Args:
            target: 目标玩家的ID
            
        Returns:
            dict: 包含能力使用结果的字典，需要游戏环境填充目标的阵营信息
        """
        if not self.is_alive:
            return {"success": False, "message": "你已经死亡，无法使用能力"}
            
        return {
            "success": True, 
            "type": "check", 
            "source": self.player_id,
            "target": target, 
            "message": f"预言家选择查验玩家 {target}",
            "result": None  # 这个结果需要由游戏环境填充
        }