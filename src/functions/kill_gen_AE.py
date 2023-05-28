import os, sys, pathlib
for p in ['core', 'helpers', 'functions']: sys.path.insert(1, f'{os.path.join(pathlib.Path(__file__).parent.resolve(), p)}')

from AExp import AExp

from WParserTypes import ExpressionBooleanEquals
from WParserTypes import ExpressionBooleanGreaterThan
from WParserTypes import Statement
from WParserTypes import StatementAssignment
from WParserTypes import StatementSkip

from Var import Var

def kill_AE(S, block):
    if type(block) == StatementSkip:
        return set()
    if type(block) == StatementAssignment:
        x = block.get_child('assignee')
        return [a for a in AExp(S) if x in Var(a)]
    if type(block) in [ExpressionBooleanGreaterThan, ExpressionBooleanEquals]:
        return set()
        exit()
    raise Exception(f'Unhandled block type:\n{block}')

def gen_AE(S, block):
    if type(block) == StatementSkip:
        return set()
    if type(block) == StatementAssignment:
        x = block.get_child('assignee')
        return {a for a in AExp(block.get_child('assigner')) if x not in Var(a)}
    if type(block) in [ExpressionBooleanGreaterThan, ExpressionBooleanEquals]:
        return AExp(block)
    raise Exception(f'Unhandled block type:\n{block}')
