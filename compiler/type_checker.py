from compiler.utils import SymbolTable
from compiler.ast_parser import PylutusNode

class TypeChecker:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def check(self, ast):
        self.symbol_table.add_symbol("ctx", "ScriptContext")
        self._check_node(ast)
        return len(self.errors) == 0

    def _check_node(self, node):
        if node.node_type == "Module":
            for child in node.children:
                self._check_node(child)

        elif node.node_type == "FunctionDef":
            self.symbol_table.enter_scope()
            for child in node.children:
                self._check_node(child)
            self.symbol_table.exit_scope()

        elif node.node_type == "If":
            for child in node.children:
                self._check_node(child)
                if child.node_type in ("PylutusSig", "Compare"):
                    if self._get_type(child) != "bool":
                        self.errors.append(f"Condition must be bool at line {child.line_no}")
                elif child.node_type == "Return":
                    if self._get_type(child.children[0]) != "bool":
                        self.errors.append(f"Return value must be bool at line {child.line_no}")

        elif node.node_type == "Return":
            if self._get_type(node.children[0]) != "bool":
                self.errors.append(f"Return value must be bool at line {node.line_no}")

        elif node.node_type == "PylutusPay":
            if not isinstance(node.value["amount"], (int, float)) or node.value["amount"] <= 0:
                self.errors.append(f"Invalid amount in pylutus_pay at line {node.line_no}")

    def _get_type(self, node):
        if node.node_type == "Bool":
            return "bool"
        elif node.node_type == "PylutusSig":
            return "bool"
        elif node.node_type == "Num":
            return "int"
        elif node.node_type == "Name":
            type_info = self.symbol_table.get_symbol(node.value)
            if type_info is None:
                self.errors.append(f"Undefined variable {node.value} at line {node.line_no}")
                return None
            return type_info
        elif node.node_type == "Compare":
            return "bool"
        return None
