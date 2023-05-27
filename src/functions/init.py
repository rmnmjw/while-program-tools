from WParserTypes import StatementSequential
from WParserTypes import StatementAssignment
from WParserTypes import StatementWhileDoOd
from WParserTypes import StatementSkip
from WParserTypes import StatementIfThenElseFi
from WParserTypes import Statement

def init(el):
    clazz = type(el)
    if clazz == Statement:
        return init(el.get_child('substatement'))
    '''Slide 46'''
    if clazz == StatementSkip:
        return el.get_label(), el
    if clazz == StatementAssignment:
        return el.get_label(), el
    if clazz == StatementSequential:
        return init(el.get_child('substatement_0'))
    if clazz == StatementIfThenElseFi:
        return el.get_child('condition').get_label(), el.get_child('condition')
    if clazz == StatementWhileDoOd:
        return el.get_child('condition').get_label(), el.get_child('condition')
    raise Exception(f'init(): Unhandled class "{clazz}"')