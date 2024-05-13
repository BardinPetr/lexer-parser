from src.forth.tokens import ForthTokenType
from src.lib.lexer.lexer import LexerRe
from src.lib.lexer.tokens import TokenType, Token
from src.lib.lexer.tstream import CharStream


class ForthLexer(LexerRe):
    def __init__(self, stream: CharStream):
        super().__init__(stream, ForthTokenType)

    def is_separator(self, char: str) -> bool:
        return char.isspace()

    def validate_token(self, token_type: TokenType, matched: str) -> bool:
        """
        Forth tokens could only be separated by delimiter
        """
        token_after = self._stream.peek(len(matched))
        return token_after is None or self.is_separator(token_after)

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
