import sys

sys.path.insert(0, '../core')
from WParser import WParser
from WState import WState
from WAst import WAst

sys.path.insert(0, '../functions')
from Var import Var
from AExp import AExp
from flow import flow


SHOW = True

# # # # # # # # # # # # # # EXERCISE 1 # # # # # # # # # # # # # #
# # # # # # # # # # # # # # EXERCISE 1 # # # # # # # # # # # # # #
# # # # # # # # # # # # # # EXERCISE 1 # # # # # # # # # # # # # #

S = """
b := 1;
i := 0;
while a > i do
    if i = 0 then
        b := b + a
    else
        b := b + 1
    fi;
    i := i + 1
od;
output := b
"""
S = WParser().parse(S)

# # # # # # # # # # # # # #  a)
if SHOW:
    print('EXERCISE 1 (Semantics):', flush=True, end='\n')


    print('a)', flush=True, end='\n')

    s = WState(output=-1, a=3, b=1, i=0)
    print('σ:', flush=True, end='\n')
    print(s, flush=True, end='\n')

    expressions = ['(i + 1) < a', 'b + 1', 'a + b']
    for i, expr in enumerate(expressions):
        val = s.eval(expr)
        print('(' + 'i' * (i+1) +  ')', f'\tσ({expr})', '=', val, flush=True, end='\n')

# # # # # # # # # # # # # #  b)
if SHOW:
    print('\nb)', flush=True, end='\n\n')
    print('Var(S) =', Var(S.get_ast()), flush=True, end='\n')
    print('AExp(S) =', AExp(S.get_ast()), flush=True, end='\n')

# # # # # # # # # # # # # #  c)
