# Tool for generating basic parser from BNF description

from lplib.bnf.bnf import compile_bnf2py

if __name__ == "__main__":
    bnf_path = "../grammar.bnf"
    python_path = "parser.gen.py"

    with open(bnf_path, "r") as f:
        code = compile_bnf2py(
            f.read(),
            token_namespace="forth.lexer.tokens.ForthTokenType",
            recursive=["func_body"]
        )

    with open(python_path, "w") as f:
        f.write(code)
