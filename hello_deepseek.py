from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
    )


response = client.chat.completions.create(
    # deepseek-reasoner / deepseek-chat
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你是谁？"},
    ],
    stream=False
)

print(response.choices[0].message.content)


'''
场景                温度
代码生成/数学解题     0.0
数据抽取/分析        1.0
通用对话             1.3
翻译                1.3
创意类写作/诗歌创作   1.5
'''


1. 任务背景确定：社会博弈？社会竞合？
2. 强化学习的建模：代码
3. 狼人杀游戏规则的提示词