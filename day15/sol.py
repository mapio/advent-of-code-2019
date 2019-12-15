from collections import defaultdict
from operator import itemgetter

from intcomp import Computer

DIR = [(0, -1), (0, 1), (-1, 0), (1, 0)]
REV = [None, 2, 1, 4, 3]

UNKNOWN, WALL, EMPTY, PLANT = -1, 0, 1, 2
s2s = {
    UNKNOWN: '?',
    WALL: '#',
    EMPTY: '.',
    PLANT: 'T'
}

def render(world, pos = None):
    cols = [0] + list(map(itemgetter(0), world.keys()))
    rows = [0] + list(map(itemgetter(1), world.keys()))
    rr = min(rows), max(rows)
    cr = min(cols), max(cols)
    RENDER = [[' ' for c in range(cr[1] - cr[0] + 1)] for r in range(rr[1] - rr[0] + 1)]
    plant = None
    for (col, row), s in world.items():
        y = row - rr[0]
        x = col - cr[0]
        RENDER[y][x] = s2s[s]
        if s == PLANT: plant = x, y
    RENDER[0 - rr[0]][0 - cr[0]] = 'S'
    if plant is not None: RENDER[plant[1]][plant[0]] = 'T'
    if pos is not None: RENDER[pos[1] - rr[0]][pos[0] - cr[0]] = '*'

    print('\033[2J' + '\033[H')
    print('\n'.join(''.join(row) for row in RENDER))
    return RENDER

with open('program.intcode') as inf: PRG = list(map(int, inf.read().split(',')))

world = defaultdict(lambda : UNKNOWN)

bag = [([], (0, 0))]
done = False
while bag:

    path, pos = bag.pop(0)
    c = Computer(PRG)
    if path: c.run(path)

    for n, d in enumerate(DIR, 1):
        next_pos = (pos[0] + d[0], pos[1] + d[1])
        if world[next_pos] != UNKNOWN: continue
        c.run([n])
        info = world[next_pos] = c.OUTPUT[0]

        render(dict(world), pos)

        if info == PLANT:
            done = True
            result = path + [n]
            break

        if info == EMPTY:
            bag.append((path + [n], next_pos))
            c.run([REV[n]])



def t(x):
    if x == 'S': return '.'
    if x == 'T': return 'O'
    return x

RENDER = render(dict(world))

STATUS = [
    [[t(c) for c in row] for row in RENDER],
    [[t(c) for c in row] for row in RENDER]
]

def ox(m, r, c):
    for d in DIR:
        try:
            if m[r + d[0]][c + d[1]] == 'O': return True
        except IndexError:
            pass
    return False

nxt = 0
rounds = 0
while any('.' in row for row in STATUS[nxt]):
    rounds += 1
    curr = nxt
    nxt = 1 - curr
    for r, row in enumerate(STATUS[curr]):
        for c, s in enumerate(row):
            if s != '.':
                STATUS[nxt][r][c] = s
            elif ox(STATUS[curr], r, c):
                STATUS[nxt][r][c] = 'O'

    print('\033[2J' + '\033[H')
    print('\n'.join(''.join(row) for row in STATUS[nxt]))


print('1)', len(result))
print('2)', rounds)

