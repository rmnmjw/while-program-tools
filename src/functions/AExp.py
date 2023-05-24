def AExp(ast):
    variables = set()
    if ast.type.startswith('ExpressionArithmetic'):
        variables.add(ast.to_code())
    for c in ast.get_children():
        variables.update(AExp(c))
    return variables