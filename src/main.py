import sys

sys.path.insert(1, './core')
from WParser import WParser
from WState import WState
from WAst import WAst

sys.path.insert(1, './functions')
from flow import flow
from add_labels import add_labels

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
exit()

# print(S, flush=True, end='\n')
# print('#################################', flush=True, end='\n')
# print('#################################', flush=True, end='\n')
# print('#################################', flush=True, end='\n')

f = flow(S)
print("result flow:", f, flush=True, end='\n')






# code = """
# skip;
# x := 0;
# if b > a then
#     x := 0
# else
#     x := 5;
#     while a > x do
#         a := a - 1
#     od
# fi;
# b := a
# """

# ast = WParser().parse(code)


# s = WState(output=-1, a=3, b=1, i=0)
# ast = WParser().parse("(i + 1) < a")
# value = s.eval(ast)





print("done.", flush=True, end='\n')