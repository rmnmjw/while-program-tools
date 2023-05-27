from copy import deepcopy

from WParser import WParser
from WParserBaseType import WParserBaseType

class WState:
    
    def __init__(self, **kwargs):
        self.variables = {}
        for k, v in kwargs.items():
            self.set(k, v)
        
        self.name = 'σ'
        self.counter = 0
    
    def __eq__(self, other):
        for k in set(self.variables.keys()).union(set(other.variables.keys())):
            if k not in self.variables or k not in other.variables:
                return False
            if self.get(k) != other.get(k):
                return False
        return self.counter == other.counter

    def __hash__(self):
        h = self.counter.__hash__()
        for v in self.variables:
            h += v.__hash__()
        return h
    
    def __lt__(self, other):
        return self.counter < other.counter
    
    def get_name(self):
        if self.counter != 0:
            return f'{self.name}_{self.counter}'
        return self.name
    
    def increment_counter(self):
        self.counter += 1
    
    def clone(self):
        return deepcopy(self)
    
    def set(self, key, value):
        self.variables[key] = value
    
    def get(self, key):
        return self.variables.get(key)
    
    def __repr__(self):
        return str(self.variables)
    
    def beautiful(self):
        result = ''
        longest_k = -1
        longest_v = -1
        for k, v in self.variables.items():
            longest_k = max(longest_k, len(str(k)))
            longest_v = max(longest_v, len(str(v)))
        for k, v in self.variables.items():
            result += '    ' + k.rjust(longest_k) + ' |-> ' + str(v).rjust(longest_v) + '\n'
        return result
    
    def __call__(self, stringOrAst):
        return self.eval(stringOrAst)
    
    def get_ast_from(self, stringOrAst):
        ast = None
        if WParserBaseType in type(stringOrAst).__bases__:
            ast = stringOrAst
        if type(stringOrAst) == str:
            ast = WParser().parse(stringOrAst)
        return ast
    
    def eval(self, stringOrAst):
        ast = self.get_ast_from(stringOrAst)
        if ast != None:
            return self.eval_internal(ast), self
        raise Exception(f'WState.eval: Type "{type(stringOrAst)}" is not supported to be evaluated.')
    
    def eval_internal(self, ast):
        type_name = type(ast).__name__
        method = getattr(self, f'eval_internal_{type_name}')
        return method(ast)
    
    def eval_internal_Statement(self, ast):
        return self.eval_internal(ast.get_child('substatement'))
    
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
    
    def eval_internal_ExpressionBooleanEquals(self, ast):
        left = self.eval_internal(ast.get_child('left'))
        right = self.eval_internal(ast.get_child('right'))
        return left == right    
    
    def eval_internal_StatementAssignment(self, ast):
        assignee = ast.get_child('assignee').get_value()
        assigner = self.eval_internal(ast.get_child('assigner'))
        self.set(assignee, assigner)
