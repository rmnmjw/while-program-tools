import sys

sys.path.insert(1, './core')
from WParserTypes import ExpressionBooleanGreaterThan
from WParserTypes import Statement
from WParserTypes import StatementAssignment
from WParserTypes import StatementIfThenElseFi
from WParserTypes import StatementSequential
from WParserTypes import StatementSkip
from WParserTypes import StatementWhileDoOd
from WParserTypes import ExpressionArithmeticAddition

sys.path.insert(1, './functions')
from flow import flow
from blocks import blocks


class WLabelizer:
    
    def __init__(self):
        pass
    
    def labelize(self, el):
        self.current_label = 1
        self.add_labels(el)
        return el
    
    def add_labels(self, el):
        clazz = type(el)
        if clazz == Statement:
            for c in el.get_children():
                self.add_labels(c)
            return
        if clazz == StatementSequential:
            for c in el.get_children():
                self.add_labels(c)
            return
        if clazz == StatementAssignment:
            el.set_label(self.current_label)
            self.current_label += 1
            return
        if clazz == StatementWhileDoOd:
            cond = el.get_child('condition').set_label(self.current_label)
            self.current_label += 1
            self.add_labels(el.get_child('body'))
            return
        if clazz == StatementIfThenElseFi:
            cond = el.get_child('condition').set_label(self.current_label)
            self.current_label += 1
            self.add_labels(el.get_child('statementTrue'))
            self.add_labels(el.get_child('statementFalse'))
            return
        if clazz == StatementSkip:
            el.set_label(self.current_label)
            self.current_label += 1
            return
        if clazz == ExpressionBooleanGreaterThan:
            el.set_label(self.current_label)
            self.current_label += 1
            return
        if clazz == ExpressionArithmeticAddition:
            el.set_label(self.current_label)
            self.current_label += 1
            return
        raise Exception(f'Labelizer.add_labels(): Case of type "{clazz}" is not handled.')
    
