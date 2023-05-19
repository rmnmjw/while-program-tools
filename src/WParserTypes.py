
class Parsable:
        
    def __init__(self, tokens, name):
        self.tokens = []
        self.parent = None
        self.name   = ""
        self.function = ""
        self.children = []
        self.value = None
        
        self.tokens = tokens
        self.set_name(name)
    
    def indent(self):
        el = self
        for i in range(1000):
            if not el.parent:
                return "\t" * (i * 2)
            el = el.parent
        return ""
    
    def set_child(self, key, value):
        value.set_parent(self)
        value.set_function(key)
        
        index = -1
        for i, el in enumerate(self.children):
            if el.get_function() == key:
                index = i
                break
        if index != -1:
            self.children[index] = value
        else:
            self.children.append(value)
    
    def set_children(self, elements):
        self.children = []
        for i, el in enumerate(elements):
            el.set_function('substatement_' + str(i))
            el.set_parent(self)
            self.children.append(el)
    
    def get_children(self):
        return self.children
    
    def get_child(self, key):
        for el in self.children:
            if el.get_function() == key:
                return el
    
    def set_parent(self, parent):
        self.parent = parent
    
    def get_parent(self):
        return self.parent
    
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_function(self, function):
        self.function = function
    
    def get_function(self):
        return self.function

    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value

    def __repr__(self):
        result = ''
        result += self.indent() + f"<<{self.name}>>"
        if self.get_value() != None:
            result += "\n" + self.indent() + f"\tVALUE: {self.get_value()}"
        for i, s in enumerate(self.get_children()):
            result += "\n" + self.indent() + f"\t{s.get_function()} ({i+1}/{len(self.get_children())}):"
            if s == None:
                result += "\n#### NONE ####"
            else:
                result += "\n" + str(s)
        return result

class TruthValue(Parsable):
    pass

class Variable(Parsable):
    
    def __init__(self, tokens):
        if len(tokens) != 1:
            raise Exception(f"Variable can only have one token, but has: {len(tokens)}. Tokens: {tokens}")
        super().__init__(tokens, self.__class__.__name__)
        self.set_value(self.tokens[0])
    
class Number(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        self.set_value(self.tokens[0])
    
class ExpressionArithmeticSubstraction(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        
        [minuend, subtrahend] = self.parse(tokens)
        self.set_child('minuend', minuend)
        self.set_child('subtrahend', subtrahend)
    
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == '-':
            minuend = ExpressionArithmetic(tokens[0])
            subtrahend = ExpressionArithmetic(tokens[2])
            return [minuend, subtrahend]
        
        raise Exception(f"[{self.__class__.__name__}] NOT IMPLEMENTED YET {tokens}")

class ExpressionArithmetic(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        self.set_child('expression', self.parse(tokens))
    
    def is_number(self, value):
        for char in str(value):
            if char not in ["0","1","2","3","4","5","6","7","8","9"]:
                return False
        return True
    
    def parse_single_token(self, tokens):
        t = tokens[0]
        if self.is_number(t):
            tokens_integer = [int(t)]
            return Number(tokens_integer)
        else:
            tokens_variable = [t]
            return Variable(tokens_variable)
    
    def parse_sindle_assignment(self, tokens):
        if len(tokens) == 3 and tokens[1] == '-':
            return ExpressionArithmeticSubstraction(tokens)
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

class ExpressionBooleanGreaterThan(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        
        [left, right] = self.parse(tokens)
        self.set_child('left', left)
        self.set_child('right', right)
    
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == '>':
            left = ExpressionArithmetic(tokens[0])
            right = ExpressionArithmetic(tokens[2])
            return [left, right]
        
        raise Exception(f"[{self.__class__.__name__}] Not implemented yet. Tokens: {self.tokens}")

class ExpressionBoolean(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        self.set_child('expression', self.parse(tokens))
    
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == ">":
            return ExpressionBooleanGreaterThan(tokens)
        
        raise Exception("Not implemented yet")

class Statement(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        self.set_child('substatement', self.parse(tokens))
    
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
            return StatementSequential(tokens)
        
        if tokens[0] == "if":
            return StatementIfThenElseFi(tokens)
        
        if tokens[0] == "while":
            return StatementWhileDoOd(tokens)
        
        if len(tokens) >= 2 and tokens[1] == ":=":
            return StatementAssignment(tokens)
        
        if tokens[0] == "skip":
            return StatementSkip(tokens)
        
        return " - *** NOT IMPLEMENTED *** - [ " + " ".join(tokens) + " ]"

class StatementAssignment(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        [assignee, assigner] = self.parse(tokens)
        self.set_child('assignee', assignee)
        self.set_child('assigner', assigner)
    
    def parse(self, tokens):
        if tokens[1] != ":=":
            raise Exception(f"Assignement error! Tokens: {tokens}")
        assignee = Variable(tokens[0:1])
        assigner = ExpressionArithmetic(tokens[2:])
        return [assignee, assigner]

class StatementIfThenElseFi(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        
        [condition, statementTrue, statementFalse] = self.parse(tokens)
        self.set_child('condition', condition)
        self.set_child('statementTrue', statementTrue)
        self.set_child('statementFalse', statementFalse)
    
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
        
        part_condition = ExpressionBoolean(part_condition)
        part_then = Statement(part_then)
        part_else = Statement(part_else)
        return [part_condition, part_then, part_else]

class StatementSequential(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        self.set_children(self.parse(tokens))
    
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
        
        parts = [Statement(p) for p in parts]
        return parts

class StatementWhileDoOd(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        
        [condition, body] = self.parse(tokens)
        self.set_child('condition', ExpressionBoolean(condition))
        self.set_child('body', Statement(body))
    
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

class StatementSkip(Parsable):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
