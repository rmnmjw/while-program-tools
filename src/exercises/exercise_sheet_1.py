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
print('\n\nb)', flush=True, end='\n\n')
print('Var(S) =', Var(S), flush=True, end='\n')
print('AExp(S) =', AExp(S), flush=True, end='\n')

# # # # # # # # # # # # # #  c)
print('\n\nc)', flush=True, end='\n\n')

exe = WDerivator(S, WState(output=-1, a=3, b=1, i=0))
derivation = exe.derivate(steps=20)

print(derivation.beautiful(), flush=True, end='\n\n\n')



states = list(set([state for ast, state in derivation]))
states.sort()
states = [to_spaced_block(state) for state in states]
for i in range(int(len(states)/3)):
    m = merge_lines(states[i*3:i*3+3])
    print(m, flush=True, end='\n')


print('\n\nc)', flush=True, end='\n\n')

blks = {b.get_label(): b.to_code().strip() for b in blocks(S)}

output = f"""
        ┌──────────┐       ┌──────────┐
        │{blks[2] }│<──────│{blks[1] }│<──
        └──────────┘       └──────────┘
             │
             V
        ┌──────────┐  No   ┌───────────────┐
    ┌──>│{blks[3]} │──────>│{blks[8]      }│──>
    │   └──────────┘       └───────────────┘
    │        │
    │        V 
    │   ┌──────────┐  Yes   ┌──────────────┐
    │   │{blks[4]} │──────> │{blks[5]     }│
    │   └──────────┘        └──────────────┘
    │        │ No                  │
    │        V                     V
    │ ┌──────────────┐       ┌──────────────┐
    │ │{blks[6]     }│─────> │{blks[7]     }│
    │ └──────────────┘       └──────────────┘
    │                               │
    └───────────────────────────────┘
"""
print(output, flush=True, end='\n\n')



# # # # # # # # # # # # # # EXERCISE 2 # # # # # # # # # # # # # #
# # # # # # # # # # # # # # EXERCISE 2 # # # # # # # # # # # # # #
# # # # # # # # # # # # # # EXERCISE 2 # # # # # # # # # # # # # #

print('EXERCISE 2 (Extending syntax and semantics):', flush=True, end='\n\n\n')

out = '''
Syntaxerweiterung:
    S ::= skip | ... | do S od while b ∈ Stm

Semantikerweiterung: DO-WHILE
    
    ────────────────────────────────────────────────
    <do S od while b, σ> --> <S; while b do S od, σ>

(Danch mit WHILE I bzw WHILE II fortsetzen.)
'''

print(out, flush=True, end='\n')