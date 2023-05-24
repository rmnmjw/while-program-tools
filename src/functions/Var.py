def Var(ast):
    variables = set()
    if ast.type == 'Variable':
        variables.add(ast.get_value())
    for c in ast.get_children():
        variables.update(Var(c))
    return variables