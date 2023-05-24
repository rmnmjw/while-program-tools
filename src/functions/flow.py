import sys

sys.path.insert(1, '../core')
from WParser import WParser
from WState import WState
from WAst import WAst

from add_labels import add_labels

def flow(ast):
    if type(ast) == WAst:
        add_labels(ast)
        print(ast, flush=True, end='\n')
    exit()
    
    
    if ast.type == 'StatementSequential':
        print(ast.get_children(), flush=True, end='\n')
        exit()
    print(ast.type, flush=True, end='\n')
    exit()
