from dataclasses import dataclass, field
from typing import List, Callable, Dict, Any

from src.lib.lexer.tokens import Token, TokenType

Tokens = List[Token]


@dataclass
class ParseResult:
    success: bool
    result: Tokens = field(default_factory=list)
    rest: Tokens = field(default_factory=list)
    captures: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def fail() -> 'ParseResult':
        return ParseResult(False)

    @staticmethod
    def ok(*args, **kwargs) -> 'ParseResult':
        return ParseResult(True, *args, **kwargs)


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
            out.extend(res.result)
            tokens = res.rest
        print("AND", out)
        return success(out, tokens)

    return _call


def countComb(min_count: int, comb: Combinator) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        out = []
        cnt = 0
        while (res := comb(tokens)).success:
            tokens = res.rest
            out.extend(res.result)
            cnt += 1

        if cnt >= min_count:
            return success(out, tokens)
        return fail()

    return _call


def tokenComb(type_id: TokenType) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        if tokens and tokens[0].type_id == type_id:
            return success([tokens[0]], tokens[1:])
        return fail()

    return _call


class Parser:

    def __init__(self):
        pass

    def parse(self, tokens: List[Token]):
        pass
