import json

def process_game_data(input_file, output_file):
    """
    处理游戏日志JSON数据，提取特定信息。

    Args:
        input_file (str): 输入的JSON文件名。
        output_file (str): 输出的JSON文件名。
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误: 输入文件 '{input_file}' 未找到。")
        return
    except json.JSONDecodeError:
        print(f"错误: '{input_file}' 中的JSON数据格式无效。")
        return

    all_processed_games = []
    # 新的JSON结构是一个包含多个游戏列表的列表
    for game_log in data:
        current_game_processed = []
        for item in game_log:
            # 检查 "phase" 是否为 "END"，如果是，则保留
            if item.get("phase") == "END":
                pass  # 保留此元素，跳过下面的忽略条件
            # 否则，应用忽略规则
            else:
                # 忽略 "role" 是 "Host" 的元素
                if item.get("role") == "Host":
                    continue

                content_str = item.get("content", "")
                if isinstance(content_str, str):
                    content_str = content_str.strip()
                    # 忽略 "content" 以"现在是"或"你在第"开头的元素
                    if content_str.startswith("现在是") or content_str.startswith("你在第"):
                        continue
            
            content = item.get("content", "")
            # 清理content: 去除 '\n', '\"', ' '
            if isinstance(content, str):
                content = content.replace('\n', ' ').replace(' ', '')

            # 提取 "player_id"、"role"、"phase" 和 "content"
            processed_item = {
                "player_id": item.get("player_id"),
                "role": item.get("role"),
                "phase": item.get("phase"),
                "content": content
            }
            current_game_processed.append(processed_item)
        all_processed_games.append(current_game_processed)

    # 将处理后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_processed_games, f, ensure_ascii=False, indent=2)

    print(f"处理完成，数据已保存到 '{output_file}'")

if __name__ == "__main__":
    # 假设您的JSON数据保存在 'game_data.json' 文件中
    # 或者直接修改下面的文件名
    input_filename = "src/data/data_backup/all_games_messages_backup_20250625_225335_game100.json" 
    output_filename = "src/data/processed_data/processed_all_games_messages.json"

    process_game_data(input_filename, output_filename)
