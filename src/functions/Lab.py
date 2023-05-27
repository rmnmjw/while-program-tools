from blocks import blocks

def Lab(S):
    return {b.get_label() for b in blocks(S)}
