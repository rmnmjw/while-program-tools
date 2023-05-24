import sys
sys.path.insert(1, './core')

from WParser import WParser
from WState import WState
from WAst import WAst

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






s = WState(output=-1, a=3, b=1, i=0)
ast = WParser().parse("a+b")
value = s.eval(ast)
print('value', value, flush=True, end='\n')
exit()





val = s.eval(ast)
print('val', val, flush=True, end='\n')
# print(s, flush=True, end='\n')
# state = {
#     'output': -1,
#     'a': 3,
#     'b': 1,
#     'i': 0
# }

# print(state, flush=True, end='\n')


