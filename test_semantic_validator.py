from compiler.ast_parser import PylutusParser
from compiler.semantic_validator import SemanticValidator

with open("tests/easy_contract.pylutus", "r") as f:
    source = f.read()

parser = PylutusParser()
ast = parser.parse(source)
validator = SemanticValidator()
result = validator.validate(ast)
print(result)  # Should print: True
print(validator.errors)  # Should print: []
