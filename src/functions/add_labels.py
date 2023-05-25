import sys

sys.path.insert(1, '../core')
from WAst import WAst
from WParserTypes import StatementSequential
from WParserTypes import StatementAssignment
from WParserTypes import StatementWhileDoOd
from WParserTypes import StatementIfThenElseFi
from WParserTypes import StatementSkip

current_label = 1
def add_labels(el):
    global current_label
    clazz = type(el)
    if clazz == WAst:
        current_label = 1
        add_labels(el.get_ast())
        return
    if clazz == StatementSequential:
        for c in el.get_children():
            add_labels(c)
        return
    if clazz == StatementAssignment:
        el.set_label(current_label)
        current_label += 1
        return
    if clazz == StatementWhileDoOd:
        cond = el.get_child('condition').set_label(current_label)
        current_label += 1
        add_labels(el.get_child('body'))
        return
    if clazz == StatementIfThenElseFi:
        cond = el.get_child('condition').set_label(current_label)
        current_label += 1
        add_labels(el.get_child('statementTrue'))
        add_labels(el.get_child('statementFalse'))
        return
    if clazz == StatementSkip:
        el.set_label(current_label)
        current_label += 1
        return
    raise Exception(f'add_labels(): Case of type "{clazz}" is not handled.')