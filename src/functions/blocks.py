import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.parent.resolve(), p)}')

from OrderedSet import OrderedSet

class blocks(OrderedSet):
    
    def __init__(self, el):
        super().__init__()
        if el.get_label() != None:
            self.add(el)
        for c in el.get_children():
            self.update(blocks(c))
    
    def __call__(self, label):
        for i in self.keys():
            if i.get_label() == label:
                return i
        return None
