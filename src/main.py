import sys
sys.path.insert(1, './core')

from WParser import WParser
from WState import WState
from WAst import WAst

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

ast = WParser().parse("output")

s = WState(output=-1, a=3, b=1, i=0)
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