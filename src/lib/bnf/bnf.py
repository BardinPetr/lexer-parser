import re
from enum import auto

from src.lib.lexer.lexer import LexerRe
from src.lib.lexer.tstream import CharStream, FileCharStream
from src.lib.parser.parser import *
from src.lib.parser.transformer import Transformer


class BNFTokenType(TokenType):
    EQ = "::="
    OR = "|"
    EOL = "\n"
    LEXER_WORD = re.compile(r"[A-Z_\-]+")
    PARSER_WORD = re.compile(r"[a-z_\-]+")


class BNFLexer(LexerRe):
    def __init__(self):
        super().__init__(BNFTokenType)

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

    def __call__(self, stream: CharStream) -> List[Token]:
        last_type = None
        res = []
        # remove sequential EOFs
        for i in super().__call__(stream):
            if i.type_id == BNFTokenType.EOL and \
                    (i.type_id == last_type or last_type is None):
                continue
            res.append(i)
            last_type = i.type_id
        return res


class BNFNodeType(PNodeType):
    ROOT = -1
    REF_PARSER = auto()
    REF_LEXER = auto()
    OR_NODE = auto()
    AND_NODE = auto()
    DEF_NODE = auto()
    DEF_OR_NODE = auto()


def BNFParser():
    bnfParserWordComb = nodeComb(
        BNFNodeType.REF_PARSER,
        tokenComb(BNFTokenType.PARSER_WORD)
    )
    bnfLexerWordComb = nodeComb(
        BNFNodeType.REF_LEXER,
        tokenComb(BNFTokenType.LEXER_WORD)
    )

    bnfReferenceComb = orComb(
        bnfParserWordComb, bnfLexerWordComb
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
            bnfParserWordComb,
            tokenComb(BNFTokenType.EQ),
            bnfOrComb,
            tokenComb(BNFTokenType.EOL)
        )
    )

    bnfRoot = nodeComb(
        BNFNodeType.ROOT,
        countComb(1, bnfDef)
    )
    return bnfRoot


class BNF2PythonTransformer(Transformer):

    def __init__(self, namespace):
        super().__init__()
        self._ns = namespace

    def REF_PARSER(self, i: Token):
        return i.value

    def REF_LEXER(self, i: Token):
        ref = f"{self._ns}TokenType.{i.value}"
        return f"tokenComb({ref})"

    def AND_NODE(self, *andNodes):
        if len(andNodes) == 1:
            return andNodes[0]
        nodes = ',\n'.join(andNodes)
        return f"andComb(\n{nodes}\n)"

    def before_DEF_NODE(self, node: PNode) -> PNode:
        # replace root OR_NODE node with DEF_OR_NODE
        # and push name of definition to it
        # to control recursion on level of DEF_OR_NODE
        name, _, body, _ = node.values
        own_name = name.values[0].value
        body.type = BNFNodeType.DEF_OR_NODE
        body.values = (own_name, body.values)
        return PNode(node.type, [name, body])

    def OR_NODE(self, *orNodes):
        if len(orNodes) == 1:
            return orNodes[0]
        nodes = ',\n'.join(orNodes)
        return f"orComb(\n{nodes}\n)"

    def DEF_OR_NODE(self, parent, orNodes):
        # check if we have recursion in BNF form
        # (supports only form of "name = <...> | name")
        if parent not in orNodes:
            return self.OR_NODE(*orNodes)
        orNodes.remove(parent)
        return f"countComb(\n1, \n{self.OR_NODE(*orNodes)}\n)"

    def DEF_NODE(self, name, body):
        return f"{name} = {body}"

    def ROOT(self, *lines):
        text = '\n'.join(lines[::-1])
        return f"""
            from src.lib.parser.parser import *
            {text}
        """


if __name__ == "__main__":
    bnf_path = "/home/petr/Desktop/cpu1_forth/src/forth/grammar.bnf"
    python_path = "../../forth/parser.py"
    namespace = "Forth"

    text = FileCharStream(bnf_path)
    tokens = BNFLexer()(text)
    tree = BNFParser()(tokens).result
    tree = BNF2PythonTransformer(namespace)(tree)

    with open(python_path, "w") as f:
        f.write(tree)
