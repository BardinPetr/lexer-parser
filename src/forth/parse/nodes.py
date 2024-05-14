from enum import StrEnum, auto

from lplib.parser.models import PNodeType


class ForthPNodeType(PNodeType, StrEnum):
    cmd_io = auto()
    cmd_calc = auto()
    cmd_compare = auto()
    cmd_mem = auto()
    cmd_call = auto()
    def_arr = auto()
    def_var = auto()
    def_const = auto()
    while_expr = auto()
    for_expr = auto()
    if_expr = auto()
    program = auto()
    function = auto()
    cmd_push = auto()
