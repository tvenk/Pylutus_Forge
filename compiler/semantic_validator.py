class SemanticValidator:
    def __init__(self):
        self.errors = []

    def validate(self, node):
        if node is None:
            return

        if node.node_type == "Module":
            for child in node.children:
                self.validate(child)
        
        elif node.node_type == "FunctionDef":
            for child in node.children:
                self.validate(child)
        
        elif node.node_type == "If":
            test = node.children[0]
            body = node.children[1:]
            if test.node_type == "Bool" and test.value is True:
                self.errors.append(f"Unreachable else clause at line {node.line_no}")
            for child in body:
                self.validate(child)
        
        elif node.node_type == "Return":
            pass
        
        elif node.node_type == "PylutusPay":
            if node.value["amount"] < 1000000:
                self.errors.append(f"Payment amount must be at least 1 ADA at line {node.line_no}")
