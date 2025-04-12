from src.environment.game_manager import GameManager
import os


def main():
    # 游戏初始化
    # Check if game_messages.json exists and delete it
    if os.path.exists("game_messages.json"):
        os.remove("game_messages.json")
        print("Deleted existing game_messages.json file.")

    game_manager = GameManager()
    game_manager.run_phase()  # 运行游戏阶段


if __name__ == "__main__":
    main()