from src.environment.game_manager import GameManager
import os
import json


def main():
    # 存储所有游戏的消息记录
    all_games_messages = []
    
    # 循环运行100次游戏
    for game_index in range(100):
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
    
    # 将所有游戏的消息记录保存到新的JSON文件中
    output_filename = "all_games_messages.json"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(all_games_messages, f, ensure_ascii=False, indent=2)
        print(f"\n{'='*50}")
        print(f"所有游戏完成！共进行了 {len(all_games_messages)} 场游戏")
        print(f"整合后的消息记录已保存到: {output_filename}")
        print(f"{'='*50}")
    except Exception as e:
        print(f"保存整合消息文件时出错: {e}")


if __name__ == "__main__":
    main()