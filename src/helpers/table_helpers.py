import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.resolve(), p)}')

from OrderedSet import OrderedSet

def print_as_table(data):
    vmax = [len(el) for el in data[0]]
    cols = len(vmax) - 1
    for d in data:
        for i, el in enumerate(d):
            vmax[i] = max(vmax[i], len(str(el)))
    vtot = sum(vmax) + (len(data[0]) - 1) * 2
    
    for y, d in enumerate(data):
        if y != 0:
            for i, v in enumerate(vmax):
                if i == 0:
                    print((v+1) * '─', flush=True, end='')
                else:
                    print((v+2) * '─', flush=True, end='')
                if i < len(vmax) -1:
                    print('┼', flush=True, end='')
            print(flush=True, end='\n')
        
        for x, c in enumerate(d):
            c = str(c)
            if c == 'set()':
                c = '{' + '}'
            print(c.rjust(vmax[x]), flush=True, end='')
            if x < cols:
                print(' │ ', flush=True, end='')
        print(flush=True, end='\n')

def make_lab_kill_gen_table(S, blks, kill_func, gen_func, header):
    result = [header]
    for b in blks:
        l = b.get_label()
        k = str(OrderedSet({k.to_code() for k in kill_func(S, b)}, no_quotes=True))
        g = str(OrderedSet({g.to_code() for g in gen_func(S, b)}, no_quotes=True))
        result.append((l, k, g))
    return result