import os
from openai import OpenAI


def get_response(messages):
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    completion = client.chat.completions.create(model="qwen-plus",
                                                messages=messages,
                                                # stream=True # 为流式输出，即分多次输出结果
                                                )
    return completion


try:
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'}
    ]
    # completion = get_response(messages)
    # print(completion.choices[0].message.content)

    assistant_output = "我是一名AI助手，很高兴为您服务！"
    user_input = ""
    print(f"模型输出：{assistant_output}\n")
    while "结束" not in user_input:
        user_input = input("请输入：")
        print(f"用户输入：{user_input}\n")
        # 将用户问题信息添加到messages列表中
        messages.append({"role": "user", "content": user_input})
        assistant_output = get_response(messages).choices[0].message.content
        # 将大模型的回复信息添加到messages列表中
        messages.append({"role": "assistant", "content": assistant_output})
        print(f"模型输出：{assistant_output}")
        print("\n")
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
