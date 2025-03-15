class Role:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.is_alive = True
        
    def use_ability(self, target):
        # 使用角色特殊能力
        pass