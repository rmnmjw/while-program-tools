from WParser import WParser

class WState:
    
    def __init__(self, **kwargs):
        self.variables = {}
        for k, v in kwargs.items():
            self.set(k, v)
    
    def set(self, k, v):
        self.variables[k] = v
    
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
        ast = None
        typeName = type(stringOrAst).__name__
        if typeName == 'str':
            ast = WParser().parse(stringOrAst)
        if typeName == 'WAst':
            ast = stringOrAst
        ast = ast.get_ast()
        if type(ast).__name__ == 'Variable':
            return self.variables.get(ast.get_value())
        raise Exception(f'Variable "{ast.get_value()}" not defined.')