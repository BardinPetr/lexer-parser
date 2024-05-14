from typing import Optional

from src.lib.lexer.tokens import TokenType
from src.lib.parser.models import *


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
            return success([tokens[0]], tokens[1:])
        return fail()

    return _call


def nodeComb(node_type: PNodeType, comb: Combinator) -> Combinator:
    def _call(tokens: Tokens) -> ParseResult:
        if (res := comb(tokens)).success:
            return success(PNode(node_type, res.result), res.rest)
        return fail()

    return _call


class CombinatorRef:
    """
    Store reference to parser-combinator for using in recursive structures,
    so we could refer to our combinator before actually defining it
    """

    def __init__(self):
        self.__parser: Optional[Combinator] = None

    def assign(self, parser: Combinator):
        if self.__parser:
            raise RuntimeError("Already assigned parser")
        self.__parser = parser

    def __call__(self, *tokens: Tokens) -> ParseResult:
        if not self.__parser:
            raise RuntimeError("Not assigned parser")
        return self.__parser(*tokens)
