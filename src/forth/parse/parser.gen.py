# Generated from BNF
from lplib.parser.utils import CombinatorRef
from forth.lexer.tokens import ForthTokenType

func_body = CombinatorRef()

cmd_io = labelComb(
    orComb(
        tokenComb(ForthTokenType.IO_IN),
        tokenComb(ForthTokenType.IO_OUT_STR),
        tokenComb(ForthTokenType.IO_OUT_INT),
        tokenComb(ForthTokenType.IO_OUT_CHAR),
        tokenComb(ForthTokenType.IO_OUT_CR)
        , create_node=True
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
        , create_node=True
    ),
    node_name="cmd_calc"
)

cmd_compare = labelComb(
    orComb(
        tokenComb(ForthTokenType.CMP_EQ),
        tokenComb(ForthTokenType.CMP_LT),
        tokenComb(ForthTokenType.CMP_GT)
        , create_node=True
    ),
    node_name="cmd_compare"
)

cmd_mem = labelComb(
    orComb(
        tokenComb(ForthTokenType.MEM_FETCH),
        tokenComb(ForthTokenType.MEM_STORE),
        tokenComb(ForthTokenType.MEM_STORE_INC)
        , create_node=True
    ),
    node_name="cmd_mem"
)

cmd_call = labelComb(
    tokenComb(ForthTokenType.WORD),
    node_name="cmd_call"
)

cmd_push = labelComb(
    tokenComb(ForthTokenType.NUMBER),
    node_name="cmd_push"
)

command = labelComb(
    orComb(
        cmd_call,
        cmd_compare,
        cmd_calc,
        cmd_io,
        cmd_mem,
        cmd_push
        , create_node=True
    ),
    node_name="command"
)

def_var = labelComb(
    andComb(
        tokenComb(ForthTokenType.DEF_VAR),
        tokenComb(ForthTokenType.WORD)
    ),
    node_name="def_var"
)

def_const = labelComb(
    andComb(
        tokenComb(ForthTokenType.NUMBER),
        tokenComb(ForthTokenType.DEF_CONST),
        tokenComb(ForthTokenType.WORD)
    ),
    node_name="def_const"
)

def_arr = labelComb(
    andComb(
        def_var,
        tokenComb(ForthTokenType.NUMBER),
        tokenComb(ForthTokenType.WORD),
        tokenComb(ForthTokenType.MEM_ALLOC)
    ),
    node_name="def_arr"
)

definition = labelComb(
    orComb(
        def_const,
        def_arr,
        def_var
        , create_node=True
    ),
    node_name="definition"
)

while_expr = labelComb(
    andComb(
        tokenComb(ForthTokenType.WHILE_BEGIN),
        func_body,
        tokenComb(ForthTokenType.WHILE_END)
    ),
    node_name="while_expr"
)

for_expr = labelComb(
    andComb(
        tokenComb(ForthTokenType.FOR_BEGIN),
        func_body,
        tokenComb(ForthTokenType.FOR_END)
    ),
    node_name="for_expr"
)

if_expr = labelComb(
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
        , create_node=True
    ),
    node_name="if_expr"
)

func_body.assign(labelComb(
    countComb(
        1,
        orComb(
            command,
            if_expr,
            for_expr,
            while_expr
            , create_node=True
        )
    ),
    node_name="func_body"
))

function = labelComb(
    andComb(
        tokenComb(ForthTokenType.FUNC_BEGIN),
        tokenComb(ForthTokenType.WORD),
        func_body,
        tokenComb(ForthTokenType.FUNC_END)
    ),
    node_name="function"
)

program = labelComb(
    countComb(
        1,
        orComb(
            definition,
            function,
            command
            , create_node=True
        )
    ),
    node_name="program"
)
