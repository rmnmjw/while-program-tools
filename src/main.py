
from WParser import WParser

code = """
skip;
if b > a then
    x := 0
else
    x := 5;
    while a > x do
        a := a - 1
    od
fi;
b := a
"""

ast = WParser({"simplify": False}).parse(code)

print(ast)
