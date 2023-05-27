from WTokenizer import WTokenizer
from WNormalizer import WNormalizer
from WLabelizer import WLabelizer
from WParserTypes import Statement

class WParser:
    
    def __init__(self, options={}):
        self.normalize = True
        self.labelize = True
        self.add_access_from = True
        if 'normalize' in options:
            self.normalize = options.get('normalize')
        if 'labelize' in options:
            self.labelize = options.get('labelize')
    
    def parse(self, code):
        tokens = WTokenizer().tokenize(code)
        ast = Statement(tokens)
        if self.normalize:
            ast = WNormalizer().normalize(ast)
        if self.labelize:
            ast = WLabelizer().labelize(ast)
        return ast
