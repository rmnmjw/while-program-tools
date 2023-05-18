class Simplifier:
    
    def simplify(self, el):
        className = el.__class__.__name__
        if className == "Statement":
            el.substatement.parent = el.parent
            el = el.substatement
            self.simplify(el)
            return el
        
        if className == "StatementSequential":
            for i, s in enumerate(el.substatements):
                el.substatements[i] = self.simplify(el.substatements[i])
            return el
        
        if className == "StatementIfThenElseFi":
            el.condition = self.simplify(el.condition)
            el.statementTrue = self.simplify(el.statementTrue)
            el.statementFalse = self.simplify(el.statementFalse)
            return el
        
        if className == "ExpressionBoolean":
            el.expression.parent = el.parent
            el = self.simplify(el.expression)
            return el
        
        if className == "StatementWhileDoOd":
            el.condition.parent = el.parent
            el.condition = self.simplify(el.condition.expression)
            el.body = self.simplify(el.body)
            return el
        
        if className == "ExpressionBooleanGreaterThan":
            el.left.parent = el.parent
            el.left = self.simplify(el.left.expression)
            el.right.parent = el.parent
            el.right = self.simplify(el.right.expression)
            return el
        
        if className == "StatementAssignment":
            el.assignee = self.simplify(el.assignee)
            el.assigner = self.simplify(el.assigner)
            return el
        
        if className == "ExpressionArithmetic":
            el.expression.parent = el.parent
            el = self.simplify(el.expression)
            return el
        
        if className == "ExpressionArithmeticSubstraction":
            el.minuend = self.simplify(el.minuend)
            el.subtrahend = self.simplify(el.subtrahend)
            return el
        
        if className in ["Number", "StatementSkip", "Variable"]:
            return el # nothing to simplify
        
        raise Exception(f'[Simplifier.simplify()] Unhandled class: "{className}"')

