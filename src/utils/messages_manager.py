import json
import os
from  src.utils.game_enum import GameRole, GamePhase, MessageType
from typing import List, Dict, Any


class Message:
    def __init__(self,
                 number: int,
                 player_id: str,
                 role: GameRole,
                 day_count: int,
                 phase: GamePhase,
                 message_type: MessageType,
                 content: str,
                 ):
        self.number = number
        self.player_id = player_id
        self.role = role
        self.phase = phase
        self.message_type = message_type
        self.content = content
        self.day_count = day_count

    def to_dict(self) -> Dict[str, Any]:
        return {
            "number": self.number,
            "player_id": self.player_id,
            "role": self.role,
            "day_count": self.day_count,
            "phase": self.phase,
            "message_type": self.message_type,
            "content": self.content
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(
            number=data["number"],
            player_id=data["player_id"],
            role=data["role"],
            day_count=data.get("day_count", 1),
            phase=data["phase"],
            message_type=data["message_type"],
            content=data["content"]
        )


class MessagesManager:
    def __init__(self, file_path: str = None):
        self.messages: List[Message] = []
        self.next_message_number = 1
        self.file_path = file_path

        # 如果提供了文件路径，立即从文件中加载消息
        if file_path and os.path.exists(file_path):
            self.load_from_file(file_path)

    def add_message(self,
                    player_id: str,
                    role: GameRole,
                    day_count: int,
                    phase: GamePhase,
                    message_type: MessageType,
                    content: str,
                    file_path: str = None) -> Message:
        """添加一条新消息并自动保存到文件"""
        # 获取保存路径
        save_path = file_path or self.file_path

        # 如果文件存在，先检查文件中的最大消息编号
        if save_path and os.path.exists(save_path):
            self._update_next_message_number(save_path)

        message = Message(
            number=self.next_message_number,
            player_id=player_id,
            role=role,
            phase=phase,
            message_type=message_type,
            content=content,
            day_count=day_count
        )
        self.messages.append(message)
        self.next_message_number += 1

        # 保存消息到文件
        if save_path:
            self.append_message_to_file(save_path, message)

        return message

    def _update_next_message_number(self, file_path: str) -> None:
        """从文件中更新下一个消息编号"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data:
                    max_number = max(item["number"] for item in data)
                    self.next_message_number = max_number + 1
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # 如果文件不存在或为空或有错误，保持当前编号
            pass

    def get_messages(self) -> List[Message]:
        """获取所有消息"""
        return self.messages

    def append_message_to_file(self, file_path: str, message: Message) -> None:
        """将单个消息追加到现有JSON文件"""
        existing_messages = []

        # 如果文件存在，先读取现有消息
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_messages = json.load(f)
            except json.JSONDecodeError:
                # 如果文件为空或格式错误，使用空列表
                existing_messages = []

        # 添加新消息
        existing_messages.append(message.to_dict())

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_messages, f, ensure_ascii=False, indent=2)

    def load_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """从JSON文件加载消息并返回JSON格式的消息列表"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.messages = [Message.from_dict(item) for item in data]
                if self.messages:
                    self.next_message_number = max(
                        message.number for message in self.messages) + 1
                else:
                    self.next_message_number = 1
            return [message.to_dict() for message in self.messages]
        except FileNotFoundError:
            self.messages = []
            self.next_message_number = 1
            return []
