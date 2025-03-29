from src.environment.game_state import GameState
from src.environment.game_manager import GameManager


def main():
    # 游戏初始化
    game_manager = GameManager()
    agents = game_manager.setup_game() 
    game_state = GameState(agents)

    alive_players_id = game_state.get_alive_players_id()
    alive_players_role = game_state.get_alive_players_role()

    phase = game_state.phase
    game_manager.run_phase()


if __name__ == "__main__":
    main()
