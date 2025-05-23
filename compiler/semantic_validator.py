from compiler.ast_parser import PylutusNode

class SemanticValidator:
    def __init__(self):
        self.errors = []

    def validate(self, ast):
        self._validate_node(ast)
        return len(self.errors) == 0

    def _validate_node(self, node):
        if node.node_type == "Module":
            for child in node.children:
                self._validate_node(child)

        elif node.node_type == "FunctionDef":
            for child in node.children:
                self._validate_node(child)

        elif node.node_type == "If":
            test = node.children[0]
            if test.node_type == "Bool" and test.value is True:
                self.errors.append(f"Unreachable else clause at line {node.line_no}")
            elif test.node_type == "Bool" and test.value is False:
                self.errors.append(f"Unreachable if clause at line {node.line_no}")
            for child in node.children[1:]:
                self._validate_node(child)

        elif node.node_type == "PylutusPay":
            if node.value["amount"] < 1000000:  # Minimum 1 ADA
                self.errors.append(f"Payment amount must be at least 1 ADA at line {node.line_no}")
