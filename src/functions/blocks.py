import sys

sys.path.insert(1, './core')
from WAst import WAst

sys.path.insert(1, './helpers')
from OrderedSet import OrderedSet

def blocks(el):
    items = OrderedSet()
    if type(el) == WAst:
        items.update(blocks(el.get_ast()))
        return items
    if el.get_label() != None:
        items.add(el)
    for c in el.get_children():
        items.update(blocks(c))
    return items
    # return sorted(items, key=lambda el: el.get_label())