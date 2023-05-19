JUST_CONTINUE = [
      'StatementSequential'
    , 'StatementIfThenElseFi'
    , 'StatementWhileDoOd'
    , 'StatementAssignment'
    , 'ExpressionArithmeticSubstraction'
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

class WSimplifier:
    
    def simplify(self, el):
        className = el.__class__.__name__
        
        if className in JUST_CONTINUE:
            for c in el.get_children():
                el.set_child(c.get_function(), self.simplify(c))
            return el
        
        if className in SIMPLIFY:
            if len(el.get_children()) == 1:
                child = el.get_children()[0]
                child.set_parent(el.get_parent())
                return self.simplify(child)
        
        if className in IGNORE:
            return el
            
        raise Exception(f'[Simplifier.simplify()] Unhandled class: "{className}"')

