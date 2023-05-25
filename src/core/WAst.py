class WAst:
    
    def __init__(self, ast_raw=None):
        self.ast = ast_raw
    
    def __repr__(self):
        return 'WAst: ' + str(self.ast)
    
    def get_ast(self):
        return self.ast
    
    def to_code(self):
        return self.ast.to_code()