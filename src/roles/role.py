from src.utils.rules_prompt import WerewolfPrompt


class Role:
    def __init__(self, name, player_id, language="cn"):
        """
        角色基类初始化

        Args:
            name (str): 角色名称，如"doctor"、"werewolf"等
            faction (str): 阵营，如"VILLAGERS"、"WEREWOLVES"
            player_id (str): 玩家ID
            language (str): 提示语言，默认中文"cn"，可选英文"en"
        """
        self.name = name
        if self.name in ['doctor', 'seer', 'villager']:
            self.faction = "VILLAGERS"
        elif self.name == "werewolf":
            self.faction = "WEREWOLVES"
        self.player_id = player_id

        # 创建提示生成器实例
        self.prompt = WerewolfPrompt(
            roles_list=None,  # 游戏中可能出现的角色列表，在游戏开始时设置
            players_num=6,    # 默认玩家数量，在游戏开始时更新
            player_id=player_id,
            language=language
        )

    def use_ability(self):
        """使用角色特殊能力（由子类实现）"""
        pass