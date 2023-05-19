
from WParser import WParser

code = """
skip;
x := 0;
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

ast = WParser({"normalize": True}).parse(code)

print(ast)
