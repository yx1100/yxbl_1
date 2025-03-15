from .role import Role

class Werewolf(Role):
    def __init__(self, player_id, name="狼人"):
        super().__init__(player_id, name)
        self.role_type = "werewolf"
        self.team = "werewolf"  # 狼人阵营
        
    def use_ability(self, target):
        """狼人能力：选择一名玩家击杀
        
        Args:
            target: 目标玩家的ID
            
        Returns:
            dict: 包含能力使用结果的字典
        """
        if not self.is_alive:
            return {"success": False, "message": "你已经死亡，无法使用能力"}
            
        return {
            "success": True, 
            "type": "kill", 
            "source": self.player_id,
            "target": target, 
            "message": f"狼人选择了击杀玩家 {target}"
        }