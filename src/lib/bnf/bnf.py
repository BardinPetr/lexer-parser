import re
from pprint import pprint

from src.lib.lexer.lexer import LexerRe
from src.lib.lexer.tstream import CharStream, FileCharStream
from src.lib.parser.parser import *


class BNFTokenType(TokenType):
    EQ = "::="
    OR = "|"
    EOL = "\n"
    LEXER_WORD = re.compile(r"[A-Z_\-]+")
    PARSER_WORD = re.compile(r"[a-z_\-]+")


class BNFLexer(LexerRe):
    def __init__(self, stream: CharStream):
        super().__init__(stream, BNFTokenType)

    def is_separator(self, char: str) -> bool:
        return char == " "

    def is_fallback_separator(self, char: str) -> bool:
        return char.isspace()

    def handle_token_type(self, token_type: TokenType, matched: str):
        match token_type:
            case BNFTokenType.LEXER_WORD:
                return Token(token_type, matched)
            case BNFTokenType.PARSER_WORD:
                return Token(token_type, matched)
        return Token(token_type, None)

    def __call__(self) -> List[Token]:
        last_type = None
        res = []
        # remove sequential EOFs
        for i in super().__call__():
            if i.type_id == BNFTokenType.EOL and \
                    (i.type_id == last_type or last_type is None):
                continue
            res.append(i)
            last_type = i.type_id
        return res


class BNFNodeType(NodeType):
    REF_NODE = 0
    OR_NODE = 1
    AND_NODE = 2
    DEF_NODE = 3


# class BNFParser:
#     bnfReferenceComb = nodeComb(BNFNodeType.REF_NODE, orComb(
#         tokenComb(BNFTokenType.LEXER_WORD),
#         tokenComb(BNFTokenType.PARSER_WORD)
#     ))
#     bnfAndComb = countComb(1, bnfReferenceComb)
#     bnfOrComb = countCombSep(
#         1,
#         mainComb=bnfAndComb,
#         separatorComb=tokenComb(BNFTokenType.OR),
#     )
#     bnfDef = andComb(
#         tokenComb(BNFTokenType.PARSER_WORD),
#         tokenComb(BNFTokenType.EQ),
#         bnfOrComb,
#         tokenComb(BNFTokenType.EOL)
#     )
#     bnfRoot = countComb(1, bnfDef)


#     def __init__(self):
#         # BNFParser.bnfRoot([])
#         print(inspect.getmembers(self.__class__))

# def __new__(cls, *args, **kwargs):
#     cls.root = BNFParser.bnfRoot
#     return super().__new__(cls)

# def parse(self, tokens: List[Token]):
#     return super().root(tokens)


if __name__ == "__main__":
    text = FileCharStream("/home/petr/Desktop/cpu1_forth/src/forth/grammar.bnf")
    # text = CharStream("""
    # if_expr ::= COND_IF body COND_THEN | COND_IF body COND_ELSE body COND_THEN
    # """)
    tokens = BNFLexer(text)()
    print(tokens)

    # p = BNFParser() #.parse(tokens)

    bnfReferenceComb = nodeComb(
        BNFNodeType.REF_NODE,
        orComb(
            tokenComb(BNFTokenType.LEXER_WORD),
            tokenComb(BNFTokenType.PARSER_WORD)
        )
    )

    bnfAndComb = nodeComb(
        BNFNodeType.AND_NODE,
        countComb(1, bnfReferenceComb)
    )

    bnfOrComb = nodeComb(
        BNFNodeType.OR_NODE,
        countCombSep(
            1,
            mainComb=bnfAndComb,
            separatorComb=tokenComb(BNFTokenType.OR),
        )
    )

    bnfDef = nodeComb(
        BNFNodeType.DEF_NODE,
        andComb(
            tokenComb(BNFTokenType.PARSER_WORD),
            tokenComb(BNFTokenType.EQ),
            bnfOrComb,
            tokenComb(BNFTokenType.EOL)
        )
    )

    bnfRoot = countComb(1, bnfDef)

    pprint(bnfRoot(tokens).result)
