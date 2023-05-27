def to_spaced_block(state):
    out = state.get_name() + ': '
    lines = [l.strip() for l in state.beautiful().strip().split('\n')]
    out += lines[0].strip()
    left = len(out.split('|')[0])
    for l in lines[1:]:
        out += '\n' + l.split('|')[0].rjust(left) + '|' + l.split('|')[1]
    maxl = max([len(l) for l in out.split('\n')])
    out = '\n'.join([l.ljust(maxl) for l in out.split('\n')])
    return out
    
def merge_lines(blocks):
    max_lines = max([len(b.strip().split('\n')) for b in blocks])
    result = ''
    for l in range(max_lines):
        for i, b in enumerate(blocks):
            if l >= len(b.split('\n')):
                result += len(b.split('\n')[0]) * ' '
            if i != 0:
                result += '    '
            result += b.split('\n')[l]
        result += '\n'
    return result