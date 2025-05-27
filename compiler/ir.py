class IRNode:
    def __init__(self, node_type, value=None, children=None, line_no=None):
        self.node_type = node_type
        self.value = value
        self.children = children or []
        self.line_no = line_no

class IRTransformer:
    def __init__(self):
        self.errors = []

    def transform(self, ast_node):
        if ast_node is None:
            self.errors.append("Invalid AST node: None")
            return None

        if ast_node.node_type == "Module":
            children = [self.transform(child) for child in ast_node.children]
            children = [c for c in children if c is not None]
            if not children:
                self.errors.append("Empty module")
                return None
            return IRNode("Module", children=children, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "FunctionDef":
            children = [self.transform(child) for child in ast_node.children]
            children = [c for c in children if c is not None]
            if not children:
                self.errors.append(f"Empty function body at line {ast_node.line_no}")
                return None
            return IRNode("FunctionDef", value=ast_node.value, children=children, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "If":
            if len(ast_node.children) < 1:
                self.errors.append(f"Invalid if statement at line {ast_node.line_no}")
                return None
            test = self.transform(ast_node.children[0])
            body = [self.transform(child) for child in ast_node.children[1:]]
            body = [c for c in body if c is not None]
            if test is None or not body:
                self.errors.append(f"Invalid if condition or body at line {ast_node.line_no}")
                return None
            return IRNode("If", children=[test] + body, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "Return":
            if len(ast_node.children) != 1:
                self.errors.append(f"Invalid return statement at line {ast_node.line_no}")
                return None
            value = self.transform(ast_node.children[0])
            if value is None:
                self.errors.append(f"Invalid return value at line {ast_node.line_no}")
                return None
            return IRNode("Return", children=[value], line_no=ast_node.line_no)
        
        elif ast_node.node_type == "Bool":
            return IRNode("Bool", value=ast_node.value, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "Num":
            return IRNode("Num", value=ast_node.value, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "PylutusSig":
            return IRNode("SigCheck", value=ast_node.value, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "PylutusPay":
            return IRNode("Pay", value=ast_node.value, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "PylutusDatum":
            return IRNode("DatumCheck", value=ast_node.value, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "PylutusRedeemer":
            return IRNode("RedeemerCheck", value=ast_node.value, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "BoolOp":
            if ast_node.value != "And":
                self.errors.append(f"Unsupported boolean operation {ast_node.value} at line {ast_node.line_no}")
                return None
            children = [self.transform(child) for child in ast_node.children]
            children = [c for c in children if c is not None]
            if len(children) < 2:
                self.errors.append(f"Invalid boolean operation at line {ast_node.line_no}")
                return None
            return IRNode("And", children=children, line_no=ast_node.line_no)
        
        elif ast_node.node_type == "Compare":
            if len(ast_node.children) != 2:
                self.errors.append(f"Invalid comparison at line {ast_node.line_no}")
                return None
            left = self.transform(ast_node.children[0])
            right = self.transform(ast_node.children[1])
            if left is None or right is None:
                self.errors.append(f"Invalid comparison operands at line {ast_node.line_no}")
                return None
            return IRNode("Compare", value=ast_node.value, children=[left, right], line_no=ast_node.line_no)
        
        elif ast_node.node_type == "Name":
            return IRNode("Name", value=ast_node.value, line_no=ast_node.line_no)
        
        else:
            self.errors.append(f"Unsupported AST node {ast_node.node_type} at line {ast_node.line_no}")
            return None
