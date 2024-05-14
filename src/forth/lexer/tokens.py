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

    # MEM_STORE = "!"
    # MEM_STORE_INC = "+!"
    # MEM_FETCH = "@"
    # IO_IN = "key"
    # IO_OUT_INT = "."
    # IO_OUT_CHAR = "emit"
    # IO_OUT_CR = "cr"
    # MATH_ADD = "+"
    # MATH_SUB = "-"
    # MATH_DIV = "/"
    # MATH_MUL = "*"
    # MATH_MOD = "mod"
    # LOG_INV = "invert"
    # LOG_AND = "and"
    # LOG_OR = "or"
    # CMP_EQ = "="
    # CMP_LT = "<"
    # CMP_GT = ">"

    PAREN_L = "("
    PAREN_R = ")"
    DDASH = "--"

    COMMENT = "\\"

    NUMBER = re.compile(r"\d+")
    WORD = re.compile(r"[\w!#$%&*+,./<=>?@^_|~-]+")
