from enum import StrEnum, auto

from lplib.parser.models import PNodeType


class ForthPNodeType(PNodeType, StrEnum):
    cmd_push = auto()
    cmd_io_str = auto()
    cmd_str = auto()
    cmd_call = auto()
    def_arr = auto()
    def_var = auto()
    def_const = auto()
    while_expr = auto()
    do_while_expr = auto()
    for_expr = auto()
    if_expr = auto()
    program = auto()
    function = auto()
