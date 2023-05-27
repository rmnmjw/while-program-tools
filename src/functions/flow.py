import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.parent.resolve(), p)}')

from WParserTypes import StatementSequential
from WParserTypes import StatementAssignment
from WParserTypes import StatementWhileDoOd
from WParserTypes import StatementIfThenElseFi
from WParserTypes import StatementSkip
from WParserTypes import ExpressionBooleanEquals

from init import init
from final import final

from OrderedSet import OrderedSet

class flow(OrderedSet):
    def __init__(self, el):
        super().__init__()
        clazz = type(el)
        '''Spec conform implementation, see slide 49'''
        if clazz == StatementSkip:
            return # {}
        if clazz == StatementAssignment:
            return # {}
        if clazz == StatementSequential:
            # context
            S1 = el.get_child('substatement_0')
            S2 = el.get_child('substatement_1')
            # flow
            S1f = flow(S1)
            S2f = flow(S2)
            xf = {(l, init(S2)) for l in final(S1)}
            union = S1f.union(S2f).union(xf)
            self.update(union)
            return
        if clazz == StatementIfThenElseFi:
            # context
            b = el.get_child('condition')
            l = b.get_label()
            S1 = el.get_child('statementTrue')
            S2 = el.get_child('statementFalse')
            # flow
            S1f = flow(S1)
            S2f = flow(S2)
            xf = {(l, init(S1)), (l, init(S2))}
            union = S1f.union(S2f).union(xf)
            self.update(union)
            return
        if clazz == StatementWhileDoOd:
            # context
            S = el.get_child('body')
            b = el.get_child('condition')
            l = b.get_label()
            # flow
            Sf = flow(S)
            xf1 = {(l, init(S))}
            xf2 = {(ll, l) for ll in final(S)}
            union = Sf.union(xf1).union(xf2)
            self.update(union)
            return
        raise Exception(f'flow(): Type "{clazz}" unhandled.')
