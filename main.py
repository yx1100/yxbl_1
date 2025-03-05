from src.game_manager import GameManager
from src.utils.constants import Roles

def main():
    # 配置游戏参数
    num_players = 8
    role_config = {
        Roles.WEREWOLF: 2,
        Roles.SEER: 1,
        Roles.VILLAGER: 5
    }
    
    # 创建游戏管理器并运行游戏
    game = GameManager(num_players, role_config)
    game.run_game(max_days=15)
    
if __name__ == "__main__":
    main()