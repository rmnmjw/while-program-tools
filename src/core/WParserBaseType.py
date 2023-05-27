class WParserBaseTypeInternal:
        
    def __init__(self, tokens, type):
        self.label = None
        self.tokens = []
        self.parent = None
        self.type   = ""
        self.function = ""
        self.children = []
        self.value = None
        self.name = 'S'
        
        self.tokens = tokens
        self.set_type(type)
        
        self.accessed_from = None
    
    def get_name(self):
        return self.name
    
    def indent(self):
        el = self
        for i in range(1000):
            if not el.parent:
                return "\t" * (i * 2)
            el = el.parent
        return ""
    
    def indent_code(self):
        el = self.get_parent()
        c = 0
        for i in range(1000):
            if not el:
                return c * '    '
            clazzName = type(el).__name__
            if clazzName == 'StatementSequential':
                pass
            elif clazzName == 'StatementWhileDoOd':
                c += 1
            elif clazzName == 'StatementIfThenElseFi':
                c += 1
            elif clazzName == 'Statement':
                pass
            else:
                raise Exception(f'WParserBaseType.indent_code(): class "{clazzName}" is not handled.')
            el = el.parent
        return ""
    
    def set_label(self, label):
        self.label = label
    
    def get_label(self):
        return self.label
    
    def set_child(self, key, value):
        if value != None:
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
    
    def remove_child(self, child):
        self.set_child(child.get_function(), Deleted())
        print(self.get_parent(), flush=True, end='\n')
        exit()
    
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
        if self.label != None:
            result += self.indent() + f"[<<{self.type}>>] {self.label}"
        else:
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
    
    def __lt__(self, other):
        return self.get_label() < other.get_label()
    
    def __le__(self, other):
        return self.get_label() <= other.get_label()
    
    def __gt__(self, other):
        return self.get_label() > other.get_label()
    
    def __ge__(self, other):
        return self.get_label() >= other.get_label()

class Deleted(WParserBaseTypeInternal):
    def __init__(self):
        super().__init__([], self.__class__.__name__)
        pass

class WParserBaseType(WParserBaseTypeInternal):
    
    def pull_up(self, dst, dst_src):
        el_dst = self.get_child(dst)
        el_dst_src = el_dst.get_child(dst_src)
        self.set_child(dst, el_dst_src)
    
    def remove_child(self, child):
        self.set_child(child.get_function(), Deleted())
        parent = self.get_parent()
        clazz = type(parent).__name__
        if parent == None:
            remaining = [c for c in self.get_children() if type(c) != Deleted]
            if len(remaining) == 1:
                self = remaining[0]
                return
            if len(remaining) == 0:
                return # were probably done here with derivating
        else:
            if clazz == 'StatementSequential':
                remaining = [c for c in self.get_children() if type(c) != Deleted]
                if len(remaining) == 1:
                    parent.pull_up(self.get_function(), remaining[0].get_function())
                    return
            if clazz == 'Statement':
                remaining = [c for c in self.get_children() if type(c) != Deleted]
                if len(remaining) == 1:
                    parent.pull_up(self.get_function(), remaining[0].get_function())
                    return
        raise Exception(f'WParserBaseType.remove_child(): class "{clazz}" is not handled.')
    
