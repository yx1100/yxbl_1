from .role import Role

class Doctor(Role):
    def __init__(self, player_id, name="医生"):
        super().__init__(player_id, name)
        self.role_type = "doctor"
        self.team = "villager"  # 好人阵营
        self.self_saves = 0  # 记录自救次数（可以用于限制自救）
        
    def use_ability(self, target):
        """医生能力：选择一名玩家进行治疗
        
        Args:
            target: 目标玩家的ID
            
        Returns:
            dict: 包含能力使用结果的字典
        """
        if not self.is_alive:
            return {"success": False, "message": "你已经死亡，无法使用能力"}
            
        # 可以添加自救限制逻辑
        if target == self.player_id:
            self.self_saves += 1
            
        return {
            "success": True, 
            "type": "save", 
            "source": self.player_id,
            "target": target, 
            "message": f"医生选择了治疗玩家 {target}"
        }