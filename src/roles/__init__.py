from .role import Role
from .villager import Villager
from .werewolf import Werewolf
from .doctor import Doctor
from .seer import Seer

# 便于根据角色名称创建角色的映射
role_map = {
    "werewolf": Werewolf,
    "villager": Villager,
    "doctor": Doctor,
    "seer": Seer
}