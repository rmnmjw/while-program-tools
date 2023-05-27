import sys

sys.path.insert(0, './core')
from WParser import WParser
from WState import WState
from WDerivator import WDerivator

sys.path.insert(0, './functions')
from Var import Var
from AExp import AExp
from flow import flow



SHOW = True
# SHOW = False

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


    print('\n\na)', flush=True, end='\n\n')

    state = WState(output=-1, a=3, b=1, i=0)
    print('σ:', flush=True, end='\n')
    print(state.beautiful(), flush=True, end='\n')

    expressions = ['(i + 1) < a', 'b + 1', 'a + b']
    for i, expr in enumerate(expressions):
        value, state = state.eval(expr)
        print('(' + 'i' * (i+1) +  ')', f'\tσ({expr})', '=', value, flush=True, end='\n')

# # # # # # # # # # # # # #  b)
if SHOW:
    print('\n\nb)', flush=True, end='\n\n')
    print('Var(S) =', Var(S), flush=True, end='\n')
    print('AExp(S) =', AExp(S), flush=True, end='\n')

# # # # # # # # # # # # # #  c)

print('\n\nc)', flush=True, end='\n\n')

exe = WDerivator(S, WState(output=-1, a=3, b=1, i=0))
derivation = exe.derivate(steps=20)

print(derivation.beautiful(), flush=True, end='\n')

for ast, state in derivation:
    print(state.get_name(), ':', flush=True, end='\n')
    print(state.beautiful(), flush=True, end='\n')
