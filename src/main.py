import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.resolve(), p)}')

from WParser import WParser
from WState import WState
from WDerivator import WDerivator

from flow import flow

S = """
b := 2;
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
output := b;
skip
"""

S = WParser().parse(S)




from blocks import blocks
from kill_gen_AE import kill_AE, gen_AE
from WParserTypes import Variable



