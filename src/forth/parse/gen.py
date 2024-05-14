# Tool for generating basic parser from BNF description

from pprint import pprint

from src.lib.bnf.bnf import BNFLexer, BNFParser, BNF2PythonTransformer
from src.lib.lexer.tstream import FileCharStream

if __name__ == "__main__":
    bnf_path = "../grammar.bnf"
    python_path = "parser.gen.py"
    token_namespace = "src.forth.lexer.tokens.ForthTokenType"
    combinators_as_refs = ["func_body"]

    text = FileCharStream(bnf_path)
    tokens = BNFLexer()(text)
    tree = BNFParser()(tokens).result
    code = BNF2PythonTransformer(token_namespace, combinators_as_refs)(tree)

    pprint(tree)

    with open(python_path, "w") as f:
        f.write(code)
