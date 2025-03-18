from .role import Role


class Doctor(Role):
    def __init__(self, name="doctor", faction="VILLAGERS"):
        super().__init__(name, faction)
        self.role_prompt = """
        你的角色是医生。
        每到夜晚阶段，当到你（医生）的回合时，你将被唤醒，接着你可以选择任意一名还存活的玩家（包括自己）进行救治。
        如果你选择的救治目标，同时是今夜狼人的猎杀目标，那么这名玩家将会幸存下来，即不会被狼人杀死。
        如果你选择的救治目标，不是狼人的猎杀目标，那么你的救治将会无效。
        如果你选择的救治目标，是自杀的狼人，那么你将会救活狼人。
        结束你的选择后，你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        若这一夜中有人被医生救活，还存活的玩家将在白天开始时被告知：“有人得救了。
        """

    def use_ability(self):
        # 使用技能
        doctor_ability_prompt = self.role_prompt
        return doctor_ability_prompt
