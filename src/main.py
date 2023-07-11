import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.resolve(), p)}')

from WParser import WParser
from WState import WState
from WDerivator import WDerivator

from flow import flow

# S = """
# b := 1;
# i := 0;
# while a > i do
#     if i = 0 then
#         b := b + a
#     else
#         b := b + 1
#     fi;
#     i := i + 1
# od;
# output := b
# """

# S = """
# x:=a+b;
# y:=a*b;
# while y>a+b do
#     a:=a+1;
#     x:=a+b
# od
# """

S = '''
x:=2;
y:=4;
x:=1;
if y>0 then
    z:=x
else
    z:=y*y
fi;
x:=z
'''

S = WParser().parse(S)




# from blocks import blocks
from init import init
from kill_gen_AE import kill_AE, gen_AE
from kill_gen_LV import kill_LV, gen_LV
from WParserTypes import Variable
from OrderedSet import OrderedSet
from table_helpers import print_as_table, make_lab_kill_gen_table

# table = make_lab_kill_gen_table(S, blocks(S), kill_AE, gen_AE, ('Lab', 'kill_AE(B)', 'gen_AE(B)'))
# print_as_table(table)

table = make_lab_kill_gen_table(S, S.blocks(), kill_LV, gen_LV, ('Lab', 'kill_LV(B)', 'gen_LV(B)'))
print_as_table(table)


# S.phi_LV(1, set())

exit()

def phi_AE(S, l, A):
    blks = blocks(S)
    tmp = A - set(kill_AE(S, blks(l)))
    return tmp | gen_AE(S, blks(l))

def AE(S, l):
    if l == init(S):
        return set()
    
    flows = {(lll, ll) for (lll, ll) in flow(S) if ll == l}
    print(flows, flush=True, end='\n')
    exit()
    x = [phi_AE(S, lll, AE(S, lll)) for lll, _ in flows]
    if len(x) == 0:
        return set()
    if len(x) == 1:
        return x[0]
    else:
        raise Exception('NYI')

# AE_l = {}
# for l in [1, 2, 3]:# [b.get_label() for b in blocks(S)]:
#     AE_l[l] = AE(S, l)
# print(AE_l, flush=True, end='\n')
# exit()

# AE_1 = AE(S, init(S))
# print(AE_1, flush=True, end='\n')
# AE_2 = AE(S, blocks(S)[1].get_label())
# print(AE_2, flush=True, end='\n')
AE_3 = AE(S, blocks(S)[2].get_label())
print(AE_3, flush=True, end='\n')


# def kill_LV(S, blk):
#     pass
# def gen_LV(S, blk):
#     pass

