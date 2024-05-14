from src.forth.tokens import ForthTokenType
from src.lib.parser.combinator import *

cmd_io = orComb(
    tokenComb(ForthTokenType.IO_IN),
    tokenComb(ForthTokenType.IO_OUT_STR),
    tokenComb(ForthTokenType.IO_OUT_INT),
    tokenComb(ForthTokenType.IO_OUT_CHAR),
    tokenComb(ForthTokenType.IO_OUT_CR)
)
cmd_calc = orComb(
    tokenComb(ForthTokenType.MATH_ADD),
    tokenComb(ForthTokenType.MATH_SUB),
    tokenComb(ForthTokenType.MATH_DIV),
    tokenComb(ForthTokenType.MATH_MUL),
    tokenComb(ForthTokenType.MATH_MOD),
    tokenComb(ForthTokenType.LOG_INV),
    tokenComb(ForthTokenType.LOG_AND),
    tokenComb(ForthTokenType.LOG_OR)
)
cmd_compare = orComb(
    tokenComb(ForthTokenType.CMP_EQ),
    tokenComb(ForthTokenType.CMP_LT),
    tokenComb(ForthTokenType.CMP_GT)
)
cmd_mem = orComb(
    tokenComb(ForthTokenType.MEM_FETCH),
    tokenComb(ForthTokenType.MEM_STORE),
    tokenComb(ForthTokenType.MEM_STORE_INC)
)
cmd_call = tokenComb(ForthTokenType.WORD)
command = orComb(
    cmd_call,
    cmd_compare,
    cmd_calc,
    cmd_io,
    cmd_mem
)
def_arr = andComb(
    tokenComb(ForthTokenType.DEF_VAR),
    tokenComb(ForthTokenType.WORD),
    tokenComb(ForthTokenType.NUMBER),
    tokenComb(ForthTokenType.MEM_CELLS),
    tokenComb(ForthTokenType.MEM_ALLOC)
)
def_var = andComb(
    tokenComb(ForthTokenType.DEF_VAR),
    tokenComb(ForthTokenType.WORD)
)
def_const = andComb(
    tokenComb(ForthTokenType.NUMBER),
    tokenComb(ForthTokenType.DEF_CONST),
    tokenComb(ForthTokenType.WORD)
)
definition = orComb(
    def_const,
    def_var,
    def_arr
)
func_body = CombinatorRef()
while_expr = andComb(
    tokenComb(ForthTokenType.WHILE_BEGIN),
    func_body,
    tokenComb(ForthTokenType.WHILE_END)
)
for_expr = andComb(
    tokenComb(ForthTokenType.FOR_BEGIN),
    func_body,
    tokenComb(ForthTokenType.FOR_END)
)
if_expr = orComb(
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
)
func_body.assign(countComb(
    1,
    orComb(
        command,
        if_expr,
        for_expr,
        while_expr
    )
))
function = andComb(
    tokenComb(ForthTokenType.FUNC_BEGIN),
    tokenComb(ForthTokenType.WORD),
    func_body,
    tokenComb(ForthTokenType.FUNC_END)
)
program = countComb(
    1,
    orComb(
        definition,
        function,
        command
    )
)
