class Parsable:
        
    tokens = []
    parent = None
    
    name   = ""
    
    def __init__(self, tokens, parent, name):
        self.tokens = tokens
        self.set_parent(parent)
        self.set_name(name)
    
    def indent(self):
        el = self
        for i in range(1000):
            if not el.parent:
                return "\t" * (i * 2)
            el = el.parent
        return ""
    
    # def get_children(self):
        # raise Exception("get_chdilren() is not implemented yet.")
    
    def set_parent(self, parent):
        self.parent = parent
    
    def set_name(self, name):
        self.name = name
    






class TruthValue(Parsable):
    pass





class Variable(Parsable):
    
    def __init__(self, tokens, parent):
        if len(tokens) != 1:
            raise Exception(f"Variable can only have one token, but has: {len(tokens)}. Tokens: {tokens}")
        super().__init__(tokens, parent, self.__class__.__name__)
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\tVariable name: {self.tokens[0]}")
    
    # def get_children(self):
        # return []



NUMBERS = ["0","1","2","3","4","5","6","7","8","9"]
def is_number(value):
    for char in str(value):
        if char not in NUMBERS:
            return False
    return True





class Number(Parsable):
    
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\tVALUE: {self.tokens[0]}")
        
    # def get_children(self):
        # return []



class ExpressionArithmeticSubstraction(Parsable):
    
    minuend = None
    subtrahend = None

    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
        
        [minuend, subtrahend] = self.parse(tokens)
        self.minuend = minuend
        self.subtrahend = subtrahend
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\tMinuend:\n{self.minuend}"
            + f"\n{self.indent()}\tSubtrahend:\n{self.subtrahend}")
    
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == '-':
            minuend = ExpressionArithmetic(tokens[0], self)
            subtrahend = ExpressionArithmetic(tokens[2], self)
            return [minuend, subtrahend]
        
        raise Exception(f"[{self.__class__.__name__}] NOT IMPLEMENTED YET {tokens}")
    
    # def get_children(self):
        # return [self.minuend, self.subtrahend]




class ExpressionArithmetic(Parsable):
    
    expression = None
    
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
        self.expression = self.parse(tokens)
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\tExpression:"
            + f"\n{self.expression}")
    
    def parse_single_token(self, tokens):
        t = tokens[0]
        if is_number(t):
            tokens_integer = [int(t)]
            return Number(tokens_integer, self)
        else:
            tokens_variable = [t]
            return Variable(tokens_variable, self)
    
    def parse_sindle_assignment(self, tokens):
        if len(tokens) == 3 and tokens[1] == '-':
            return ExpressionArithmeticSubstraction(tokens, self)
        raise Exception(f"NOT IMPLEMENTED YET {tokens}")
    
    def parse(self, tokens):
        if len(tokens) == 1:
            return self.parse_single_token(tokens)
        else:
            count_and = 0
            count_or = 0
            for token in tokens:
                if token == "^":
                    count_and += 1
                if token == "^":
                    count_or += 1
            
            if count_and == 0 and count_or == 0:
                r = self.parse_sindle_assignment(tokens)
                return r
            
            # print("AND", count_and)
            # print("OR", count_or)
            # print("*** Multiple ***")
            # print(tokens)
            # print("------------")
    
    # def get_children(self):
        # return [("expression", self.expression)]


class ExpressionBooleanGreaterThan(Parsable):
    
    left = None
    right = None
    
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
        
        [left, right] = self.parse(tokens)
        self.left = left
        self.right = right
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\tleft hand side:"
            + f"\n{self.left}"
            + f"\n{self.indent()}\tright hand side:"
            + f"\n{self.right}")
    
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == '>':
            left = ExpressionArithmetic(tokens[0], self)
            right = ExpressionArithmetic(tokens[2], self)
            return [left, right]
        
        raise Exception(f"[{self.__class__.__name__}] Not implemented yet. Tokens: {self.tokens}")
    
    # def get_children(self):
        # return [("left", self.left), ("right", self.right)]

class ExpressionBoolean(Parsable):
    
    expression = None
    
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
        self.expression = self.parse(tokens)
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\texpression:"
            + f"\n{self.expression}")
    
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == ">":
            return ExpressionBooleanGreaterThan(tokens, self)
        
        raise Exception("Not implemented yet")
    
    # def get_children(self):
        # return [("expression", self.expression)]







class Statement(Parsable):
    
    substatement = None
    
    def __init__(self, tokens, parent=None):
        super().__init__(tokens, parent, self.__class__.__name__)
        self.substatement = self.parse(tokens)
    
    def parse(self, tokens):
        # sequential
        depth = 0
        is_sequential = False
        for token in tokens:
            if token in ['if', 'while']:
                depth += 1
            if token in ['od', 'fi']:
                depth -= 1
            if depth == 0 and token == ';':
                is_sequential = True
        
        if is_sequential:
            return StatementSequential(tokens, self)
        
        if tokens[0] == "if":
            return StatementIfThenElseFi(tokens, self)
        
        if tokens[0] == "while":
            return StatementWhileDoOd(tokens, self)
        
        if tokens[1] == ":=":
            return StatementAssignment(tokens, self)
        
        if tokens[0] == "skip":
            return StatementSkip(tokens, self)
        
        return " - *** NOT IMPLEMENTED *** - [ " + " ".join(tokens) + " ]"
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\tsubstatement:\n" + str(self.substatement))
    
    # def get_children(self):
        # return [("substatement",  self.substatement)]





class StatementAssignment(Parsable):
    
    assignee = None
    assigner = None
    
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
        [assignee, assigner] = self.parse(tokens)
        self.assignee = Variable(assignee, self)
        self.assigner = ExpressionArithmetic(assigner, self)
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\tASSIGNEE:"
            + f"\n{self.assignee}"
            + f"\n{self.indent()}\tASSIGNER:"
            + f"\n{self.assigner}")
    
    def parse(self, tokens):
        if tokens[1] != ":=":
            raise Exception(f"Assignement error! Tokens: {tokens}")
        
        assignee = tokens[0:1]
        assigner = tokens[2:]
        return [assignee, assigner]
    
    # def get_children(self):
        # return [("assignee", self.assignee), ("assigner", self.assigner)]





class StatementIfThenElseFi(Parsable):
    
    condition = None
    statementTrue = None
    statementFalse = None
        
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
        
        [condition, statementTrue, statementFalse] = self.parse(tokens)
        self.condition = ExpressionBoolean(condition, self)
        self.statementTrue = Statement(statementTrue, self)
        self.statementFalse = Statement(statementFalse, self)
    
    def __repr__(self):
        return (self.indent() + f"<<{self.name}>>"
            + f"\n{self.indent()}\tIF CONDITION:"
            + f"\n{self.condition}"
            + f"\n{self.indent()}\tTHEN STATEMENT:"
            + f"\n{self.statementTrue}"
            + f"\n{self.indent()}\tELSE STATEMENT:"
            + f"\n{self.statementFalse}")
        
    
    def parse(self, tokens):
        EXTENSION = len(tokens)
        tokens = tokens + [""] * EXTENSION

        # codition part
        cond_start = 1
        cond_end   = -1
        cond_depth = 0
        for j in range(1, 1+EXTENSION):
            if tokens[j] == "if":
                cond_depth += 1
                continue
            if cond_depth > 0 and tokens[j] == "then":
                cond_depth -= 1
                continue
            if tokens[j] == "then":
                cond_end = j
                break
        part_condition = tokens[cond_start:cond_end]
        
        # then part
        cond_end += 1
        
        then_start = cond_end
        then_end   = -1
        then_depth = 0
        for j in range(cond_end, cond_end+EXTENSION):
            if tokens[j] == "if":
                then_depth += 1
                continue
            if then_depth > 0 and tokens[j] == "fi":
                then_depth -= 1
                continue
            if tokens[j] == "else":
                then_end = j
                break
        part_then = tokens[then_start:then_end]
        
        # else part
        then_end += 1
        
        else_start = then_end
        else_end   = -1
        else_depth = 0
        for j in range(then_end, then_end+EXTENSION):
            if tokens[j] == "if":
                else_depth += 1
                continue
            if else_depth > 0 and tokens[j] == "fi":
                else_depth -= 1
                continue
            if tokens[j] == "fi":
                else_end = j
                break
        part_else = tokens[else_start:else_end]
        
        return [part_condition, part_then, part_else]
    
    # def get_children(self):
        # return [("condition", self.condition), ("statementTrue", self.statementTrue), ("statementFalse", self.statementFalse)]




class StatementSequential(Parsable):
    
    substatements = None
    
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
        self.tokens = tokens
        self.substatements = self.parse(tokens)
    
    def __repr__(self):
        result = (self.indent() + f"<<{self.name}>>"
            + "\n" + self.indent() + f"\tsubstatements ({len(self.substatements)}):")
        for s in self.substatements:
            result += "\n" + str(s)
        # todo: debug: remove this case later, when it's not needed anymore
        # if len(self.substatements) == 0:
        #     result += "\n\t\t" + self.indent() + "<none>"
        return result
    
    def parse(self, tokens):
        depth = 0
        parts = []
        current = []
        for token in tokens:
            if token in ['if', 'while']:
                depth += 1
            if token in ['od', 'fi']:
                depth -= 1
            if depth == 0 and token == ';':
                parts.append(current)
                current = []
                continue
            current.append(token)
        if len(current) != 0:
            parts.append(current)
        
        parts = [Statement(p, self) for p in parts]
        return parts
    
    # def get_children(self):
        # return [(i, el) for i, el in enumerate(self.substatements)]





class StatementWhileDoOd(Parsable):
    
    condition = None
    body = None
    
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
        
        [condition, body] = self.parse(tokens)
        self.condition = ExpressionBoolean(condition, self)
        self.body = Statement(body, self)
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>"
            + f"\n{self.indent()}\tCondition:"
            + f"\n{self.condition}"
            + f"\n{self.indent()}\tBody:"
            + f"\n{self.body}"
            )
    
    def parse(self, tokens):
        # codition part
        cond_start = 1
        cond_end   = -1
        for j in range(1, len(tokens)):
            if tokens[j] == "do":
                cond_end = j
                break
        part_condition = tokens[cond_start:cond_end]
        
        
        # body
        body_start = cond_end + 1
        body_end   = -1
        body_depth = 0
        for j in range(cond_end + 1, len(tokens)):
            if tokens[j] in ['if', 'while']:
                body_depth += 1
            if tokens[j] in ['fi', 'od']:
                body_depth -= 1
            if body_depth == 0 and tokens[j] == "od":
                body_end = j
                break
        part_body = tokens[body_start:body_end]
        
        return [part_condition, part_body]
    
    # def get_children(self):
        # return [("condition", self.condition), ("body", self.body)]






class StatementSkip(Parsable):
    
    def __init__(self, tokens, parent):
        super().__init__(tokens, parent, self.__class__.__name__)
    
    def __repr__(self):
        return (f"{self.indent()}<<{self.name}>>")
    
    # def get_children(self):
        # return []
