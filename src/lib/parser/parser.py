import inspect
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Callable, Any

from src.lib.lexer.tokens import Token, TokenType

Tokens = List[Token]


class NodeType(Enum):
    pass


@dataclass
class Node:
    type: NodeType
    value: Any

    def __str__(self):
        return f"{self.type.name}({self.value})"

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
    def ok(result: Any, rest: Tokens) -> 'ParseResult':
        return ParseResult(True, result, rest)


fail = ParseResult.fail
success = ParseResult.ok
Combinator = Callable[[Tokens], ParseResult]


def orComb(*combs: Combinator) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        for comb in combs:
            if (res := comb(tokens)).success:
                return res
        return fail()

    return _call


def andComb(*combs: Combinator) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        out = []
        for comb in combs:
            if not (res := comb(tokens)).success:
                return fail()
            out.append(res.result)
            tokens = res.rest
        return success(out, tokens)

    return _call


def countComb(min_count: int, comb: Combinator) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        out = []
        cnt = 0
        while (res := comb(tokens)).success:
            tokens = res.rest
            out.append(res.result)
            cnt += 1

        if cnt >= min_count:
            return success(out, tokens)
        return fail()

    return _call


def countCombSep(min_count: int, mainComb: Combinator, separatorComb: Combinator) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        out = []
        cnt = 0

        while (res := mainComb(tokens)).success:
            tokens = res.rest
            out.append(res.result)
            cnt += 1

            if (res := separatorComb(tokens)).success:
                tokens = res.rest
            else:
                break

        if cnt >= min_count:
            return success(out, tokens)
        return fail()

    return _call


def tokenComb(type_id: TokenType) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        if tokens and tokens[0].type_id == type_id:
            return success(tokens[0], tokens[1:])
        return fail()

    return _call


def nodeComb(node_type: NodeType, comb: Combinator) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        if (res := comb(tokens)).success:
            return success(Node(node_type, res.result), res.rest)
        return fail()

    return _call


class Parser:

    def __init__(self):
        pass

    def parse(self, tokens: List[Token]):
        pass
