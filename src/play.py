from src.environment.game_manager import GameManager
import os
import json
from datetime import datetime


def save_progress(all_games_messages, game_index, is_final=False):
    """保存游戏进度"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if is_final:
        output_filename = "all_games_messages.json"
    else:
        output_filename = f"all_games_messages_backup_{timestamp}_game{game_index + 1}.json"
    
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(all_games_messages, f, ensure_ascii=False, indent=2)
        
        if is_final:
            print(f"最终结果已保存到: {output_filename}")
        else:
            print(f"进度已自动保存到: {output_filename}")
        return True
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return False


def load_existing_progress():
    """加载已存在的进度文件"""
    if os.path.exists("all_games_messages.json"):
        try:
            with open("all_games_messages.json", "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                print(f"发现已存在的进度文件，已加载 {len(existing_data)} 场游戏记录")
                return existing_data, len(existing_data)
        except Exception as e:
            print(f"加载已存在进度文件失败: {e}")
    return [], 0


def main():
    # 加载已存在的进度
    all_games_messages, start_index = load_existing_progress()
    
    # 循环运行100次游戏
    for game_index in range(start_index, 100):
        print(f"\n{'='*50}")
        print(f"开始第 {game_index + 1} 场游戏")
        print(f"{'='*50}")
        
        # 删除之前的game_messages.json文件（如果存在）
        if os.path.exists("game_messages.json"):
            os.remove("game_messages.json")
        
        # 游戏初始化并运行
        game_manager = GameManager()
        game_manager.run_phase()  # 运行游戏阶段
        
        # 读取当前游戏生成的消息文件
        if os.path.exists("game_messages.json"):
            try:
                with open("game_messages.json", "r", encoding="utf-8") as f:
                    current_game_messages = json.load(f)
                    # 将当前游戏的消息列表添加到总列表中
                    all_games_messages.append(current_game_messages)
                    print(f"第 {game_index + 1} 场游戏完成，记录了 {len(current_game_messages)} 条消息")
            except json.JSONDecodeError:
                print(f"第 {game_index + 1} 场游戏的消息文件格式错误，跳过")
            except Exception as e:
                print(f"读取第 {game_index + 1} 场游戏消息时出错: {e}")
        else:
            print(f"第 {game_index + 1} 场游戏未生成消息文件")
        
        # 每10次游戏自动保存一次进度
        if (game_index + 1) % 10 == 0:
            print(f"\n{'='*30}")
            print(f"已完成 {game_index + 1} 场游戏，自动保存进度...")
            save_progress(all_games_messages, game_index, is_final=False)
            print(f"{'='*30}")
    
    # 将所有游戏的消息记录保存到最终JSON文件中
    print(f"\n{'='*50}")
    print(f"所有游戏完成！共进行了 {len(all_games_messages)} 场游戏")
    save_progress(all_games_messages, 99, is_final=True)
    print(f"整合后的消息记录已保存到最终文件")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()