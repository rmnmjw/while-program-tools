from Tokenizer import Tokenizer
from Simplifier import Simplifier
from types import Statement

class Parser:
    
    simplify = True
    
    def __init__(self, options={}):
        if "simplify" in options:
            self.simplify = options.get("simplify")
        pass
    
    def parse(self, code):
        
        tokens = Tokenizer().tokenize(code)
        ast = Statement(tokens)
        if self.simplify:
            ast = Simplifier().simplify(ast)
        
        return ast
