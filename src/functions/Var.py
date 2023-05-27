def Var(ast):
    variables = set()
    if ast.type == 'Variable':
        variables.add(ast)
    for c in ast.get_children():
        variables.update(Var(c))
    return variables