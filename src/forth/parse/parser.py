from forth.lexer.tokens import ForthTokenType
from lplib.parser.combinator import *
from lplib.parser.utils import CombinatorRef
from forth.parse.nodes import ForthPNodeType as T

func_body = CombinatorRef()

wordComb = mapComb(
    lambda n_name, n_vals: (n_name, [n_vals[0].value]),
    tokenComb(ForthTokenType.WORD)
)
numberComb = mapComb(
    lambda n_name, n_vals: (n_name, [int(n_vals[0].value)]),
    tokenComb(ForthTokenType.NUMBER)
)


def commandComb() -> Combinator:
    cmd_io_str = tokenComb(ForthTokenType.IO_OUT_STR,
                           node_name=T.cmd_io_str)

    cmd_str = tokenComb(ForthTokenType.CONST_STR,
                        node_name=T.cmd_str)

    cmd_call = labelComb(wordComb,
                         node_name=T.cmd_call)

    cmd_push = mapComb(
        lambda n_name, n_vals: (T.cmd_push, [n_vals[0]]),
        numberComb,
    )

    return orComb(
        cmd_call,
        cmd_io_str,
        cmd_str,
        cmd_push
    )


def definitionComb() -> Combinator:
    # take name and size child nodes, then merge nodes
    def_arr = flattenComb(
        [1, 2],
        andComb(
            tokenComb(ForthTokenType.DEF_VAR),
            wordComb,
            numberComb,
            tokenComb(ForthTokenType.MEM_CELLS),
            tokenComb(ForthTokenType.MEM_ALLOC)
        ),
        node_name=T.def_arr
    )

    # take name child node and extract
    def_var = flattenComb(
        [1],
        andComb(
            tokenComb(ForthTokenType.DEF_VAR),
            wordComb
        ),
        node_name=T.def_var
    )

    # take name and value child nodes, then merge nodes
    def_const = flattenComb(
        [2, 0],
        andComb(
            numberComb,
            tokenComb(ForthTokenType.DEF_CONST),
            wordComb
        ),
        node_name=T.def_const
    )

    return orComb(
        def_const,
        def_arr,
        def_var
    )


do_while_expr = takeComb(
    [1],
    andComb(
        tokenComb(ForthTokenType.WHILE_BEGIN),
        func_body,
        tokenComb(ForthTokenType.WHILE_END)
    ),
    node_name=T.do_while_expr
)

while_expr = takeComb(
    [1, 3],
    andComb(
        tokenComb(ForthTokenType.WHILE_BEGIN),
        func_body,
        tokenComb(ForthTokenType.WHILE_COND),
        func_body,
        tokenComb(ForthTokenType.WHILE_REPEAT)
    ),
    node_name=T.while_expr
)

for_expr = takeComb(
    [1],
    andComb(
        tokenComb(ForthTokenType.FOR_BEGIN),
        func_body,
        tokenComb(ForthTokenType.FOR_END)
    ),
    node_name=T.for_expr
)

if_expr = takeComb(
    slice(1, None, 2),
    orComb(
        andComb(
            tokenComb(ForthTokenType.COND_IF),
            func_body,
            tokenComb(ForthTokenType.COND_THEN)
        ),
        andComb(
            tokenComb(ForthTokenType.COND_IF),
            func_body,
            tokenComb(ForthTokenType.COND_ELSE),
            func_body,
            tokenComb(ForthTokenType.COND_THEN)
        )
    ),
    node_name=T.if_expr
)

func_body.assign(
    countComb(
        1,
        orComb(
            commandComb(),
            if_expr,
            for_expr,
            do_while_expr,
            while_expr
        ),
        node_name=T.func_body
    )
)

function = mapComb(
    # extract name and code from function node
    lambda n_name, n_vals: (T.function, [
        n_vals[1].values[0],  # func_name -> value
        n_vals[2]  # func_body
    ]),
    andComb(
        tokenComb(ForthTokenType.FUNC_BEGIN),
        wordComb,
        func_body,
        tokenComb(ForthTokenType.FUNC_END)
    )
)

ForthParser = labelComb(
    countComb(
        1,
        orComb(
            definitionComb(),
            commandComb(),
            function
        )
    ),
    node_name=T.program
)
