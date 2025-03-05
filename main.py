from src.game_manager import GameManager
from src.utils.constants import Roles

def main():
    # 配置游戏参数 - 7名玩家
    num_players = 7
    role_config = {
        Roles.WEREWOLF: 2,   # 2位狼人
        Roles.SEER: 1,       # 1位预言家
        Roles.DOCTOR: 1,     # 1位医生
        Roles.VILLAGER: 3    # 3位村民
    }
    
    # 创建游戏管理器并运行游戏
    game = GameManager(num_players, role_config)
    game.run_game(max_days=15)
    
if __name__ == "__main__":
    main()