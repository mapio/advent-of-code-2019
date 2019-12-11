from math import atan2
from collections import defaultdict

RAW = """#...##.####.#.......#.##..##.#.
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

MAP = list(map(list, RAW.splitlines()))

def dist2(dc, dr):
  return dc * dc + dr * dr

# returns a map from {alpha: (dist2, (r, c)) for all (r, c) in direction alpha wrt (rr, cc)}
def to_los(rr, cc):
    if MAP[rr][cc] == '.': return dict()
    line_of_sight = defaultdict(list)
    for r, row in enumerate(MAP):
        for c, ch in enumerate(row):
            if (r == rr and c == cc) or ch == '.': continue
            delta = (c-cc), (r-rr)
            line_of_sight[atan2(*delta)].append((dist2(*delta), (r, c)))
    return line_of_sight

max_los = dict()
for r in range(len(MAP)):
    for c in range(len(MAP[0])):
        los = to_los(r, c)
        if len(los) > len(max_los):
            max_los = los

print('1)', len(max_los))

alphas = sorted(max_los.keys())[::-1]
n = 0
while any(len(max_los[alpha]) for alpha in alphas):
    for alpha in alphas:
        if max_los[alpha]:
            dist, (r, c) = min(max_los[alpha]) # this is the first in line of sight
            max_los[alpha].remove((dist, (r, c)))
            n += 1
            if n == 200:
              print('2)', 100 * c + r)
              break
