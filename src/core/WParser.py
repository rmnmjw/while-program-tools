from WTokenizer import WTokenizer
from WNormalizer import WNormalizer
from WParserTypes import Statement
from WAst import WAst

class WParser:
    
    normalize = True
    
    def __init__(self, options={}):
        if "normalize" in options:
            self.normalize = options.get("normalize")
        pass
    
    def parse(self, code):
        
        tokens = WTokenizer().tokenize(code)
        ast_raw = Statement(tokens)
        if self.normalize:
            ast_raw = WNormalizer().normalize(ast_raw)
        
        ast = WAst(ast_raw)
        
        return ast
