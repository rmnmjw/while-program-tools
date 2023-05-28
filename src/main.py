import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.resolve(), p)}')

from WParser import WParser
from WState import WState
from WDerivator import WDerivator

from flow import flow

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

S = """
x:=a+b;
y:=a*b;
while y>a+b do
    a:=a+1;
    x:=a+b
od
"""

S = WParser().parse(S)




from blocks import blocks
from kill_gen_AE import kill_AE, gen_AE
from WParserTypes import Variable
from table_helpers import print_as_table, make_lab_kill_gen_table

table = make_lab_kill_gen_table(S, blocks(S), kill_AE, gen_AE, ('Lab', 'kill_AE(B)', 'gen_AE(B)'))
print_as_table(table)





# def kill_LV(S, blk):
#     pass
# def gen_LV(S, blk):
#     pass

