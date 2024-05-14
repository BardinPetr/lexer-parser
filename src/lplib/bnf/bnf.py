import re

from lplib.lexer.lexer import LexerRe
from lplib.lexer.tstream import CharStream
from lplib.parser.combinator import *
from lplib.parser.transformer import Transformer


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


def BNFParser():
    bnfParserWordComb = tokenComb(BNFTokenType.PARSER_WORD, node_name="pword")
    bnfLexerWordComb = tokenComb(BNFTokenType.LEXER_WORD, node_name="lword")
    bnfReferenceComb = orComb(bnfParserWordComb, bnfLexerWordComb)

    bnfAndComb = countComb(
        1, bnfReferenceComb,
        node_name="group_and"
    )

    bnfOrComb = countComb(
        1, bnfAndComb,
        separatorComb=tokenComb(BNFTokenType.OR),
        node_name="group_or"
    )

    bnfDef = andComb(
        bnfParserWordComb,
        tokenComb(BNFTokenType.EQ),
        bnfOrComb,
        tokenComb(BNFTokenType.EOL),
        node_name="node_def"
    )

    bnfRoot = countComb(
        1, bnfDef,
        node_name="root"
    )
    return bnfRoot


class BNF2PythonTransformer(Transformer):

    def __init__(self, tokenTypeNS: str, combinators_as_refs: List[str]):
        super().__init__()
        self._tt_class = tokenTypeNS[tokenTypeNS.rfind('.') + 1:]
        self._tt_ns = tokenTypeNS[:tokenTypeNS.rfind('.')]
        self._use_as_ref = combinators_as_refs

    def pword(self, i: Token):
        return i.value

    def lword(self, i: Token):
        return f"tokenComb({self._tt_class}.{i.value})"

    def group_and(self, *andNodes):
        if len(andNodes) == 1:
            return andNodes[0]
        nodes = ',\n'.join(andNodes)
        return f"andComb(\n{nodes}\n)"

    def group_or(self, *orNodes):
        if len(orNodes) == 1:
            return orNodes[0]
        nodes = ',\n'.join(orNodes)
        return f"orComb(\n{nodes}\n, create_node=True\n)"

    def node_def_root_or(self, parent, orNodes):
        # check if we have recursion in BNF form
        # (supports only form of "name = <...> | name")
        if parent not in orNodes:
            return self.group_or(*orNodes)
        orNodes.remove(parent)
        return f"countComb(\n1, \n{self.group_or(*orNodes)}\n)"

    def before_node_def(self, node: PNode) -> PNode:
        # replace root OR_NODE node with DEF_OR_NODE
        # and push name of definition to it
        # to control recursion on level of DEF_OR_NODE
        name, _, body, _ = node.values
        own_name = name.values[0].value
        body.type = "node_def_root_or"
        body.values = (own_name, body.values)
        return PNode(node.type, [name, body])

    def node_def(self, name, body):
        labeled_body = f"labelComb(\n{body},\nnode_name=\"{name}\"\n)"
        return f"{name}.assign({labeled_body})" \
            if name in self._use_as_ref \
            else f"{name} = {labeled_body}"

    def root(self, *lines):
        lines = lines[::-1]

        body = '\n\n'.join(lines)
        decls = "\n".join([
            f"{i} = CombinatorRef()"
            for i in self._use_as_ref
        ])
        return f"""
            # Generated from BNF
            from lplib.parser.utils import CombinatorRef
            from lplib.parser.combinator import *
            from {self._tt_ns} import {self._tt_class}\n
            {decls}\n
            {body}
        """


def compile_bnf2py(bnf_text: str, token_namespace: str, recursive: List[str]) -> str:
    """
    Parse BNF file and build parser-combinators corresponding to that grammar.
    :param bnf_text:  BNF grammar
    :param token_namespace: full pythonic path to extended TokenType class
    :param recursive: list of grammar parser names, which are used recursively
    :return:
    """
    text = CharStream(bnf_text)
    tokens = BNFLexer()(text)
    tree = BNFParser()(tokens).result
    return BNF2PythonTransformer(token_namespace, recursive)(tree)
