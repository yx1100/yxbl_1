import os
import json
from openai import OpenAI
from tqdm import tqdm

# 确保你的API Key已在环境变量中设置
# export DASHSCOPE_API_KEY="sk-..."
try:
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    qwen_model = "qwen3-235b-a22b-instruct-2507"  # 使用的模型名称 qwen-plus
    system_content = """遍历分析以下收集的狼人杀游戏的发言数据的结构，然后对每条发言中的content内容进行分析，提取其中的{动作: 目标}对，其中动作和目标可以有多个。保证输出的内容可以被Python的json.loads解析。
发言：content中的内容。
动作：根据content中的内容，结合玩家的角色，综合分析出玩家的一个或多个意图（动作）。具体动作包括'''
- CLAIM_SEER # 我是预言家
- CLAIM_DOCTOR # 我是医生
- CLAIM_VILLAGER # 我是村民
- CLAIM_WEREWOLF # 我是狼人
- ACCUSE_PLAYER # 指控一名玩家是狼人
- DEFEND_SELF # 为自己辩护
- DEFEND_OTHER # 为其他玩家辩护
- LEAD_VOTE_AGAINST # 号召投票给一名玩家
- QUESTION_PLAYER # 质疑一名玩家的发言或行为
- SHARE_INFO # 分享信息
- FABRICATE_INFO # 伪造信息
- STAY_NEUTRAL # 发表中立、划水的言论
- VOTE_PLAYER # 投票淘汰一名玩家
- ABSTAIN_VOTE # 放弃投票
- NIGHT_ACTION_KILL # 狼人：选择杀害一名玩家
- NIGHT_ACTION_HEAL # 医生：选择治疗一名玩家
- NIGHT_ACTION_CHECK # 预言家：选择查验一名玩家'''。
目标：动作所指向的对象，通常是玩家ID。如果动作是CLAIM_SEER、CLAIM_DOCTOR、CLAIM_VILLAGER、CLAIM_WEREWOLF和DEFEND_SELF，则目标为"SELF"。如果动作是ACCUSE_PLAYER、DEFEND_OTHER、LEAD_VOTE_AGAINST、QUESTION_PLAYER、VOTE_PLAYER、NIGHT_ACTION_KILL、NIGHT_ACTION_HEAL和NIGHT_ACTION_CHECK，则目标为被指控或被投票的玩家ID。如果动作是SHARE_INFO、FABRICATE_INFO、STAY_NEUTRAL和ABSTAIN_VOTE，则目标为"NONE"。
输出格式必须是严格的JSON格式，例如：{"NIGHT_ACTION_XXX": "ID_n", ...}
"""

    # 读取JSON数据文件
    json_file_path = os.path.join(os.path.dirname(__file__), '..', 'processed_data', 'processed_all_games_messages.json')
    with open(json_file_path, 'r', encoding='utf-8') as f:
        all_games_data = json.load(f)

    processed_results = []

    # 遍历每场游戏和每条发言
    for game in tqdm(all_games_data, desc="Processing Games"):
        game_result_content = ""
        for message in game:
            if message.get("phase") == "END":
                game_result_content = message.get("content", "")
                break
        
        game_records = []
        for message in tqdm(game, desc="Processing Messages", leave=False):
            player_id = message.get("player_id")
            role = message.get("role")
            content_str = message.get("content")
            phase = message.get("phase")

            if not content_str or phase == "END":
                continue
            
            actions_dict = {}
            
            try:
                content_json = json.loads(content_str)
                user_content = ""

                if phase == "NIGHT":
                    action = content_json.get("action")
                    target = content_json.get("target")
                    if action == "kill":
                        actions_dict["NIGHT_ACTION_KILL"] = target
                    elif action == "save":
                        actions_dict["NIGHT_ACTION_HEAL"] = target
                    elif action == "see":
                        actions_dict["NIGHT_ACTION_CHECK"] = target
                elif phase == "DAY":
                    # 对于投票(vote)的action，也直接处理
                    if "action" in content_json and content_json.get("action") == "vote":
                         actions_dict["VOTE_PLAYER"] = content_json.get("target")
                    else:
                        reasoning = content_json.get("reasoning", "")
                        statement = content_json.get("statement", "")
                        user_content = f"role:{role}\nreasoning: {reasoning}\nstatement: {statement}"

                if user_content:
                    # 调用大模型API处理content
                    completion = client.chat.completions.create(
                        model= qwen_model,
                        messages=[
                            {'role': 'system', 'content': system_content},
                            {'role': 'user', 'content': user_content}
                        ],
                        temperature=0 # 为了保证输出的稳定性
                    )
                    
                    actions_str = completion.choices[0].message.content
                    
                    # 解析模型返回的JSON字符串
                    if actions_str:
                        # 模型可能返回包含在markdown代码块中的json
                        if actions_str.strip().startswith("```json"):
                            actions_str = actions_str.strip()[7:-4].strip()
                        actions_dict.update(json.loads(actions_str))
                    else:
                        actions_dict["error"] = "model returned empty content"

            except json.JSONDecodeError:
                # content不是json，直接将其作为API的输入
                try:
                    completion = client.chat.completions.create(
                        model=qwen_model,
                        messages=[
                            {'role': 'system', 'content': system_content},
                            {'role': 'user', 'content': content_str}
                        ],
                        temperature=0
                    )
                    actions_str = completion.choices[0].message.content
                    if actions_str:
                        if actions_str.strip().startswith("```json"):
                            actions_str = actions_str.strip()[7:-4].strip()
                        actions_dict = json.loads(actions_str)
                    else:
                        actions_dict = {"error": "model returned empty content"}
                except Exception as api_e:
                     actions_dict = {"error": f"API call failed on non-json content: {api_e}"}

            except Exception as e:
                actions_dict = {"error": f"An unexpected error occurred: {e}"}

            # 判断结果
            result = "LOSE" # 默认为LOSE
            if "村民胜利" in game_result_content:
                if role in ["Seer", "Doctor", "Villager"]:
                    result = "WIN"
            elif "狼人胜利" in game_result_content:
                if role == "Werewolf":
                    result = "WIN"

            # 构建输出列表
            game_records.append([player_id, role, phase, content_str, actions_dict, result])
        processed_results.extend(game_records)

    # 对最终结果进行后处理
    final_results = []
    keys_to_check_for_none = {
        "ACCUSE_PLAYER", "DEFEND_OTHER", "LEAD_VOTE_AGAINST", 
        "QUESTION_PLAYER", "VOTE_PLAYER", "NIGHT_ACTION_KILL", 
        "NIGHT_ACTION_HEAL", "NIGHT_ACTION_CHECK"
    }
    for record in processed_results:
        actions_dict = record[4]
        # 创建一个新字典以避免在迭代时修改
        cleaned_actions = {}
        for key, value in actions_dict.items():
            # 如果键在检查列表中且值为 "NONE"，则跳过
            if key in keys_to_check_for_none and value == "NONE":
                continue
            cleaned_actions[key] = value
        record[4] = cleaned_actions
        final_results.append(record)

    # 将最终结果写入文件
    output_file_path = os.path.join(os.path.dirname(__file__), '..', 'processed_data', 'intent_action_data.json')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)

    print(f"处理完成，结果已保存到 {output_file_path}")

except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")