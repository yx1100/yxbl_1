import os
from openai import OpenAI


class LLMClient:
    def __init__(self, api_key=None, model="qwen-plus", system_message="You are a helpful assistant."):
        """
        初始化 LLM 客户端

        Args:
            api_key: API 密钥，默认从环境变量获取
            model: 使用的模型名称，默认是 qwen-plus
        """

        # 如果没有提供 API 密钥，尝试从环境变量获取
        if api_key is None:
            api_key = os.getenv("DASHSCOPE_API_KEY")
        else:
            print("Using custom API key")

        # 初始化客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        # 设置使用的模型
        self.model = model

        # 初始化消息列表
        self.messages = [
            {'role': 'system', 'content': system_message}
        ]

    def get_response(self, input_messages):
        """
        调用 LLM API 获取回复

        消息列表，格式为 [{"role": "...", "content": "..."}, ...]
        消息类型:
                您通过API与大模型进行交互时的输入和输出也被称为消息（Message）。每条消息都属于一个角色（Role），角色包括系统（System）、用户（User）和助手（Assistant）。
                - 系统消息（System Message，也称为System Prompt）：用于告知模型要扮演的角色或行为。例如，您可以让模型扮演一个严谨的科学家等。默认值是“You are a helpful assistant”。您也可以将此类指令放在用户消息中，但放在系统消息中会更有效。
                - 用户消息（User Message）：您输入给模型的文本。
                - 助手消息（Assistant Message）：模型的回复。您也可以预先填写助手消息，作为后续助手消息的示例。

        Args:
            system_message: 系统消息
        Returns:
            返回 AI 的回复内容
        """

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=input_messages
            )
            return {
                "success": True,
                "content": completion.choices[0].message.content,
            }
        except Exception as e:
            error_message = f"错误信息： {e}"
            error_message += "\n请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code"
            return {
                "success": False,
                "error": error_message,
            }
