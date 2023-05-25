import math

from WParserBaseType import WParserBaseType
from WTokenizer import KEYWORDS

def is_number(value):
    for char in str(value):
        if char not in ["0","1","2","3","4","5","6","7","8","9"]:
            return False
    return True

class Statement(WParserBaseType):
    
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
        
        if len(tokens) == 1:
            is_probably_just_a_single_variable_access_or_number = True
            for forbidden in [' ', '>', '=', ';']:
                if forbidden in tokens[0]:
                    is_probably_just_a_single_variable_access_or_number = False
                    break
            if is_probably_just_a_single_variable_access_or_number:
                if is_number(tokens[0]):
                    return Number(tokens)
                else:
                    return Variable(tokens)
        
        # check if given tokens are an arithmetic expression
        is_arithmetic = True
        for token in tokens:
            if token in ['skip', 'if', 'while', 'fi', 'do', 'then', 'else', ':=', '>', '<', ';', 'od', '=', '¬', '∧', '∨']:
                is_arithmetic = False
                break
        if is_arithmetic:
            return ExpressionArithmetic(tokens)
        
        # check if given tokens are an boolean expression
        is_boolean = True
        for token in tokens:
            if token in ['skip', 'if', 'while', 'fi', 'do', 'then', 'else', ':=', ';', 'od']:
                is_boolean = False
                break
        if is_boolean:
            return ExpressionBoolean(tokens)
        
        raise Exception(" - *** NOT IMPLEMENTED *** - [ " + " ".join(tokens) + " ]")

class TruthValue(WParserBaseType):
    pass

class Variable(WParserBaseType):
    
    def __init__(self, tokens):
        if len(tokens) != 1:
            raise Exception(f"Variable can only have one token, but has: {len(tokens)}. Tokens: {tokens}")
        super().__init__(tokens, self.__class__.__name__)
        self.set_value(self.tokens[0])
    
    def to_code(self):
        return self.get_value()
    
class Number(WParserBaseType):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        self.set_value(self.tokens[0])
    
    def to_code(self):
        return self.get_value()
    
class ExpressionArithmeticSubstraction(WParserBaseType):
    
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
    
    def to_code(self):
        m = self.get_child("minuend").to_code()
        s = self.get_child("subtrahend").to_code()
        return f'{m} + {s}'
    
class ExpressionArithmeticAddition(WParserBaseType):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        
        [summand0, summand1] = self.parse(tokens)
        self.set_child('summand0', summand0)
        self.set_child('summand1', summand1)
    
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == '+':
            summand0 = ExpressionArithmetic(tokens[0])
            summand1 = ExpressionArithmetic(tokens[2])
            return [summand0, summand1]
        
        raise Exception(f"[{self.__class__.__name__}] NOT IMPLEMENTED YET {tokens}")
    
    def to_code(self):
        s0 = self.get_child("summand0").to_code()
        s1 = self.get_child("summand1").to_code()
        return f'{s0} + {s1}'

class ExpressionArithmetic(WParserBaseType):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        self.set_child('expression', self.parse(tokens))
    
    def parse_single_token(self, tokens):
        t = tokens[0]
        if is_number(t):
            tokens_integer = [int(t)]
            return Number(tokens_integer)
        else:
            tokens_variable = [t]
            return Variable(tokens_variable)
    
    # FIXME: make this completely dynamic
    def parse_single_assignment(self, tokens):
        if len(tokens) == 3 and tokens[1] == '-':
            return ExpressionArithmeticSubstraction(tokens)
        if len(tokens) == 3 and tokens[1] == '+':
            return ExpressionArithmeticAddition(tokens)
        if len(tokens) == 5 and tokens[0] == '(' and tokens[1] not in KEYWORDS and tokens[2] in ['+', '-', '*'] and tokens[3] not in KEYWORDS and tokens[4] == ')':
            return self.parse_single_assignment(tokens[1:4])
        raise Exception(f"NOT IMPLEMENTED YET {tokens}")
    
    def parse(self, tokens):
        if type(tokens) is str: # fixme: tokens should always be a list. where did it go wrong?
            return self.parse_single_token([tokens])
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
                r = self.parse_single_assignment(tokens)
                return r

class ExpressionBooleanGreaterThan(WParserBaseType):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        
        [left, right] = self.parse(tokens)
        self.set_child('left', left)
        self.set_child('right', right)
    
    # FIXME: make this completely dynamic
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == '>':
            left = ExpressionArithmetic(tokens[0])
            right = ExpressionArithmetic(tokens[2])
            return [left, right]
        if len(tokens) == 7 and tokens[0] not in KEYWORDS and tokens[1] == '>' and tokens[2] == '(' and tokens[3] not in KEYWORDS and tokens[4] in ['+', '-', '*'] and tokens[5] not in KEYWORDS and tokens[6] == ')':
            left = ExpressionArithmetic(tokens[0])
            right = ExpressionArithmetic(tokens[2:7])
            return [left, right]
        raise Exception(f"[{self.__class__.__name__}] Not implemented yet. Tokens: {self.tokens}")
    
    def to_code(self):
        result = f'{self.get_child("left").to_code()} > {self.get_child("right").to_code()}'
        label = self.get_label()
        if label != None:
            result = f'[{result}]^{label}'
        return result


class ExpressionBooleanEquals(WParserBaseType):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        
        [left, right] = self.parse(tokens)
        self.set_child('left', left)
        self.set_child('right', right)
    
    # FIXME: make this completely dynamic
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == '=':
            left = ExpressionArithmetic(tokens[0])
            right = ExpressionArithmetic(tokens[2])
            return [left, right]
        raise Exception(f"[{self.__class__.__name__}] Not implemented yet. Tokens: {self.tokens}")

    def to_code(self):
        l = self.get_child('left').to_code()
        r = self.get_child('right').to_code()
        result = f'{l} = {r}'
        label = self.get_label()
        if label != None:
            result = f'[{result}]^{label}'
        return result


class ExpressionBoolean(WParserBaseType):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
        self.set_child('expression', self.parse(tokens))
    
    # FIXME: make this completely dynamic
    def parse(self, tokens):
        if len(tokens) == 3 and tokens[1] == ">":
            return ExpressionBooleanGreaterThan(tokens)
        if len(tokens) == 3 and tokens[1] == "=":
            return ExpressionBooleanEquals(tokens)
        if len(tokens) == 7:
            if tokens[0] == '(' and tokens[1] not in KEYWORDS and tokens[2] in ['+', '-'] and tokens[3] not in KEYWORDS and tokens[4] == ')' and tokens[5] == '<' and tokens[6] not in KEYWORDS:
                tokens = tokens[6:7] + ['>'] + tokens[0:5]
                return ExpressionBooleanGreaterThan(tokens)
        
        raise Exception("Not implemented yet")

class StatementAssignment(WParserBaseType):
    
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
    
    def to_code(self):
        ee = self.get_child("assignee").to_code()
        er = self.get_child("assigner").to_code()
        label = self.get_label()
        ci = self.indent_code()
        result = f'{ee} := {er}'
        if label != None:
            result = f'{ci}[{result}]^{label}'
        return result

class StatementIfThenElseFi(WParserBaseType):
    
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
        
        part_condition = ExpressionBoolean([el for el in part_condition if el != ''])
        part_then = Statement([el for el in part_then if el != ''])
        part_else = Statement([el for el in part_else if el != ''])
        return [part_condition, part_then, part_else]
    
    def to_code(self):
        c = self.get_child('condition').to_code()
        t = self.get_child('statementTrue').to_code()
        f = self.get_child('statementFalse').to_code()
        ci = self.indent_code()
        result = f'{ci}if {c} then\n{t}\n{ci}else\n{f}\n{ci}fi'
        return result

class StatementSequential(WParserBaseType):
    
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
                current.append(token)
                parts.append(current)
                current = []
                continue
            current.append(token)
        if len(current) != 0:
            parts.append(current)
        
        if len(parts) == 1:
            parts = [Statement(p[0])]
            return parts
        else:
            left = parts[0:math.floor(len(parts)/2)] 
            left = [token for upper in left for token in upper]
            right = parts[math.floor(len(parts)/2):]
            right = [token for upper in right for token in upper]
            
            if left[-1] == ";":
                left = left[:-1]
            if left[0] == ";":
                left = left[1:]
            if right[-1] == ";":
                right = right[:-1]
            if right[0] == ";":
                right = right[1:]
            
            statement_left = Statement(left)
            statement_right = Statement(right)
            parts = [statement_left, statement_right]
        
        return parts
    
    def to_code(self):
        result = ""
        result = ';\n'.join([c.to_code() for c in self.get_children()])
        return result
    
   
        
        
        

class StatementWhileDoOd(WParserBaseType):
    
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
    
    def to_code(self):
        c = self.get_child("condition")
        label = c.get_label()
        ci = self.indent_code()
        result  = f'{ci}while {c.to_code()} do'
        result += f'\n{self.get_child("body").to_code()}\n{ci}od'
        return result

class StatementSkip(WParserBaseType):
    
    def __init__(self, tokens):
        super().__init__(tokens, self.__class__.__name__)
    
    def to_code(self):
        label = self.get_label()
        if label != None:
            return f'{self.indent_code()}[skip]^{label}'
        return 'skip'
