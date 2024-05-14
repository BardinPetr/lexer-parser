from typing import Optional

from src.lib.parser.models import Combinator, Tokens, ParseResult


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
