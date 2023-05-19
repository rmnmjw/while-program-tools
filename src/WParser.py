from WTokenizer import WTokenizer
from WNormalizer import WNormalizer
from WParserTypes import Statement

class WParser:
    
    normalize = True
    
    def __init__(self, options={}):
        if "normalize" in options:
            self.normalize = options.get("normalize")
        pass
    
    def parse(self, code):
        
        tokens = WTokenizer().tokenize(code)
        ast = Statement(tokens)
        if self.normalize:
            ast = WNormalizer().normalize(ast)
        
        return ast
