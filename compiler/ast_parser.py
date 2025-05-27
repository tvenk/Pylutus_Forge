import ast

class PylutusNode:
    def __init__(self, node_type, value=None, children=None, line_no=None):
        self.node_type = node_type
        self.value = value
        self.children = children or []
        self.line_no = line_no

class PylutusParser:
    def __init__(self):
        self.errors = []

    def parse(self, source):
        try:
            tree = ast.parse(source)
            return self._convert_ast(tree)
        except SyntaxError as e:
            self.errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
            return None

    def _convert_ast(self, node):
        if isinstance(node, ast.Module):
            return PylutusNode("Module", children=[self._convert_ast(n) for n in node.body])
        
        elif isinstance(node, ast.FunctionDef):
            if node.name != "validator":
                self.errors.append(f"Invalid function name '{node.name}' at line {node.lineno}. Expected 'validator'.")
                return None
            args = [arg.arg for arg in node.args.args]
            if len(args) == 1 and args[0] == "ctx":
                return PylutusNode("FunctionDef", value={"name": node.name, "args": ["ctx"]}, 
                                  children=[self._convert_ast(n) for n in node.body], line_no=node.lineno)
            elif len(args) == 3 and args[0] == "datum" and args[1] == "redeemer" and args[2] == "ctx":
                return PylutusNode("FunctionDef", value={"name": node.name, "args": ["datum", "redeemer", "ctx"]}, 
                                  children=[self._convert_ast(n) for n in node.body], line_no=node.lineno)
            else:
                self.errors.append(f"Invalid arguments at line {node.lineno}. Expected 'ctx' or 'datum, redeemer, ctx'.")
                return None
        
        elif isinstance(node, ast.If):
            test = self._convert_ast(node.test)
            body = [self._convert_ast(n) for n in node.body]
            orelse = [self._convert_ast(n) for n in node.orelse]
            return PylutusNode("If", children=[test] + body + orelse, line_no=node.lineno)
        
        elif isinstance(node, ast.Return):
            value = self._convert_ast(node.value)
            return PylutusNode("Return", children=[value], line_no=node.lineno)
        
        elif isinstance(node, ast.NameConstant):
            return PylutusNode("Bool", value=node.value, line_no=node.lineno)
        
        elif isinstance(node, ast.Num):
            return PylutusNode("Num", value=node.n, line_no=node.lineno)
        
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "pylutus_sig":
                if len(node.args) != 1 or not isinstance(node.args[0], ast.Str):
                    self.errors.append(f"Invalid pylutus_sig call at line {node.lineno}.")
                    return None
                return PylutusNode("PylutusSig", value=node.args[0].s, line_no=node.lineno)
            elif isinstance(node.func, ast.Name) and node.func.id == "pylutus_pay":
                if len(node.args) != 2 or not isinstance(node.args[0], ast.Str) or not isinstance(node.args[1], ast.Num):
                    self.errors.append(f"Invalid pylutus_pay call at line {node.lineno}.")
                    return None
                return PylutusNode("PylutusPay", value={"addr": node.args[0].s, "amount": node.args[1].n}, line_no=node.lineno)
            elif isinstance(node.func, ast.Name) and node.func.id == "pylutus_datum":
                if len(node.args) != 1 or not isinstance(node.args[0], ast.Str):
                    self.errors.append(f"Invalid pylutus_datum call at line {node.lineno}.")
                    return None
                return PylutusNode("PylutusDatum", value=node.args[0].s, line_no=node.lineno)
            elif isinstance(node.func, ast.Name) and node.func.id == "pylutus_redeemer":
                if len(node.args) != 1 or not isinstance(node.args[0], ast.Str):
                    self.errors.append(f"Invalid pylutus_redeemer call at line {node.lineno}.")
                    return None
                return PylutusNode("PylutusRedeemer", value=node.args[0].s, line_no=node.lineno)
        
        elif isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                op = "And"
            else:
                self.errors.append(f"Only 'and' operator supported at line {node.lineno}.")
                return None
            children = [self._convert_ast(n) for n in node.values]
            return PylutusNode("BoolOp", value=op, children=children, line_no=node.lineno)
        
        elif isinstance(node, ast.Compare):
            if len(node.ops) != 1 or len(node.comparators) != 1:
                self.errors.append(f"Complex comparisons not supported at line {node.lineno}.")
                return None
            left = self._convert_ast(node.left)
            right = self._convert_ast(node.comparators[0])
            op_type = type(node.ops[0]).__name__
            return PylutusNode("Compare", value=op_type, children=[left, right], line_no=node.lineno)
        
        elif isinstance(node, ast.Name):
            return PylutusNode("Name", value=node.id, line_no=node.lineno)
        
        elif isinstance(node, ast.Expr):
            return self._convert_ast(node.value)
        
        else:
            self.errors.append(f"Unsupported syntax at line {node.lineno}: {type(node).__name__}")
            return None
