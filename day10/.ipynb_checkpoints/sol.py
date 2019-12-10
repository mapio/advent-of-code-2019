#!/usr/bin/env python
# coding: utf-8

# In[115]:


RAW ="""#...##.####.#.......#.##..##.#.
#.##.#..#..#...##..##.##.#.....
#..#####.#......#..#....#.###.#
...#.#.#...#..#.....#..#..#.#..
.#.....##..#...#..#.#...##.....
##.....#..........##..#......##
.##..##.#.#....##..##.......#..
#.##.##....###..#...##...##....
##.#.#............##..#...##..#
###..##.###.....#.##...####....
...##..#...##...##..#.#..#...#.
..#.#.##.#.#.#####.#....####.#.
#......###.##....#...#...#...##
.....#...#.#.#.#....#...#......
#..#.#.#..#....#..#...#..#..##.
#.....#..##.....#...###..#..#.#
.....####.#..#...##..#..#..#..#
..#.....#.#........#.#.##..####
.#.....##..#.##.....#...###....
###.###....#..#..#.....#####...
#..##.##..##.#.#....#.#......#.
.#....#.##..#.#.#.......##.....
##.##...#...#....###.#....#....
.....#.######.#.#..#..#.#.....#
.#..#.##.#....#.##..#.#...##..#
.##.###..#..#..#.###...#####.#.
#...#...........#.....#.......#
#....##.#.#..##...#..####...#..
#.####......#####.....#.##..#..
.#...#....#...##..##.#.#......#
#..###.....##.#.......#.##...##
"""

DATA =list(map(list, RAW.splitlines()))


# In[121]:


from math import atan2

def d(rr, cc):
    CH = DATA[rr][cc].lower()
    if CH == '.': return dict()
    los2ch = dict()
    cmset = set()
    for r, row in enumerate(DATA):
        for c, ch in enumerate(row):
            if r == rr and c == cc: continue
            if ch != '.':
                delta = (c-cc),(r-rr)
                los = atan2(*delta)
                if los in los2ch:
                    los2ch[los].append((delta[0] * delta[0] + delta[1] * delta[1], (r, c)))
                else:
                    los2ch[los] = [(delta[0] * delta[0] + delta[1] * delta[1], (r, c))]
    return los2ch


# In[122]:


max_ast = -1
witness = None

for r in range(len(DATA)):
    for c in range(len(DATA[0])):
        #print(d(r, c) if DATA[r][c] != '.' else 0, end = ' ')
        n = d(r, c)
        if len(n) > max_ast:
            max_ast = len(n)
            witness = r, c

print(witness, max_ast)


# In[124]:


TOOUT = set([1, 2, 3, 10, 20, 30, 50, 100, 199, 200, 201, 299])

OUT = [[DATA[r][c]*2 for c in range(len(DATA[0]))] for r in range(len(DATA))]
OUT[3][8] = 'XX'
res = d(22, 17)
keys = sorted(res.keys())[::-1]
n = 0

while any(len(res[k]) for k in keys):
    for k in keys:
        if res[k]:
            delta, (r, c) = min(res[k])
            res[k].remove((delta, (r, c)))
            n += 1
            OUT[r][c] = n
            if n in TOOUT: print(n, r, c)


# In[ ]:




