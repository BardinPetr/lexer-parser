import re

from lplib.lexer.tokens import TokenType


class ForthTokenType(TokenType):
    FUNC_BEGIN = ":"
    FUNC_END = ";"

    COND_IF = "if"
    COND_ELSE = "else"
    COND_THEN = "then"

    FOR_BEGIN = "do"
    FOR_END = "loop"

    WHILE_BEGIN = "begin"
    WHILE_END = "until"
    WHILE_REPEAT = "repeat"
    WHILE_COND = "while"

    MEM_ALLOC = "allot"
    MEM_CELLS = "cells"

    DEF_CONST = "constant"
    DEF_VAR = "variable"

    IO_OUT_STR = ".\""
    CONST_STR = "s\""

    PAREN_L = "("
    PAREN_R = ")"
    DDASH = "--"

    COMMENT = "\\"

    NUMBER = re.compile(r"\d+")
    WORD = re.compile(r"[\w!#$%&*+,./<=>?@^_|~-]+")
