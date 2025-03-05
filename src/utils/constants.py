from enum import Enum, auto

class Roles(Enum):
    VILLAGER = auto()
    WEREWOLF = auto()
    SEER = auto()
    DOCTOR = auto()  # 添加医生角色
    WITCH = auto()
    HUNTER = auto()

class GamePhase(Enum):
    NIGHT_WEREWOLF = auto()  # 狼人行动
    NIGHT_SEER = auto()      # 预言家行动
    NIGHT_DOCTOR = auto()    # 医生行动
    NIGHT_WITCH = auto()     # 女巫行动
    DAY_ANNOUNCE = auto()    # 公布夜间信息
    DAY_DISCUSSION = auto()  # 白天讨论
    DAY_VOTE = auto()        # 白天投票