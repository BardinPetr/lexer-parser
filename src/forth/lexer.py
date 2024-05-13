from re import Pattern
from typing import Optional, Tuple, Dict

from src.forth.tokens import ForthTokenType
from src.lib.lexer.lexer import Lexer
from src.lib.lexer.tokens import TokenType, Token
from src.lib.lexer.tstream import CharStream


class ForthLexer(Lexer):
    def __init__(self, stream: CharStream):
        super().__init__(stream, ForthTokenType)
        self._fallbacks: Dict[TokenType, Pattern] = ForthTokenType.pattern_values()

    def is_separator(self, char: str) -> bool:
        return char.isspace()

    def validate_token(self, token_type: TokenType, matched: str) -> bool:
        """
        Forth tokens could only be separated by delimiter
        """
        token_after = self._stream.peek(len(matched))
        return token_after is None or self.is_separator(token_after)

    def parse_fallback(self) -> Optional[Tuple[TokenType, str]]:
        res = ""
        while not self._stream.eof() and not self.is_separator(self._stream.peek()):
            res += self._stream.next()

        for tok_type, test in self._fallbacks.items():
            if test.fullmatch(res):
                return tok_type, res

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
