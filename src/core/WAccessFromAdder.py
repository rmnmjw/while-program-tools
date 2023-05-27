from WParserTypes import StatementSequential
from WParserTypes import StatementWhileDoOd

from blocks import blocks
from init import init

class WAccessFromAdder:
    
    def __init__(self):
        pass
    
    def add_access_from(self, el):
        self.init = init(el)
        self.blocks = blocks(el)
        self.add(el)
        return el
    
    def find_access_parent(self, el):
        parent = el.get_parent()
        if type(parent) == StatementSequential:
            last = None
            for c in parent.get_children():
                if c == el: break
                last = c
            if last == None:
                return self.find_access_parent(parent)
            return last
        if type(parent) == StatementWhileDoOd:
            
            print(parent, flush=True, end='\n')
            exit()
            
        # print(el, flush=True, end='\n')
        print(type(parent), flush=True, end='\n')
        exit()
    
    def add(self, el):
        return el
        for i, b in enumerate(self.blocks):
            if self.init == b.get_label(): continue
            b.accessed_from = self.find_access_parent(b)
            
            if i == 3:
                print(i, flush=True, end='\n')
                exit()
            
        
        el.get_label()
        print(el, flush=True, end='\n')
        exit()
        return el