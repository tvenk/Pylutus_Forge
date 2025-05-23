from compiler.ast_parser import PylutusParser

with open("tests/payment_contract.pylutus", "r") as f:
    source = f.read()

parser = PylutusParser()
ast = parser.parse(source)
print(ast.node_type)  # Should print: Module
print(ast.children[0].node_type)  # Should print: FunctionDef
print(ast.children[0].children[0].node_type)  # Should print: PylutusPay
print(parser.errors)  # Should print: []
