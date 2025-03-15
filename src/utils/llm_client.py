import os
from openai import OpenAI

class LLMClient:
    def __init__(self, api_key=None, model="qwen-plus", use_qwen=True):
        """
        初始化 LLM 客户端
        
        Args:
            api_key: API 密钥，默认从环境变量获取
            model: 使用的模型名称，默认是 qwen-plus
            use_qwen: 是否使用通义千问 API，默认为 True
        """
        # 如果没有提供 API 密钥，尝试从环境变量获取
        if api_key is None:
            if use_qwen:
                api_key = os.getenv("DASHSCOPE_API_KEY")
            else:
                api_key = os.getenv("OPENAI_API_KEY")
        
        # 初始化客户端
        if use_qwen:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
        else:
            self.client = OpenAI(api_key=api_key)
            
        self.model = model
        self.use_qwen = use_qwen
    
    def get_response(self, messages):
        """
        调用 LLM API 获取回复
        
        Args:
            messages: 消息列表，格式为 [{"role": "...", "content": "..."}, ...]
            
        Returns:
            返回 AI 的回复内容
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return {
                "success": True,
                "content": completion.choices[0].message.content,
                "raw_response": completion
            }
        except Exception as e:
            error_message = f"API 调用错误: {e}"
            if self.use_qwen:
                error_message += "\n请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
            return {
                "success": False,
                "error": error_message,
                "content": None
            }
    
    def get_role_prompt(self, role_type, game_state=None):
        """
        根据角色类型生成系统提示词
        
        Args:
            role_type: 角色类型，如 "werewolf", "villager" 等
            game_state: 当前游戏状态信息
            
        Returns:
            适合该角色的系统提示词
        """
        if role_type == "werewolf":
            return "你是一名狼人，你的目标是在不被发现的情况下杀死所有好人。在白天，你需要伪装成好人，避免被投票处决。"
        elif role_type == "villager":
            return "你是一名普通村民，你的目标是找出并处决所有狼人。你没有特殊能力，只能通过观察和讨论来判断谁是狼人。"
        elif role_type == "doctor":
            return "你是医生，你可以在夜晚救治一名玩家，使其免于狼人的袭击。你的目标是帮助村民找出并处决所有狼人。"
        elif role_type == "seer":
            return "你是预言家，你可以在夜晚查验一名玩家的身份。你的目标是帮助村民找出并处决所有狼人。"
        else:
            return "你是狼人杀游戏中的一名玩家，请根据游戏规则和你的角色进行游戏。"