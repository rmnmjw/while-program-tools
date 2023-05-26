from WAst import WAst
from WParserTypes import StatementSequential
from WParserTypes import StatementAssignment
from WParserTypes import StatementWhileDoOd
from WParserTypes import StatementSkip
from WParserTypes import StatementIfThenElseFi

def init(el):
    '''Slide 46'''
    clazz = type(el)
    if clazz == WAst:
        return init(el.get_ast())
    if clazz == StatementSkip:
        return el.get_label()
    if clazz == StatementAssignment:
        return el.get_label()
    if clazz == StatementSequential:
        return init(el.get_child('substatement_0'))
    if clazz == StatementIfThenElseFi:
        return el.get_child('condition').get_label()
    if clazz == StatementWhileDoOd:
        return el.get_child('condition').get_label()
    raise Exception(f'init(): Unhandled class "{clazz}"')