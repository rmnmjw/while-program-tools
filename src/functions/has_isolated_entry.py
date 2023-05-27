import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.parent.resolve(), p)}')

from Lab import Lab
from init import init
from flow import flow

def has_isolated_entry(S):
    return {l for l in Lab(S) if (l, init(S)) in flow(S)} == set()