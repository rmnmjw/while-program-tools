import collections

class OrderedSet(collections.OrderedDict):
    def __init__(self, collection=None):
        super().__init__()
        if collection != None:
            self.update(collection)
    
    def __repr__(self):
        return '{' + str(list(self.keys()))[1:-1] + '}'
    
    def __sort(self):
        items = list(self)
        items.sort()
        for k in items:
            del self[k]
            self[k] = None
    
    def add(self, val):
        self[val] = None
        self.__sort()
    
    def update(self, vals):
        for v in vals:
            self.add(v)
    
    def union(self, other):
        s = OrderedSet()
        for v in self:
            s.add(v)
        for v in other:
            s.add(v)
        return s
    
    # TODO: add all the other needed methods
