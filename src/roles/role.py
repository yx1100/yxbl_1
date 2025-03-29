import re
import json
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

    def extract_target(self, response):
        try:
            # 尝试解析JSON
            data = json.loads(response)

            # 检查action字段是否存在
            if 'target' in data:
                target = data['target']

                # 使用正则表达式提取"kill ID_X"中的ID_X部分
                match = re.search(r'(ID_\d+)', target)
                if match:
                    return match.group(1)
            else:
                # 如果没有匹配到ID，直接返回目标
                print("没有找到目标，请检查回复格式！")
        except:
            # JSON解析失败，尝试直接从文本中提取
            print("response JSON解析失败，请检查格式！")
