from re import Pattern
from typing import List, Type, Optional, Tuple, Dict

from src.lib.lexer.tokens import Token, TokenType
from src.lib.lexer.tstream import CharStream


class Lexer:

    def __init__(self, tokens: Type[TokenType]):
        self._char_automata = tokens.automata()
        self._stream = None

    def __call__(self, stream: CharStream) -> List[Token]:
        self._stream = stream
        res = []
        while not self._stream.eof():
            self.skip()
            if self._stream.eof():
                break
            res.append(self.__parse_token())
        return res

    def is_separator(self, char: str) -> bool:
        return False

    def skip(self):
        """
        Skip symbols matching 'is_separator()'
        """
        self._stream.skip(self.is_separator)

    def error(self, err_text: str):
        """
        Raise error with specified text and append info on source text
        """
        line_text = self._stream[:][:10].replace('\n', ' ')
        raise ValueError(f"Failed to tokenize starting at: `{line_text}...`:\n\terror: ({err_text})")

    def __parse_token(self) -> Token:
        search = self._char_automata.search(self._stream[:])
        if search is not None:
            matched, token_type = search
            matched_len = len(matched)

            if self.validate_token(token_type, matched):
                self._stream.advance(matched_len)
                return self.handle_token_type(token_type, matched)

        token = self.parse_fallback()
        if token is not None:
            return self.handle_token_type(*token)

        self.error("not found")

    def parse_fallback(self) -> Optional[Tuple[TokenType, str]]:
        """
        Try to find token if trie search failed by directly checking stream
        :returns None if not found, else token type and matched string
        """
        return None

    def validate_token(self, token_type: TokenType, matched: str) -> bool:
        """
        Check if found token is valid (fully matched)
        :return:
        """
        return True

    def handle_token_type(self, token_type: TokenType, matched: str) -> Token:
        """
        Should create Token object for given type and matched string.
        It may consume more symbols from 'stream' to fill Token (but not before the end of 'matched').
        Or prevent handling of that token by throwing an exception.
        """
        return Token(token_type, None)


class LexerRe(Lexer):
    """
    Extended lexer with regex fallback support from TokenType Patterns
    """

    def __init__(self, tokens: Type[TokenType]):
        super().__init__(tokens)
        self._fallbacks: Dict[TokenType, Pattern] = tokens.pattern_values()

    def parse_fallback(self) -> Optional[Tuple[TokenType, str]]:
        res = ""
        while not self._stream.eof() and not self.is_fallback_separator(self._stream.peek()):
            res += self._stream.next()

        for tok_type, test in self._fallbacks.items():
            if test.fullmatch(res):
                return tok_type, res

        return None

    def is_fallback_separator(self, char: str) -> bool:
        return self.is_separator(char)
