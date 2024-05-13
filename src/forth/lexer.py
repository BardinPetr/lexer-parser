import string
from typing import Optional

from src.forth.tokens import ForthTokenType
from src.lib.lexer import Lexer
from src.lib.tokens import TokenType, Token
from src.lib.tstream import CharStream


class ForthLexer(Lexer):
    WORD_SYMBOLS = string.digits + string.ascii_letters + "?-_"

    def __init__(self, stream: CharStream):
        super().__init__(stream, ForthTokenType)

    def is_separator(self, char: str) -> bool:
        return char.isspace()

    def is_identifier(self, text: str) -> bool:
        return all([i in self.WORD_SYMBOLS for i in text])

    def validate_token(self, token_type: TokenType, matched: str) -> bool:
        """
        Forth tokens could only be separated by delimiter
        """
        token_after = self._stream.peek(len(matched))
        return token_after is None or self.is_separator(token_after)

    def parse_fallback(self) -> Optional[Token]:
        res = ""
        while not self._stream.eof() and not self.is_separator(self._stream.peek()):
            res += self._stream.next()

        if res.isdigit():
            return Token(ForthTokenType.NUMBER, int(res))
        if self.is_identifier(res):
            return Token(ForthTokenType.WORD, res)

        return None

    def handle_token_type(self, token_type: TokenType, matched: str):
        match token_type:
            case ForthTokenType.NUMBER:
                return Token(token_type, int(matched))
            case ForthTokenType.WORD:
                return Token(token_type, matched)
            case ForthTokenType.IO_OUT_STR:
                return self.__match_string()

        return super().handle_token_type(token_type, matched)

    def __match_string(self):
        self.skip()
        text = ""
        while not self._stream.eof():
            if (char := self._stream.next()) != '"':
                text += char
            else:
                break
        else:
            self.error("Not matched string")

        return Token(ForthTokenType.IO_OUT_STR, text)

