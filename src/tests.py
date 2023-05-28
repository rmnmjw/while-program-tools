import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.resolve(), p)}')

from blocks import blocks
from flow import flow
from kill_gen_AE import kill_AE, gen_AE
from WDerivator import WDerivator
from WParser import WParser
from WParserTypes import Variable
from WState import WState

def test(code, result=None):
    # state for eval: start
    output = -1
    a=3
    b=1
    i=0
    # state for eval: end
    if result == None:
        result = eval(code)
    state = WState(output=output, a=a, b=b, i=i)
    ast = WParser().parse(code)
    value, _ = state.eval(ast)
    return result == value

assert test("99999")
assert test("1+1")
assert test("0+0")
assert test("48464882986+21119798939")
assert test("5-4")
assert test("1+a")
assert test("b+a")
assert test("b+1")
assert test("b+999999")
assert test("1>0")
assert test("0>1")
assert test("(i + 1) < a")

state = WState(a=3)
S = WParser().parse('a+4')
assert(state.eval(S) == state(S))

S = """b:=1;i:=0;while a>i do if i=0 then b:=b+a else b:=b+1 fi;i:=i+1 od;output:=b;skip"""
S = WParser().parse(S)
# add_labels(S)
result = """[b := 1]^1;
[i := 0]^2;
while [a > i]^3 do
    if [i = 0]^4 then
        [b := b + a]^5
    else
        [b := b + 1]^6
    fi;
    [i := i + 1]^7
od;
[output := b]^8;
[skip]^9"""
assert result == S.to_code()





#
#
# kill_AE
#
#


# test kill_AE(skip)
S = WParser().parse('skip')
b = blocks(S)[0]
k = kill_AE(S, b)
assert k == set()


# test kill_AE([x:=expr]^l)
S = WParser().parse('a:=1+1;b:=a+a')
b = blocks(S)[0]
k = kill_AE(S, b)
assert k[0].to_code() == 'a + a'

# test kill_AE([b]^l)
S = WParser().parse('if 2 = 1 then skip else skip fi')
b = blocks(S)[0]
assert kill_AE(S, b) == set()


# test gen_AE(skip)
S = WParser().parse('skip')
b = blocks(S)[0]
k = gen_AE(S, b)
assert k == set()

# test gen_AE([x:=expr]^l)
S = WParser().parse('a:=1+1')
bb = blocks(S)
assert [g.to_code() for g in gen_AE(S, bb[0])][0] == '1 + 1'

S = WParser().parse('a:=a+1')
bb = blocks(S)
assert [g.to_code() for g in gen_AE(S, bb[0])] == []

# test gen_AE([b]^l)
S = WParser().parse('if 2 = 1 then skip else skip fi')
b = blocks(S)[0]
assert gen_AE(S, b) == set()