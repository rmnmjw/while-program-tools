from WAst import WAst
from WParserTypes import StatementSequential
from WParserTypes import StatementAssignment
from WParserTypes import StatementWhileDoOd
from WParserTypes import StatementSkip
from WParserTypes import StatementIfThenElseFi

def final(el):
    '''Slide 47'''
    clazz = type(el)
    if clazz == WAst:
        return final(el.get_ast())
    if clazz == StatementSkip:
        return {el.get_label()}
    if clazz == StatementAssignment:
        return {el.get_label()}
    if clazz == StatementSequential:
        return final(el.get_child('substatement_1'))
    if clazz == StatementIfThenElseFi:
        S1f = final(el.get_child('statementTrue'))
        S2f = final(el.get_child('statementFalse'))
        return S1f.union(S2f)
    if clazz == StatementWhileDoOd:
        return {el.get_child('condition').get_label()}
    raise Exception(f'final(): Unhandled class "{clazz}"')