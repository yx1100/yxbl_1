from enum import Enum
from tkinter import END

class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class GamePhase(Enum):
    INIT = "INIT"
    END = "END"
    NIGHT = "NIGHT"
    DAY = "DAY"
    VOTE = "VOTE"

class GameRole(Enum):
    HOST = "Host"
    WEREWOLF = "Werewolf"
    DOCTOR = "Doctor"
    SEER = "Seer"
    VILLAGER = "Villager"

class GameFaction(Enum):
    VILLAGERS = "VILLAGERS"
    WEREWOLVES = "WEREWOLVES"

class MessageType(Enum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"

    