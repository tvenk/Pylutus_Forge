from compiler.utils import SymbolTable

symbol_table = SymbolTable()
symbol_table.add_symbol("ctx", "ScriptContext")
print(symbol_table.get_symbol("ctx"))  # Should print: ScriptContext
symbol_table.enter_scope()
symbol_table.add_symbol("x", "bool")
print(symbol_table.get_symbol("x"))    # Should print: bool
print(symbol_table.get_symbol("ctx"))  # Should print: ScriptContext
symbol_table.exit_scope()
print(symbol_table.get_symbol("x"))    # Should print: None
