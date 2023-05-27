import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.parent.resolve(), p)}')

from Lab import Lab
from init import init
from flow import flow
from final import final


def has_isolated_exits(S):
    return {ll for ll in Lab(S) for l in final(S) if (l, ll) in flow(S)} == set()