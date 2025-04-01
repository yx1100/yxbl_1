class MessagesManager:
    def __init__(self):
        # 初始化对话管理器
        # role：system, user, assistant
        # content：对话内容
        """
        messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'},
        {'role': 'assistant', 'content': '我是一个AI助手。'}
        ]
        """
        self.history = {}  # 各玩家间的对话历史

        """
        {"Day_1": {
            "Night": [],
            "Day": [],
            "Vote": []
        },
         "Day_2": {
            "Night": [],
            "Day": [],
            "Vote": []
        },
         "Day_3": {
            "Night": [],
            "Day": [],
            "Vote": []
        },
         ...}
         """

        self.public_messages = []  # 公共消息
        self.private_messages = []  # 私人消息

        self.werewolf1_messages = []
        self.werewolf2_messages = []
        self.doctor_messages = []
        self.seer_messages = []
        self.villager1_messages = []
        self.villager2_messages = []
        
    def add_message(self, role, content):
        # 添加新消息
        if role == "werewolf1":
            self.werewolf1_messages.append(content)
        elif role == "werewolf2":
            self.werewolf2_messages.append(content)
        elif role == "doctor":
            self.doctor_messages.append(content)
        elif role == "seer":
            self.seer_messages.append(content)
        elif role == "villager1":
            self.villager1_messages.append(content)
        elif role == "villager2":
            self.villager2_messages.append(content)
        else:
            raise ValueError("Unknown role: {}".format(role))
        
    def get_conversation_by_id(self, player_id):
        # 获取与特定玩家相关的所有对话
        pass

    def get_conversation_by_role(self, role):
        # 获取与特定角色相关的所有对话
        if role == "werewolf":
            return self.werewolf_messages
        elif role == "doctor":
            return self.doctor_messages
        elif role == "seer":
            return self.seer_messages
        elif role == "villager":
            return self.villager_messages
        else:
            raise ValueError("Unknown role: {}".format(role))

