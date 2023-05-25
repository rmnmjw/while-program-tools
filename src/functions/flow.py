import sys

sys.path.insert(1, './core')
from WAst import WAst
from WParserTypes import StatementSequential
from WParserTypes import StatementAssignment
from WParserTypes import StatementWhileDoOd
from WParserTypes import StatementIfThenElseFi
from WParserTypes import StatementSkip

from add_labels import add_labels

sys.path.insert(1, './helpers')
from OrderedSet import OrderedSet

def find_first_child(el):
    if el.get_label() != None:
        return el
    for c in el.get_children():
        return find_first_child(c)
    return None

def find_last_upper_children(el):
    clazz = type(el)
    if clazz == StatementSequential:
        c = el.get_child('substatement_1')
        return find_last_upper_children(c)
    if clazz == StatementAssignment:
        return [el]
    if clazz == StatementWhileDoOd:
        return [el]
    if clazz == StatementIfThenElseFi:
        s0 = el.get_child('statementTrue')
        s1 = el.get_child('statementFalse')
        return [s0, s1]
    if clazz == StatementSkip:
        return [el]
    raise Exception(f'find_last_upper_children(): Class "{clazz}" unhandled.')

def get_next(el):
    found_self = False
    parent = el.get_parent()
    if parent != None:
        for c in parent.get_children():
            if c == el:
                found_self = True
                continue
            if found_self:
                el_next = find_first_child(c)
                if el_next != None:
                    return el_next
        parents_next = get_next(el.get_parent())
        if parents_next != None:
            return parents_next
    return None

def flow_internal(el, source=None, candidates=set()):
    clazz = type(el)
    if clazz == WAst:
        add_labels(el)
        candidates.update(flow_internal(el.get_ast()))
        return candidates
    if clazz == StatementSequential:
        children = el.get_children()
        if source != None:
            if len(children) >= 1:
                print('source', source, flush=True, end='\n')
                first = find_first_child(children[0])
                candidates.add((source, first.get_label()))
        if len(children) == 2:
            for src in find_last_upper_children(children[0]):
                dst = find_first_child(children[1])
                if src != None and dst != None: # workaround for while etc
                    if src.get_label() != None and dst.get_label() != None: # workaround for while etc
                        candidates.add((src.get_label(), dst.get_label()))
        for c in children:
            candidates.update(flow_internal(c, source))
        return candidates
    if clazz == StatementAssignment:
        el_next = get_next(el)
        if el_next != None:
            candidates.add((el.get_label(), el_next.get_label()))
        return candidates
    if clazz == StatementWhileDoOd:
        first = find_first_child(el.get_child('body'))
        if first != None:
            candidates.add((el.get_child('condition').get_label(), first.get_label()))
        candidates.update(flow_internal(el.get_child('body'), el.get_label()))
        el_next = get_next(el)
        if el_next != None:
            candidates.add((el.get_child('condition').get_label(), el_next.get_label()))
        return candidates
    if clazz == StatementIfThenElseFi:
        condition = el.get_child('condition')
        
        sTrue = el.get_child('statementTrue')
        sTrueChild = find_first_child(sTrue)
        candidates.add((condition.get_label(), sTrueChild.get_label()))
        f = flow_internal(sTrue)
        candidates.update(flow_internal(sTrue, el.get_child('condition').get_label()))
        
        sFalse = el.get_child('statementFalse')
        sFalseChild = find_first_child(sFalse)
        candidates.add((condition.get_label(), sFalseChild.get_label()))
        candidates.update(flow_internal(sFalse, el.get_label()))
        return candidates
    if clazz == StatementSkip: # TODO: review this
        el_next = get_next(el)
        if el_next != None:
            candidates.add((el.get_label(), el_next.get_label()))
            candidates.update(flow_internal(el_next, el_next.get_label()))
        return candidates
    raise Exception(f'flow_internal(): Class "{clazz}" unhandled.')

class flow(OrderedSet):
    def __init__(self, ast):
        super().__init__()
        flow_unordered = list(flow_internal(ast))
        flow_unordered.sort()
        for f in flow_unordered:
            self.add(f)
