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
