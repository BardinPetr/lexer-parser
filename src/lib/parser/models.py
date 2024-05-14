from dataclasses import dataclass, field
from typing import List, Any, Callable, Optional

from src.lib.lexer.tokens import Token

Tokens = List[Token]


class PNodeType:
    N_DEFAULT = "node_default"
    N_ARR = "node_array"
    N_VAL = "node_value"


@dataclass
class PNode:
    type: PNodeType
    values: List[Any]

    def __str__(self):
        return f"{self.type}{self.values}"

    def __repr__(self):
        return self.__str__()

    def print(self, level=1) -> str:
        child = [
            i.print(level + 1)
            if isinstance(i, PNode)
            else f"{'  ' * level}{i}"
            for i in self.values
        ]
        child = [i for i in child]
        child = '\n'.join(child)
        res = f"{'  ' * (level - 1)}<{self.type}>:\n{child}"
        return res


@dataclass
class ParseResult:
    success: bool
    result: Optional[PNode] = None
    rest: Tokens = field(default_factory=list)

    @staticmethod
    def fail() -> 'ParseResult':
        return ParseResult(False)

    @staticmethod
    def ok(children: List[Any], rest: Tokens, node: Optional[PNodeType] = None) -> 'ParseResult':
        if node is None:
            node = PNodeType.N_DEFAULT
        node = PNode(node, children)
        return ParseResult(True, node, rest)


fail = ParseResult.fail
success = ParseResult.ok
Combinator = Callable[[Tokens], ParseResult]
