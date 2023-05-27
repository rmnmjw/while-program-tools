from WParserTypes import StatementSequential
from WParserTypes import StatementAssignment
from WParserTypes import StatementWhileDoOd
from WParserTypes import StatementSkip
from WParserTypes import StatementIfThenElseFi
from WParserTypes import Statement

def init(el, withElement=False):
    clazz = type(el)
    if clazz == Statement:
        return init(el.get_child('substatement'), withElement)
    '''Slide 46'''
    if clazz == StatementSkip:
        if withElement:
            return el.get_label(), el
        return el.get_label()
    if clazz == StatementAssignment:
        if withElement:
            return el.get_label(), el
        return el.get_label()
    if clazz == StatementSequential:
        return init(el.get_child('substatement_0'), withElement)
    if clazz == StatementIfThenElseFi:
        if withElement:
            return el.get_child('condition').get_label(), el.get_child('condition')
        return el.get_child('condition').get_label()
    if clazz == StatementWhileDoOd:
        if withElement:
            return el.get_child('condition').get_label(), el.get_child('condition')
        return el.get_child('condition').get_label()
    raise Exception(f'init(): Unhandled class "{clazz}"')