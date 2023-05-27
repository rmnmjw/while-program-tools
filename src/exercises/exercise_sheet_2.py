import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.parent.resolve(), p)}')

from WParser import WParser
from WState import WState
from WDerivator import WDerivator

from Var import Var
from AExp import AExp
from flow import flow
from blocks import blocks
from state_printing import to_spaced_block, merge_lines

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
print('EXERCISE 1 (Live variable analysis):', flush=True, end='\n')


print('\n\na)', flush=True, end='\n\n')

print(Var(S), flush=True, end='\n')