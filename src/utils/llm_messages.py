from enum import Enum

class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class LLMMessages:
    def __init__(self):
        self.messages = []

    def add_message(self, role: MessageRole, content: str):
        """
        添加消息到消息列表

        Args:
            role: 消息角色
            content: 消息内容
        """
        self.messages.append({"role": role.value, "content": content})



