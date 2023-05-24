class WParserBaseType:
        
    def __init__(self, tokens, type):
        self.tokens = []
        self.parent = None
        self.type   = ""
        self.function = ""
        self.children = []
        self.value = None
        
        self.tokens = tokens
        self.set_type(type)
    
    def indent(self):
        el = self
        for i in range(1000):
            if not el.parent:
                return "\t" * (i * 2)
            el = el.parent
        return ""
    
    def set_child(self, key, value):
        value.set_parent(self)
        value.set_function(key)
        
        index = -1
        for i, el in enumerate(self.children):
            if el.get_function() == key:
                index = i
                break
        if index != -1:
            self.children[index] = value
        else:
            self.children.append(value)
    
    def set_children(self, elements):
        self.children = []
        for i, el in enumerate(elements):
            el.set_function('substatement_' + str(i))
            el.set_parent(self)
            self.children.append(el)
    
    def get_children(self):
        return self.children
    
    def get_child(self, key):
        for el in self.children:
            if el.get_function() == key:
                return el
    
    def set_parent(self, parent):
        self.parent = parent
    
    def get_parent(self):
        return self.parent
    
    def set_type(self, type):
        self.type = type
    
    def get_type(self):
        return self.type
    
    def set_function(self, function):
        self.function = function
    
    def get_function(self):
        return self.function

    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value

    def __repr__(self):
        result = ''
        result += self.indent() + f"<<{self.type}>>"
        if self.get_value() != None:
            result += "\n" + self.indent() + f"\tVALUE: {self.get_value()}"
        for i, s in enumerate(self.get_children()):
            result += "\n" + self.indent() + f"\t{s.get_function()} ({i+1}/{len(self.get_children())}):"
            if s == None:
                result += "\n#### NONE ####"
            else:
                result += "\n" + str(s)
        return result