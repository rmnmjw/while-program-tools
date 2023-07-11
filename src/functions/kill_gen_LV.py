import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.resolve(), p)}')

from AExp import AExp

from WParserTypes import ExpressionBooleanEquals
from WParserTypes import ExpressionBooleanGreaterThan
from WParserTypes import Statement
from WParserTypes import StatementAssignment
from WParserTypes import StatementSkip

from Var import Var

def kill_LV(S, block):
    if type(block) == StatementSkip:
        return set()
    if type(block) == StatementAssignment:
        return [block.get_child('assignee')]
    if type(block) in [ExpressionBooleanGreaterThan, ExpressionBooleanEquals]:
        return set()
    raise Exception(f'Unhandled block type:\n{block}')

def gen_LV(S, block):
    if type(block) == StatementSkip:
        return set()
    if type(block) == StatementAssignment:
        a = block.get_child('assigner')
        return Var(a)
    if type(block) in [ExpressionBooleanGreaterThan, ExpressionBooleanEquals]:
        return Var(block)
    raise Exception(f'Unhandled block type:\n{block}')
