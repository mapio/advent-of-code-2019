from itertools import combinations

from intcomp import Computer

c = Computer('program.intcode')
c.run([])
MAP = ''.join(map(chr, c.OUTPUT))
MAPL = list(map(list, MAP.splitlines()))[:-1]

s = 0
for r in range(1, len(MAPL) - 1):
    for c in range(1, len(MAPL[0]) - 1):
        if (
            MAPL[r][c] == '#' and
            MAPL[r - 1][c] == '#' and
            MAPL[r + 1][c] == '#' and
            MAPL[r][c - 1] == '#' and
            MAPL[r][c + 1] == '#'
        ):
            s += r * c

print('1)', s)


DIR = (-1, 0), (0, 1), (1, 0), (0, -1)

def find(x, m):
    for r, row in enumerate(m):
        for c, ch in enumerate(row):
            if ch == x:
                return r, c

def is_scaf(pos, d, m):
    d = d % 4
    nxt = pos[0] + DIR[d][0], pos[1] + DIR[d][1]
    if nxt[0] < 0 or nxt[0] >= len(m): return False
    if nxt[1] < 0 or nxt[1] >= len(m[0]): return False
    return m[nxt[0]][nxt[1]] == '#'

path = []
cur = 0
pos = find('^', MAPL)
l = 0
while True:
    nxt = pos[0] + DIR[cur][0], pos[1] + DIR[cur][1]
    if is_scaf(pos, cur, MAPL):
        pos = nxt
        l += 1
    else:
        if is_scaf(pos, cur + 1, MAPL):
            cur = (cur + 1) % 4
            if l: path.append(str(l))
            path.append('R')
            l = 0
        elif is_scaf(pos, cur - 1, MAPL):
            cur = (cur - 1) % 4
            if l: path.append(str(l))
            l = 0
            path.append('L')
        else:
            path.append(str(l))
            break

P = path

for j, k, l, m, n in combinations(range(2, len(P) + 1, 2), 5):
    S = P[:j], P[k:l], P[m:n]
    if any(len(','.join(s)) > 20 for s in S): continue
    sol = []
    Ps = []
    while Ps != P:
        #print(sol)
        for n, s in enumerate(S):
            if P[len(Ps):len(Ps)+len(s)] == s:
                sol.append(n)
                Ps.extend(s)
                break
        else:
             break
    if Ps == P:
        MAIN = ','.join('ABC'[i] for i in sol)
        if len(MAIN) > 20: continue
        FUNCS = {
            'ABC'[i]: ','.join(s)
            for i, s in enumerate(S)
        }
        break

c = Computer('program.intcode')
c.MEM[0] = 2
c.run([])
c.run(list(map(ord, MAIN + '\n')))
#print(''.join(map(chr, c.OUTPUT)))
for k in 'A', 'B', 'C':
    c.run(list(map(ord, FUNCS[k] + '\n')))
    # print(''.join(map(chr, c.OUTPUT)))
c.run(list(map(ord, 'n\n'))) # C
print('2)', c.OUTPUT[-1])

