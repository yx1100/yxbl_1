from src.environment.game_manager import GameManager


def main():
    # 游戏初始化
    game_manager = GameManager()
    game_manager.run_phase()  # 运行游戏阶段


if __name__ == "__main__":
    main()
