from dataclasses import dataclass, field
from enum import Enum
from typing import List, Any, Callable

from src.lib.lexer.tokens import Token

Tokens = List[Token]


class PNodeType(Enum):
    pass


@dataclass
class PNode:
    type: PNodeType
    values: List[Any]

    def __str__(self):
        return f"{self.type.name}({self.values})"

    def __repr__(self):
        return self.__str__()


@dataclass
class ParseResult:
    success: bool
    result: Any = field(default_factory=list)
    rest: Tokens = field(default_factory=list)

    @staticmethod
    def fail() -> 'ParseResult':
        return ParseResult(False)

    @staticmethod
    def ok(result: List[Any], rest: Tokens) -> 'ParseResult':
        return ParseResult(True, result, rest)


fail = ParseResult.fail
success = ParseResult.ok
Combinator = Callable[[Tokens], ParseResult]
