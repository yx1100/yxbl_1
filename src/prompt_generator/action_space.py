from enum import Enum, auto
from typing import Union, Tuple

class ActionIntent(Enum):
    """
    定义了游戏中所有可能的离散动作和意图。
    小模型将从这个指令集中选择一个输出，以指导大模型的行为。
    """
    # =================================
    # 发言类 (Speech Actions)
    # =================================

    # 宣称身份 (Claiming a role)
    CLAIM_SEER = auto()      # 我是预言家
    CLAIM_DOCTOR = auto()    # 我是医生
    CLAIM_VILLAGER = auto()  # 我是村民 (一种防御性或中立的发言)
    CLAIM_WEREWOLF = auto()  # 我是狼人 (罕见，但可能用于混淆视听)

    # 指控与辩护 (Accusation and Defense)
    ACCUSE_PLAYER = auto()   # 指控一名玩家是狼人
    DEFEND_PLAYER = auto()   # 为一名玩家辩护

    # 信息与态度 (Information and Attitude)
    QUESTION_PLAYER = auto() # 质疑一名玩家的发言或行为
    SHARE_INFO = auto()      # 分享信息 (例如，预言家分享查验结果)
    STAY_NEUTRAL = auto()    # 发表中立、划水的言论

    # =================================
    # 行动类 (Game Actions)
    # =================================

    # 白天投票 (Daytime Voting)
    VOTE_PLAYER = auto()     # 投票淘汰一名玩家

    # 夜晚技能 (Night Actions)
    NIGHT_ACTION_KILL = auto()   # 狼人：选择杀害一名玩家
    NIGHT_ACTION_HEAL = auto()   # 医生：选择治疗一名玩家
    NIGHT_ACTION_CHECK = auto()  # 预言家：选择查验一名玩家


def get_action_with_target(action: ActionIntent, target_player_id: int) -> Tuple[ActionIntent, int]:
    """
    一个辅助函数，用于将一个动作意图和其目标玩家绑定。
    例如：指控3号玩家，可以表示为 (ACCUSE_PLAYER, 3)

    Args:
        action (ActionIntent): 动作意图的枚举成员。
        target_player_id (int): 目标玩家的ID。

    Returns:
        Tuple[ActionIntent, int]: 一个包含动作和目标ID的元组。
    """
    # 检查动作是否需要目标
    if action not in [
        ActionIntent.ACCUSE_PLAYER, 
        ActionIntent.DEFEND_PLAYER,
        ActionIntent.QUESTION_PLAYER, 
        ActionIntent.VOTE_PLAYER,
        ActionIntent.NIGHT_ACTION_KILL, 
        ActionIntent.NIGHT_ACTION_HEAL,
        ActionIntent.NIGHT_ACTION_CHECK
    ]:
        raise ValueError(f"动作 {action.name} 不需要目标玩家。")

    return (action, target_player_id)

# --- 示例用法 ---
if __name__ == '__main__':
    # 示例1: 指控3号玩家
    accusation = get_action_with_target(ActionIntent.ACCUSE_PLAYER, 3)
    print(f"动作: {accusation[0].name}, 目标: {accusation[1]}")

    # 示例2: 宣称自己是预言家 (无目标)
    claim = ActionIntent.CLAIM_SEER
    print(f"动作: {claim.name}")

    # 示例3: 夜晚治疗2号玩家
    heal_action = get_action_with_target(ActionIntent.NIGHT_ACTION_HEAL, 2)
    print(f"动作: {heal_action[0].name}, 目标: {heal_action[1]}")

    # 示例4: 划水发言
    neutral_statement = ActionIntent.STAY_NEUTRAL
    print(f"动作: {neutral_statement.name}")
