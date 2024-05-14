from typing import Union

from src.lib.lexer.tokens import TokenType
from src.lib.parser.models import *


def orComb(*combs: Combinator, create_node=False) -> Combinator:
    """
    Tries passed combinators before first success.
    If node_name is specified, new node would be created with result node as single element

    :return: transparently returns result
    """

    def _call(tokens: Tokens) -> ParseResult:
        for comb in combs:
            if (res := comb(tokens)).success:
                if create_node:
                    return success([res.result], res.rest)
                return res
        return fail()

    return _call


def andComb(*combs: Combinator, node_name=None) -> Combinator:
    """
    Join all combinators in list sequentially. All should succeed. Returns results as node with list
    """

    def _call(tokens: Tokens) -> ParseResult:
        out = []
        for comb in combs:
            if not (res := comb(tokens)).success:
                return fail()
            out.append(res.result)
            tokens = res.rest
        return success(out, tokens, node_name)

    return _call


def countComb(min_count: int,
              mainComb: Combinator,
              separatorComb: Optional[Combinator] = None,
              node_name=None) -> Combinator:
    """
    Create combinator for getting other combinator repeated
    :param min_count: minimal repetitions for success
    :param mainComb: repeated combinator
    :param separatorComb: if not None, combinator to act as separator between mainCombs
    """

    def _call(tokens: Tokens) -> ParseResult:
        out = []
        cnt = 0
        while (res := mainComb(tokens)).success:
            tokens = res.rest
            out.append(res.result)
            cnt += 1

            if not separatorComb: continue
            if (res := separatorComb(tokens)).success:
                tokens = res.rest
            else:
                break

        if cnt >= min_count:
            return success(out, tokens, node_name)
        return fail()

    return _call


def tokenComb(type_id: TokenType, node_name=None) -> Combinator:
    """
    Combinator that takes single token of specified type
    """

    def _call(tokens: Tokens) -> ParseResult:
        if tokens and tokens[0].type_id == type_id:
            return success([tokens[0]], tokens[1:], node_name)
        return fail()

    return _call


def labelComb(comb: Combinator, node_name: Union[PNodeType | str]) -> Combinator:
    """
    Passes output of comb with PNode's type renamed to node_type
    """

    def _call(tokens: Tokens) -> ParseResult:
        if (res := comb(tokens)).success:
            return success(res.result.values, res.rest, node_name)
        return fail()

    return _call


def mapComb(func: Callable[[PNode], PNode], comb: Combinator) -> Combinator:
    """
    Run converter function on PNode returned by calling combinator
    """

    def _call(tokens: Tokens) -> ParseResult:
        if (res := comb(tokens)).success:
            return ParseResult(True, func(res.result), res.rest)
        return fail()

    return _call
