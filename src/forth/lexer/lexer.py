from forth.lexer.tokens import ForthTokenType
from lplib.lexer.lexer import LexerRe
from lplib.lexer.tokens import TokenType, Token


class ForthLexer(LexerRe):
    def __init__(self):
        super().__init__(ForthTokenType)

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
                return self.__match_string(token_type)
            case ForthTokenType.CONST_STR:
                return self.__match_string(token_type)
            case ForthTokenType.PAREN_L:
                return self.__discard_parenthesis()
            case ForthTokenType.COMMENT:
                return self.__discard_comment()

        return super().handle_token_type(token_type, matched)

    def __match_string(self, token_type: TokenType):
        self.skip()
        text = ""
        while not self._stream.eof():
            if (char := self._stream.next()) != '"':
                text += char
            else:
                break
        else:
            self.error("Not matched string")

        return Token(token_type, text)

    def __discard_parenthesis(self):
        self._stream.skip(lambda char: char != ")")
        self._stream.next()
        if self._stream.eof():
            self.error("Not matched parenthesis comment")
        return None

    def __discard_comment(self):
        self._stream.skip(lambda char: char != "\n")
        self._stream.next()
        return None
