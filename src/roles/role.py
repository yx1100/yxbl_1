from src.utils.config import LANGUAGE, MESSAGES_FILE_PATH
import re
import json
from src.utils.messages_manager import MessagesManager



class Role:
    def __init__(self, role_name, player_id=None, players_num=6, language=LANGUAGE):
        """
        角色基类初始化

        Args:
            role_name (str): 角色名称，如"doctor"、"werewolf"等
            player_id (str): 玩家ID
            players_num (int): 玩家数量，默认为6
            language (str): 提示语言，默认中文"cn"，可选英文"en"
            messages_manager (MessagesManager, optional): 消息管理器实例
            messages_file_path (str, optional): 消息文件路径
        """
        self.role_name = role_name
        if self.role_name in ['doctor', 'seer', 'villager']:
            self.faction = "VILLAGERS"
        elif self.role_name == "werewolf":
            self.faction = "WEREWOLVES"
        self.player_id = player_id
        self.players_num = players_num
        self.language = language
        
        # 初始化消息管理器
        self.messages_manager = MessagesManager(MESSAGES_FILE_PATH)

    def get_role_prompt(self, player_id):
        """
        获取角色规则提示
        
        Args:
            player_id (str): 玩家ID
            
        Returns:
            str: 针对特定角色的规则提示
        """
        pass  # 由子类实现
    
    def get_game_rule_prompt(self):
        """获取通用游戏规则提示"""
        pass
    
    def do_action(self, response_prompt, phase_prompt, game_state):
        """
        执行角色行动
        
        Args:
            response_prompt (str): 响应格式提示
            phase_prompt (str): 当前游戏阶段提示
            game_state: 游戏状态对象
            
        Returns:
            目标玩家ID或None
        """
        pass

    def extract_target(self, response):
        try:
            # 尝试解析JSON
            data = json.loads(response)

            # 检查target字段是否存在
            if 'target' in data:
                target = data['target']

                # 使用正则表达式提取"ID_X"部分
                match = re.search(r'(ID_\d+)', target)
                if match:
                    return match.group(1)
                return target  # 如果没有匹配到ID格式，直接返回target字段内容
            else:
                # 如果没有找到目标，尝试从action字段提取
                if 'action' in data and data['action']:
                    match = re.search(r'(ID_\d+)', data['action'])
                    if match:
                        return match.group(1)
                    
                print("没有找到目标，请检查回复格式！")
                return None
        except json.JSONDecodeError:
            # JSON解析失败，尝试直接从文本中提取
            print("response JSON解析失败，请检查格式！")
            # 尝试直接从文本中提取ID格式
            match = re.search(r'(ID_\d+)', response)
            if match:
                return match.group(1)
            return None

    def _save_message(self, role, day_count, phase, message_type="private", content=None):
        """
        发送消息
        
        Args:
            content (str): 消息内容
            day_count (int): 当前天数
            phase (Phase): 当前游戏阶段
            message_type (MessageType): 消息类型，默认为私人消息
            
        Returns:
            Message: 创建的消息对象
        """
        self.messages_manager.add_message(
            player_id=self.player_id,
            role=role,
            day_count=day_count,
            phase=phase,
            message_type=message_type,
            content=content
        )
