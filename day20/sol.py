from collections import defaultdict
from heapq import heappop, heappush
import string

UC = frozenset(string.ascii_uppercase)
DIR = (1, 0), (0, 1), (-1, 0), (0, -1)

def read(r, c):
    if 0 <= r < NR and 0 <= c < NC: return RAW[r][c]
    return None

def bfs(r, c):
    res = []
    queue = [(0, r, c)]
    seen = set()
    while queue:
        d, r, c = queue.pop(0)
        seen.add((r, c))
        for dr, dc in DIR:
            rr, cc = r + dr, c + dc
            if (rr, cc) in seen: continue
            if d and read(rr, cc) in UC: res.append(((r, c), d))
            if read(rr, cc) == '.': queue.append((d + 1, rr, cc))
    return res

def dijkstra(f, t):
    queue= [(0, f, ())]
    seen = set()
    while queue:
        (cost, v1, path) = heappop(queue)
        if v1 not in seen:
            seen.add(v1)
            path = path + (v1, )
            if v1 == t: return (cost, path)
            for v2, w in graph[v1]:
                if v2 not in seen:
                    heappush(queue, (cost + w, v2, path))
    return float("inf"), None

def dijkstra_level(f, t):
    queue= [(0, (f, 0), ())]
    seen = set()
    while queue:
        cost, (v1, l), path = heappop(queue)
        if (v1, l) not in seen:
            seen.add((v1, l))
            path += ((v1, l), )
            if l == 0 and v1 == t: return cost, path
            for v2, w in graph[v1]:
                if port[v1] == port[v2]:
                    if v1 in IN and v2 in OUT: lp = l + 1
                    elif v1 in OUT and v2 in IN: lp = l - 1
                else: lp = l
                #print(v1, v2, l, lp)
                if lp >= 0 and ((v2, lp) not in seen):
                    heappush(queue, (cost + w, (v2, lp), path))
    return float("inf"), None


with open('maze.txt') as inf: RAW = inf.read().splitlines()

NR = len(RAW)
NC = len(RAW[0])

port = dict()

for r in range(NR):
    for c in range(NC):
        ch = read(r, c)
        if ch in UC:
            chp = read(r + 1, c)
            if chp in UC:
                if read(r + 2, c) == '.':
                    port[(r + 2, c)] = ch + chp
                elif read(r - 1, c) == '.':
                    port[(r - 1, c)] = ch + chp
            chp = read(r, c + 1)
            if chp in UC:
                if read(r, c + 2) == '.':
                    port[(r, c + 2)] = ch + chp
                elif read(r, c - 1) == '.':
                    port[(r, c - 1)] = ch + chp

src = list(port.keys())[list(port.values()).index('AA')]
dst = list(port.keys())[list(port.values()).index('ZZ')]

p2k = defaultdict(list)

for r, c in port:
    cr, cc = r - NR/2, c - NC/2
    d = cr * cr + cc * cc
    p2k[port[(r, c)]].append((d, (r, c)))

IN, OUT = set(), set()
for n, l in p2k.items():
    if len(l) == 1: continue
    l = sorted(l)
    IN.add(l[0][1])
    OUT.add(l[1][1])

graph = dict()

for p in port:
    graph[p] = bfs(*p)
    for q in port:
        if p != q and port[p] == port[q]:
            graph[p].append((q, 1))

print('1)', dijkstra(src, dst)[0])
print('2)', dijkstra_level(src, dst)[0])
