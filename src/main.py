import sys

sys.path.insert(1, './core')
from WParser import WParser
from WState import WState
from WAst import WAst

sys.path.insert(1, './functions')
from flow import flow
from add_labels import add_labels
from blocks import blocks


if False:
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
    
    S = """b:=1;i:=0;while a>i do if i=0 then b:=b+a else b:=b+1 fi;i:=i+1 od;output:=b;skip"""
    S = WParser().parse(S)
    add_labels(S)
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
output := b;
skip
"""
S = WParser().parse(S)
add_labels(S)
print(S.to_code(), flush=True, end='\n')

# f = flow(S)
# print("result flow:", f, flush=True, end='\n')

    




print("done.", flush=True, end='\n')