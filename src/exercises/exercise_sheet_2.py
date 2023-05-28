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
# from kill_gen_AE import kill_LV

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


print('\n\na)', flush=True, end='\n')

vs = {v.to_code() for v in Var(S)}
print('\tVar_* = {vs}', flush=True, end='\n\n')


print('\nb)', flush=True, end='\n')

print('###########################################################', flush=True, end='\n')


result = []
for b in blocks(S):
    print(b, flush=True, end='\n')
    exit()
print(blks, flush=True, end='\n')