from enum import Enum
from enum import Enum
from re import Pattern
from typing import Any

from src.lib.automata import StringAutomata


class TokenType(Enum):

    @classmethod
    def values(cls):
        return {i: i.value for i in list(cls)}

    @classmethod
    def string_values(cls):
        return {k: v for k, v in cls.values().items() if isinstance(v, str)}

    @classmethod
    def pattern_values(cls):
        return {k: v for k, v in cls.values().items() if isinstance(v, Pattern)}

    @classmethod
    def automata(cls) -> StringAutomata:
        automata = StringAutomata()
        for k, v in cls.string_values().items():
            automata.push_state(v, k)
        return automata


class Token:

    def __init__(self, type_id: TokenType, value: Any):
        self.type_id = type_id
        self.value = value

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return f"T<{self.type_id}>"
