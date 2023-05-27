import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.parent.resolve(), p)}')

from OrderedSet import OrderedSet

def blocks(el):
    items = OrderedSet()
    if el.get_label() != None:
        items.add(el)
    for c in el.get_children():
        items.update(blocks(c))
    return items
    # return sorted(items, key=lambda el: el.get_label())