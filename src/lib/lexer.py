from typing import List, Generator, Type

from src.lib.token import Token, TokenType
from src.lib.tstream import CharStream


class Lexer:

    def __init__(self, tokens: Type[TokenType]):
        self._char_automata = tokens.automata()

    def __call__(self, stream: CharStream) -> List[Token]:
        res = []
        while not stream.eof():
            stream.skip(self.is_separator)
            if stream.eof():
                break
            gen = self.parse_tokens(stream)
            res.extend(list(gen))
        return res

    def is_separator(self, char: str) -> bool:
        return False

    def parse_tokens(self, stream: CharStream) -> Generator[Token, None, None]:
        search = self._char_automata.search(stream[:])
        if search is None:
            raise ValueError(f"Failed to tokenize starting at: {stream[:][:10]}...")

        matched, token_type = search

        stream.advance(len(matched))
        yield self.handle_token_type(stream, token_type, matched)

    def handle_token_type(self, stream: CharStream, token_type: TokenType, matched: str) -> Token:
        """
        Should create Token object for given type and matched string.
        It may consume more symbols from 'stream' to fill Token (but not before the end of 'matched').
        Or prevent handling of that token by throwing an exception.
        """
        return Token(token_type, token_type.name)
