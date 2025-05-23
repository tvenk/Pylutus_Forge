class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_stack = [{}]

    def enter_scope(self):
        """Start a new scope."""
        self.scope_stack.append({})

    def exit_scope(self):
        """Exit the current scope."""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()

    def add_symbol(self, name, type_info):
        """Add a variable to the current scope."""
        self.scope_stack[-1][name] = type_info

    def get_symbol(self, name):
        """Look up a variable in the current and outer scopes."""
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        return None

    def has_symbol(self, name):
        """Check if a variable exists in any scope."""
        return self.get_symbol(name) is not None
