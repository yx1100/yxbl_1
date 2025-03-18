from .role import Role


class Werewolf(Role):
    def __init__(self, name="werewolf", faction="WEREWOLVES"):
        super().__init__(name, faction)
        self.role_prompt = """
        你的角色是狼人。
        每到夜晚阶段，当到你（狼人）的回合时，在场还存活着的狼人将被唤醒，接着狼人们可以达成共识选择杀害任意一名还存活的玩家（包括狼人自己）。
        如果在场仅剩下一名狼人，这名狼人是你的话，那么你（狼人）将选择杀害任意一名还存活的玩家（包括你自己）。
        当狼人阵营选定受害者后，接着你的回合就结束了，你将会再次进入睡眠状态，等待天亮。
        等待天亮后，你将会被唤醒，接着你可以参与讨论。
        夜晚阶段被杀害的玩家将会被宣布。
        """

    def use_ability(self):
        # 使用技能
        doctor_ability_prompt = self.role_prompt
        return doctor_ability_prompt