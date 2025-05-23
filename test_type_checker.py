from compiler.ast_parser import PylutusParser
from compiler.type_checker import TypeChecker

with open("tests/easy_contract.pylutus", "r") as f:
    source = f.read()

parser = PylutusParser()
ast = parser.parse(source)
checker = TypeChecker()
result = checker.check(ast)
print(result)  # Should print: True
print(checker.errors)  # Should print: []
