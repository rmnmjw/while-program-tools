import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.resolve(), p)}')

from WParser import WParser
from WState import WState
from WDerivator import WDerivator

from flow import flow

def do_some_testing():
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
        value = state.eval(ast)
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

    exit()
# do_some_testing()















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
# print(S.to_code(), flush=True, end='\n')


# exe = WDerivator(S, WState(output=-1, a=3, b=1, i=0))

# print(exe.derivate().beautiful(), flush=True, end='\n')
