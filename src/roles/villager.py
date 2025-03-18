from .role import Role

class Villager(Role):
    def __init__(self, name="villager", faction="VILLAGERS"):
        super().__init__(name, faction)
        self.role_prompt = """
        你的角色是村民。
        你在整个夜晚阶段都将保持睡眠状态，且不会知道任何夜晚阶段发生的事情。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        """

    def use_ability(self):
        # 使用技能
        doctor_ability_prompt = self.role_prompt
        return doctor_ability_prompt
