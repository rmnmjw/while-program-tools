from WTokenizer import WTokenizer
from WSimplifier import WSimplifier
from WParserTypes import Statement

class WParser:
    
    simplify = True
    
    def __init__(self, options={}):
        if "simplify" in options:
            self.simplify = options.get("simplify")
        pass
    
    def parse(self, code):
        
        tokens = WTokenizer().tokenize(code)
        ast = Statement(tokens)
        if self.simplify:
            ast = WSimplifier().simplify(ast)
        
        return ast
