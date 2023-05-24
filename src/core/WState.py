from WParser import WParser

class WState:
    
    def __init__(self, **kwargs):
        self.variables = {}
        for k, v in kwargs.items():
            self.set(k, v)
    
    def set(self, key, value):
        self.variables[key] = value
    
    def get(self, key):
        return self.variables.get(key)
    
    def __repr__(self):
        result = 'State\n'
        longest_k = -1
        longest_v = -1
        for k, v in self.variables.items():
            longest_k = max(longest_k, len(str(k)))
            longest_v = max(longest_v, len(str(v)))
        for k, v in self.variables.items():
            result += '    ' + k.rjust(longest_k) + ' |-> ' + str(v).rjust(longest_v) + '\n'
        return result
    
    def eval(self, stringOrAst):
        type_name = type(stringOrAst).__name__
        ast = None
        if type_name == 'str':
            ast = WParser().parse(stringOrAst).get_ast()
        if type_name == 'WAst':
            ast = stringOrAst.get_ast()
        if ast != None:
            return self.eval_internal(ast)
        raise Exception(f'WState.eval: Type "{type_name}" is not supported to be evaluated.')
        
    
    def eval_internal(self, ast):
        type_name = type(ast).__name__
        method = getattr(self, f'eval_internal_{type_name}')
        return method(ast)
    
    def eval_internal_ExpressionArithmeticAddition(self, ast):
        total = 0
        for c in ast.get_children():
            total += self.eval_internal(c)
        return total
    
    def eval_internal_ExpressionArithmeticSubstraction(self, ast):
        children = ast.get_children()
        total = self.eval_internal(children[0])
        for c in children[1:]:
            total -= self.eval_internal(c)
        return total    
    
    def eval_internal_Number(self, ast):
        return int(ast.get_value())
    
    def eval_internal_Variable(self, ast):
        return self.get(ast.get_value())
    
    def eval_internal_ExpressionBooleanGreaterThan(self, ast):
        left = self.eval_internal(ast.get_child('left'))
        right = self.eval_internal(ast.get_child('right'))
        return left > right