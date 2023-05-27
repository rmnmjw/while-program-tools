def draw_graph(S):
    from IPython.display import Image, display
    import graphviz
    g = graphviz.Digraph(filename='asdfg.gv')
    for c in blocks(S):
        g.node(str(c.get_label()), c.to_code() + "<sup>a</sup>")
    for src, dst in flow(S):
        g.edge(str(src), str(dst));
    print(g, flush=True, end='\n')