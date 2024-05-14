from forth.lexer.tokens import ForthTokenType
from lplib.parser.combinator import *
from lplib.parser.utils import CombinatorRef

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
    cmd_io = labelComb(
        orComb(
            tokenComb(ForthTokenType.IO_IN),
            tokenComb(ForthTokenType.IO_OUT_STR),
            tokenComb(ForthTokenType.IO_OUT_INT),
            tokenComb(ForthTokenType.IO_OUT_CHAR),
            tokenComb(ForthTokenType.IO_OUT_CR),
        ),
        node_name="cmd_io"
    )

    cmd_calc = labelComb(
        orComb(
            tokenComb(ForthTokenType.MATH_ADD),
            tokenComb(ForthTokenType.MATH_SUB),
            tokenComb(ForthTokenType.MATH_DIV),
            tokenComb(ForthTokenType.MATH_MUL),
            tokenComb(ForthTokenType.MATH_MOD),
            tokenComb(ForthTokenType.LOG_INV),
            tokenComb(ForthTokenType.LOG_AND),
            tokenComb(ForthTokenType.LOG_OR)
        ),
        node_name="cmd_calc"
    )

    cmd_compare = labelComb(
        orComb(
            tokenComb(ForthTokenType.CMP_EQ),
            tokenComb(ForthTokenType.CMP_LT),
            tokenComb(ForthTokenType.CMP_GT)
        ),
        node_name="cmd_compare"
    )

    cmd_mem = labelComb(
        orComb(
            tokenComb(ForthTokenType.MEM_FETCH),
            tokenComb(ForthTokenType.MEM_STORE),
            tokenComb(ForthTokenType.MEM_STORE_INC)
        ),
        node_name="cmd_mem"
    )

    cmd_call = labelComb(
        wordComb,
        node_name="cmd_call"
    )

    cmd_push = mapComb(
        lambda n_name, n_vals: ("cmd_push", [n_vals[0]]),
        numberComb,
    )

    return orComb(
        cmd_call,
        cmd_compare,
        cmd_calc,
        cmd_io,
        cmd_mem,
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
        node_name="def_arr"
    )

    # take name child node and extract
    def_var = flattenComb(
        [1],
        andComb(
            tokenComb(ForthTokenType.DEF_VAR),
            wordComb
        ),
        node_name="def_var"
    )

    # take name and value child nodes, then merge nodes
    def_const = flattenComb(
        [2, 0],
        andComb(
            numberComb,
            tokenComb(ForthTokenType.DEF_CONST),
            wordComb
        ),
        node_name="def_const"
    )

    return orComb(
        def_const,
        def_arr,
        def_var
    )


while_expr = takeComb(
    [1],
    andComb(
        tokenComb(ForthTokenType.WHILE_BEGIN),
        func_body,
        tokenComb(ForthTokenType.WHILE_END)
    ),
    node_name="while_expr"
)

for_expr = takeComb(
    [1],
    andComb(
        tokenComb(ForthTokenType.FOR_BEGIN),
        func_body,
        tokenComb(ForthTokenType.FOR_END)
    ),
    node_name="for_expr"
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
    node_name="if_expr"
)

func_body.assign(
    countComb(
        1,
        orComb(
            commandComb(),
            if_expr,
            for_expr,
            while_expr
        )
    )
)

function = mapComb(
    # extract name and code from function node
    lambda n_name, n_vals: ("function", [
        n_vals[1].values[0],  # FUNC_BEGIN -> value
        n_vals[2].values  # func_body -> list
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
    node_name="program"
)
