import numpy as np
from typing import Dict, List, Any

# 游戏设定常量
PLAYER_NUM = 6
ROLES = ["WEREWOLF", "SEER", "DOCTOR", "VILLAGER"]
PHASES = ["NIGHT", "DAY", "VOTE"]

# 向量维度定义
# 静态信息
DIM_PLAYER_ID = PLAYER_NUM  # 玩家ID的one-hot编码
DIM_ROLE = len(ROLES)       # 角色one-hot编码
DIM_ROUND = 1               # 当前轮次
DIM_PHASE = len(PHASES)     # 游戏阶段one-hot编码
DIM_ALIVE = PLAYER_NUM      # 存活玩家列表

# 每轮历史信息
DIM_SECRET_ACTION = PLAYER_NUM  # 夜晚行动目标
DIM_ANNOUNCEMENT = PLAYER_NUM   # 被淘汰玩家
DIM_VOTING = PLAYER_NUM * PLAYER_NUM # 投票矩阵 (6x6)

# 单轮历史信息的总维度
DIM_PER_ROUND_HISTORY = DIM_SECRET_ACTION + DIM_ANNOUNCEMENT + DIM_VOTING

def get_observation(game_state: Dict[str, Any], player_id: int, max_rounds: int = 5) -> np.ndarray:
    """
    根据当前游戏状态，为指定玩家生成一个固定长度的向量化观测空间。

    Args:
        game_state (Dict[str, Any]): 包含完整游戏状态的字典。
            - 'player_roles': Dict[int, str]  # {1: 'WEREWOLF', 2: 'SEER', ...}
            - 'current_round': int
            - 'current_phase': str  # 'NIGHT', 'DAY', or 'VOTE'
            - 'alive_players': List[int]
            - 'history': List[Dict]  # 每轮的历史记录
                - 'night_actions': Dict[int, int] # {player_id: target_id}
                - 'eliminated_player': int or None
                - 'votes': Dict[int, int] # {voter_id: voted_id}
        player_id (int): 需要为其生成观测空间的玩家ID (1-based)。
        max_rounds (int): 观测空间包含的最大历史轮数。

    Returns:
        np.ndarray: 一个扁平化的、固定长度的NumPy数组，代表小模型的输入。
    """
    obs_parts = []

    # --- 1. 静态信息 ---
    # 玩家ID (one-hot)
    id_vec = np.zeros(DIM_PLAYER_ID)
    id_vec[player_id - 1] = 1
    obs_parts.append(id_vec)

    # 玩家角色 (one-hot)
    role_vec = np.zeros(DIM_ROLE)
    player_role = game_state['player_roles'][player_id]
    if player_role in ROLES:
        role_idx = ROLES.index(player_role)
        role_vec[role_idx] = 1
    obs_parts.append(role_vec)

    # 当前轮次和阶段
    obs_parts.append(np.array([game_state.get('current_round', 1)]))
    phase_vec = np.zeros(DIM_PHASE)
    current_phase = game_state.get('current_phase', 'DAY')
    if current_phase in PHASES:
        phase_idx = PHASES.index(current_phase)
        phase_vec[phase_idx] = 1
    obs_parts.append(phase_vec)

    # 存活玩家 (binary)
    alive_vec = np.zeros(DIM_ALIVE)
    for p_id in game_state.get('alive_players', list(range(1, PLAYER_NUM + 1))):
        alive_vec[p_id - 1] = 1
    obs_parts.append(alive_vec)

    # --- 2. 历史信息 ---
    history = game_state.get('history', [])
    for i in range(max_rounds):
        if i < len(history):
            round_history = history[i]
            # 夜晚秘密行动 (one-hot)
            secret_action_vec = np.zeros(DIM_SECRET_ACTION)
            night_actions = round_history.get('night_actions', {})
            if player_id in night_actions and night_actions[player_id] is not None:
                target_id = night_actions[player_id]
                secret_action_vec[target_id - 1] = 1
            
            # 当日出局玩家 (one-hot)
            announcement_vec = np.zeros(DIM_ANNOUNCEMENT)
            eliminated_player = round_history.get('eliminated_player')
            if eliminated_player is not None:
                announcement_vec[eliminated_player - 1] = 1

            # 当日投票结果 (flattened matrix)
            voting_matrix = np.zeros((PLAYER_NUM, PLAYER_NUM))
            votes = round_history.get('votes', {})
            for voter, voted in votes.items():
                if voter in range(1, PLAYER_NUM + 1) and voted in range(1, PLAYER_NUM + 1):
                    voting_matrix[voter - 1, voted - 1] = 1
            voting_vec = voting_matrix.flatten()

            obs_parts.extend([secret_action_vec, announcement_vec, voting_vec])
        else:
            # 如果历史记录不够长，用0填充
            obs_parts.append(np.zeros(DIM_PER_ROUND_HISTORY))

    # 将所有部分连接成一个扁平的向量
    return np.concatenate(obs_parts).astype(np.float32)

# --- 示例用法 ---
if __name__ == '__main__':
    # 构造一个示例游戏状态
    sample_game_state = {
        'player_roles': {1: 'WEREWOLF', 2: 'SEER', 3: 'DOCTOR', 4: 'VILLAGER', 5: 'VILLAGER', 6: 'WEREWOLF'},
        'current_round': 2,
        'current_phase': 'DAY',
        'alive_players': [1, 2, 3, 4, 6],
        'history': [
            { # Round 1
                'night_actions': {1: 5, 2: 4, 3: 2, 6: 5}, # 狼人杀5号, 预言家验4, 医生救2
                'eliminated_player': 5, # 5号玩家被投票出局
                'votes': {1: 5, 2: 5, 3: 1, 4: 5, 5: 1, 6: 5}
            }
        ]
    }

    player_to_observe = 2 # 为2号玩家（预言家）生成观测向量

    # 生成观测向量
    observation_vector = get_observation(sample_game_state, player_to_observe)

    # 打印信息
    print(f"为玩家 {player_to_observe} ({sample_game_state['player_roles'][player_to_observe]}) 生成的观测向量:")
    print(observation_vector)
    print(f"\n向量总维度: {observation_vector.shape[0]}")

    # 验证维度计算
    static_dims = DIM_PLAYER_ID + DIM_ROLE + DIM_ROUND + DIM_PHASE + DIM_ALIVE
    history_dims = DIM_PER_ROUND_HISTORY * 5
    expected_dim = static_dims + history_dims
    print(f"预期总维度 (5轮历史): {expected_dim}")
    assert observation_vector.shape[0] == expected_dim
