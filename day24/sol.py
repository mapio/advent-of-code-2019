RAW = """.#..#
.#.#.
#..##
.#.##
##..#
"""

MAT = tuple(map(tuple, RAW.splitlines()))
N = 5

def m(mat, r, c):
    if 0 <= r < N and 0 <= c < N:
        return mat[r][c]
    return 0

def bd(mat):
    return int('0b' + ''.join(map(str, mat[0] + mat[1] + mat[2] + mat[3] + mat[4]))[::-1], 2)

mat = [[1 if MAT[r][c] == '#' else 0 for c in range(N)] for r in range(N)]


seen = set()
while True:
    y = bd(mat)
    nxt = [[0] * 5 for _ in range(N)]
    if y in seen:
        print('1)', y)
        break
    seen.add(y)
    for r in range(N):
        for c in range(N):
            a = m(mat, r, c)
            s = m(mat, r - 1, c) + m(mat, r + 1, c) + m(mat, r, c - 1) + m(mat, r, c + 1)
            if a == 1 and s != 1: nxt[r][c] = 0
            elif a == 0 and 0 < s < 3: nxt[r][c] = 1
            else: nxt[r][c] = mat[r][c]
    mat = nxt



def mr(matl, l, r, c, d = None):
    if d == None:
        #print('n', l, r, c)
        return matl[l][r][c] if l in matl and 0<= r < N and 0<= c < N else 0

    if r == 0 and d == 'UP':
        #print('u', l, r, c)
        return mr(matl, l - 1, 1, 2)
    if r == 4 and d == 'DOWN':
        return mr(matl, l - 1, 3, 2)

    if c == 0 and d == 'LEFT':
        return mr(matl, l - 1, 2, 1)
    if c == 4 and d == 'RIGHT':
        #print('r', l, r, c)
        return mr(matl, l - 1, 2, 3)

    if r == 1 and c == 2 and d == 'DOWN':
        return sum(mr(matl, l + 1, 0, _) for _ in range(N))
    if r == 2 and c == 1 and d == 'RIGHT':
        return sum(mr(matl, l + 1, _, 0) for _ in range(N))
    if r == 2 and c == 3 and d == 'LEFT':
        return sum(mr(matl, l + 1, _, 4) for _ in range(N))
    if r == 3 and c == 2 and d == 'UP':
        return sum(mr(matl, l + 1, 4, _) for _ in range(N))

    if d == 'UP':
        return mr(matl, l, r - 1, c)
    if d == 'DOWN':
        return mr(matl, l, r + 1, c)
    if d == 'LEFT':
        return mr(matl, l, r, c - 1)
    if d == 'RIGHT':
        return mr(matl, l, r, c + 1)

def mknxtl(l):
    d = {l:[[0] * 5 for _ in range(N)] for l in range(-l, l + 1)}
    for l in range(-l, l + 1): d[l][2][2] = None
    return d

T = 200
matl = {0: [[1 if MAT[r][c] == '#' else 0 for c in range(N)] for r in range(N)]}
for t in range(1, 1 + T):
    nxtl = mknxtl(t)
    for l in range(-t, t + 1):
        for r in range(N):
            for c in range(N):
                if r == 2 and c == 2: continue
                a = mr(matl, l, r, c)
                s = sum(mr(matl, l, r, c, d) for d in ('UP', 'DOWN', 'RIGHT', 'LEFT'))
                if a == 1 and s != 1: nxtl[l][r][c] = 0
                elif a == 0 and 0 < s < 3: nxtl[l][r][c] = 1
                else: nxtl[l][r][c] = a
    matl = nxtl

s = 0
for v in matl.values():
    v[2][2] = 0
    s += sum(sum(r) for r in v)
print('2)', s)
