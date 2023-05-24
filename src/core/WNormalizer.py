JUST_CONTINUE = [
      'StatementSequential'
    , 'StatementIfThenElseFi'
    , 'StatementWhileDoOd'
    , 'StatementAssignment'
    , 'ExpressionArithmeticSubstraction'
    , 'ExpressionArithmeticAddition'
    , 'ExpressionBooleanGreaterThan'
]

IGNORE = [
      'Number'
    , 'StatementSkip'
    , 'Variable'
]

SIMPLIFY = [
      'Statement'
    , 'ExpressionArithmetic'
    , 'ExpressionBoolean'
]

class WNormalizer:
    
    def remove_shadows(self, el):
        className = el.__class__.__name__
        
        if className in JUST_CONTINUE:
            for c in el.get_children():
                el.set_child(c.get_function(), self.remove_shadows(c))
            return el
        
        if className in SIMPLIFY:
            if len(el.get_children()) == 1:
                child = el.get_children()[0]
                child.set_parent(el.get_parent())
                return self.remove_shadows(child)
        
        if className in IGNORE:
            return el
            
        raise Exception(f'[WNormalizer.simplify()] Unhandled class: "{className}"')
    
    def normalize(self, el):
        el = self.remove_shadows(el)
        return el
