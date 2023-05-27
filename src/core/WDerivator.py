from copy import deepcopy

from WParserBaseType import Deleted
from WParserTypes import ExpressionBooleanEquals
from WParserTypes import ExpressionBooleanGreaterThan
from WParserTypes import Statement
from WParserTypes import StatementAssignment
from WParserTypes import StatementIfThenElseFi
from WParserTypes import StatementSequential
from WParserTypes import StatementSkip
from WParserTypes import StatementWhileDoOd
from WState import WState

from init import init

class Derivation:
    def __init__(self, derivation):
        self.derivation = derivation
    
    def __iter__(self):
        for d in self.derivation:
            yield d
    
    def beautiful(self):
        result = ''
        ast, state = self.derivation[0]
        result += f'<{ast.get_name()}, {state.get_name()}> = '
        
        for i, (ast, state) in enumerate(self):
            pre = ''
            if i != 0:
                pre = '\n\t-> '
            if ast != None:
                code = ast.to_code(show_labels=False).replace('\n', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
                result += f'{pre}<{code}, {state.get_name()}>'
            else:
                result += f'{pre}{state.get_name()}'
        return result

class WDerivator:
    
    def __init__(self, ast, state):
        self.derivation = [(deepcopy(ast), deepcopy(state))]
    
    def last(self):
        ast = deepcopy(self.derivation[-1][0])
        state = deepcopy(self.derivation[-1][1])
        return ast, state
    
    def step_finish(self, ast, state):
        assert type(ast) == Statement
        assert type(state) == WState
        if type(ast.get_child('substatement')) == Deleted:
            ast = None
        self.derivation.append((ast, state))
        return ast, state
    
    def step(self):
        ast, state = self.last()
        _, subject = init(ast, True)
        if type(subject) == StatementAssignment:
            value, state = state.eval(subject)
            state.increment_counter()
            if subject.get_parent() != None:
                subject.get_parent().remove_child(subject)
            return self.step_finish(ast, state)
        if type(subject) == StatementSkip:
            subject.get_parent().remove_child(subject)
            return self.step_finish(ast, state)
        if type(subject) in [ExpressionBooleanGreaterThan, ExpressionBooleanEquals]:
            value, state = state.eval(subject)
            if type(subject.get_parent()) == StatementWhileDoOd and subject.get_function() == 'condition':
                if value: # result is True
                    new_node = StatementSequential()
                    new_node.set_child('substatement_0', deepcopy(subject.get_parent().get_child('body')))
                    new_node.set_child('substatement_1', deepcopy(subject.get_parent()))
                    to = subject.get_parent().get_parent()
                    fun = subject.get_parent().get_function()
                    to.set_child(fun, new_node)
                    return self.step_finish(ast, state)
                else: # result is False
                    pp = subject.get_parent().get_parent()
                    if pp != None:
                        pp.remove_child(subject.get_parent())
                        return self.step_finish(ast, state)
                    else:
                        raise Exception('Derivator.step(): NOT IMPLEMENTED YET.')
            elif type(subject.get_parent()) == StatementIfThenElseFi and subject.get_function() == 'condition':
                dst = subject.get_parent().get_function()
                if value:
                    dst_src = subject.get_parent().get_child('statementTrue').get_function()
                else:
                    dst_src = subject.get_parent().get_child('statementFalse').get_function()
                subject.get_parent().get_parent().pull_up(dst, dst_src)
                return self.step_finish(ast, state)
            else:
                raise Exception('Derivator.step(): NOT IMPLEMENTED YET.')
        raise Exception(f'Derivator.step(): Type "{type(subject)}" not handled.')
    
    def derivate(self, steps=9999999):
        assert steps > 0
        i = 0
        while True:
            i += 1
            if i > steps:
                break
            if i > 999999:
                raise Exception(f'WDerivator.derivate(): Executed too many steps.')
            ast, _ = self.step()
            if ast == None:
                break
        return Derivation(self.derivation)
        
