from src.utils.config import LANGUAGE
from src.roles.role import Role


class Villager(Role):
    def __init__(self):
        super().__init__(role_name="villager", language=LANGUAGE)
