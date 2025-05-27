class TypeChecker:
    def __init__(self):
        self.errors = []
        self.symbol_table = {"datum": "Datum", "redeemer": "Redeemer", "ctx": "ScriptContext"}

    def check(self, node):
        if node is None:
            return

        if node.node_type == "Module":
            for child in node.children:
                self.check(child)
        
        elif node.node_type == "FunctionDef":
            if node.value["name"] != "validator":
                self.errors.append(f"Invalid function name at line {node.line_no}")
                return
            expected_return = "bool"
            for child in node.children:
                self.check(child)
            if node.children and node.children[-1].node_type == "Return":
                return_type = self.infer_type(node.children[-1].children[0])
                if return_type != expected_return:
                    self.errors.append(f"Return value must be {expected_return} at line {node.line_no}")
        
        elif node.node_type == "If":
            test = node.children[0]
            test_type = self.infer_type(test)
            if test_type != "bool":
                self.errors.append(f"Condition must be bool, got {test_type} at line {node.line_no}")
            for child in node.children[1:]:
                self.check(child)
        
        elif node.node_type == "Return":
            if len(node.children) != 1:
                self.errors.append(f"Invalid return statement at line {node.line_no}")
                return
            self.check(node.children[0])
        
        elif node.node_type == "PylutusPay":
            if not isinstance(node.value["amount"], (int, float)) or node.value["amount"] <= 0:
                self.errors.append(f"Payment amount must be positive at line {node.line_no}")
        
        elif node.node_type == "BoolOp":
            for child in node.children:
                child_type = self.infer_type(child)
                if child_type != "bool":
                    self.errors.append(f"Boolean operation requires bool operands at line {node.line_no}")
        
        elif node.node_type == "Compare":
            left_type = self.infer_type(node.children[0])
            right_type = self.infer_type(node.children[1])
            if left_type != right_type:
                self.errors.append(f"Type mismatch in comparison at line {node.line_no}")

    def infer_type(self, node):
        if node.node_type == "Bool":
            return "bool"
        elif node.node_type == "Num":
            return "number"
        elif node.node_type == "PylutusSig":
            return "bool"
        elif node.node_type == "PylutusPay":
            return "void"
        elif node.node_type == "PylutusDatum":
            return "bool"
        elif node.node_type == "PylutusRedeemer":
            return "bool"
        elif node.node_type == "BoolOp":
            return "bool"
        elif node.node_type == "Compare":
            return "bool"
        elif node.node_type == "Name":
            return self.symbol_table.get(node.value, "unknown")
        return "unknown"
