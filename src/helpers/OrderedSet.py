import collections

class OrderedSet(collections.OrderedDict):
    def __init__(self):
        super().__init__()
    
    def __repr__(self):
        return '{' + str(list(self.keys()))[1:-1] + '}'
    
    def add(self, val):
        self[val] = None
    
    def update(self, vals):
        for v in vals:
            self[v] = None
    
    # TODO: add all the other needed methods
