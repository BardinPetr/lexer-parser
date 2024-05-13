from src.forth.lexer import ForthLexer
from src.forth.parser import ForthParser
from src.lib.lexer.tstream import CharStream

if __name__ == "__main__":
    text = """
        : fizz?  3 mod 0 = dup if ." Fizz" then ;
        : buzz?  5 mod 0 = dup if ." Buzz" then ;
        : fizz-buzz?  dup fizz? swap buzz? or invert ;
        : do-fizz-buzz  25 1 do cr i fizz-buzz? if i . then loop ;
        do-fizz-buzz
    """

    stream = CharStream(text)
    lexer = ForthLexer(stream)
    tokens = lexer()

    parser = ForthParser()
    ast = parser.parse(tokens)

    print(tokens)