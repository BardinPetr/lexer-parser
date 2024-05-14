from pprint import pprint

from src.forth.lexer import ForthLexer
from src.forth.parser import program as ForthParser
from src.lib.lexer.tstream import CharStream

if __name__ == "__main__":
    # text = """
    #     : fizz?  3 mod 0 = dup if ." Fizz" then ;
    #     : buzz?  5 mod 0 = dup if ." Buzz" then ;
    #     : fizz-buzz?  dup fizz? swap buzz? or invert ;
    #     : do-fizz-buzz  25 1 do cr i fizz-buzz? if i . then loop ;
    #     do-fizz-buzz
    text = """
    : test if call1 if call2 else call3 then call4 then  ;
    : test2 do if asdas then loop ; 
    """

    stream = CharStream(text)
    tokens = ForthLexer()(stream)
    ast = ForthParser(tokens)

    print(tokens)
    pprint(ast)
