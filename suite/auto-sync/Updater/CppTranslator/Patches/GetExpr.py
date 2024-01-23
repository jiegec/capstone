from tree_sitter import Node

from CppTranslator.Patches.HelperMethods import get_text
from CppTranslator.Patches.Patch import Patch


class GetExpr(Patch):
    """
    Patch   MO.getExpr()
    to      MCOperand_getExpr(MO)
    """

    def __init__(self, priority: int):
        super().__init__(priority)

    def get_search_pattern(self) -> str:
        q = (
            "(call_expression "
            "   (field_expression"
            "       ((identifier) @inst_var)"
            '       ((field_identifier) @field_id_op (#eq? @field_id_op "getExpr"))'
            "   )"
            "   ((argument_list) @arg_list)"
            ") @get_expr"
        )
        return q

    def get_main_capture_name(self) -> str:
        return "get_expr"

    def get_patch(self, captures: [(Node, str)], src: bytes, **kwargs) -> bytes:
        # Get operand variable name (MO, MachineOperand)
        op_var: Node = captures[1][0]
        op = get_text(src, op_var.start_byte, op_var.end_byte)
        return b"MCOperand_getExpr(" + op + b")"