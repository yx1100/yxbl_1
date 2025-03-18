from .role import Role


class Seer(Role):
    def __init__(self, name="seer", faction="VILLAGERS"):
        super().__init__(name, faction)
        self.role_prompt = """
        你的角色是预言家。
        每到夜晚阶段，当到你（预言家）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（除了自己）进行身份查验。
        如果你选择的查验目标是狼人，即非村民阵营角色，那么你将会得知这名玩家的角色属于狼人阵营。
        如果你选择的查验目标不是狼人，即非狼人阵营角色，那么你将会得知这名玩家的角色属于村民阵营。
        结束你的查验后，你（预言家）掌握了可以用来说服村民的信息，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        """

    def use_ability(self):
        # 使用技能
        doctor_ability_prompt = self.role_prompt
        return doctor_ability_prompt
