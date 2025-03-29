from src.utils.rules_prompt import WerewolfRolePrompt, GameRulePrompt


class Role:
    def __init__(self, role_name, player_id, players_num=6, roles_list=['werewolf', 'werewolf', 'doctor', 'seer', 'villager', 'villager'], language="cn"):
        """
        角色基类初始化

        Args:
            name (str): 角色名称，如"doctor"、"werewolf"等
            faction (str): 阵营，如"VILLAGERS"、"WEREWOLVES"
            player_id (str): 玩家ID
            language (str): 提示语言，默认中文"cn"，可选英文"en"
        """
        self.role_name = role_name
        if self.role_name in ['doctor', 'seer', 'villager']:
            self.faction = "VILLAGERS"
        elif self.role_name == "werewolf":
            self.faction = "WEREWOLVES"
        self.player_id = player_id
        self.players_num = players_num
        self.roles_list = roles_list

        # 创建提示生成器实例
        self.rule_prompt = GameRulePrompt(
            players_num=players_num,
            roles_list=roles_list,
            language=language
        )
        self.role_prompt = WerewolfRolePrompt(
            player_id=player_id,
            language=language
        )

    def get_game_rule_prompt(self):
        return self.rule_prompt.get_game_rules_prompt()
    
    def do_action(self):
        """
        执行角色行动
        :return: None
        """
        pass
