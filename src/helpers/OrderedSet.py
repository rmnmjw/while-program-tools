import collections

class OrderedSet(collections.OrderedDict):
    def __init__(self, collection=None, no_quotes=False):
        super().__init__()
        if collection != None:
            self.update(collection)
        self.no_quotes = no_quotes
    
    def __repr__(self):
        if self.no_quotes:
            result = '{'
            for i, k in enumerate(self.keys()):
                result += str(k)
                if i != len(self.keys()) - 1:
                    result += ', '
            return result + '}'
        
        return '{' + str(list(self.keys()))[1:-1] + '}'
    
    def __getitem__(self, key):
        return list(self.keys())[key]
    
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
