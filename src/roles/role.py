class Role:
    def __init__(self, name, faction):
        self.name = name
        self.faction = faction
        self.role_prompt = '你是一名狼人杀游戏的玩家。'  # 角色提示信息
        self.villager_faction_rule_prompt = ''  # 村民规则提示信息
        self.werewolf_faction_rule_prompt = ''  # 狼人规则提示信息

    def use_ability(self):
        # 使用角色特殊能力
        pass
