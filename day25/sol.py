from collections import deque
from itertools import chain, combinations

from intcomp import Computer

c = Computer('program.intcode')
PRG = c.MEM[:]

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def parse(out):
    indir = False
    inobj = False
    dirs = []
    objs = []
    for line in out.splitlines():
        if indir:
            if line.startswith('-'):
                dirs.append(line[2:])
            else:
                indir = False
        if inobj:
            if line.startswith('-'):
                objs.append(line[2:])
            else:
                inobj = False
        if line.startswith('Doors here lead'):
            indir = True
        elif line.startswith('Items here'):
            inobj = True
        elif line.startswith('=='):
            room = line[3:-3]
    return room, dirs, objs

def dir2input(d):
    return list(map(ord, d + '\n'))

def output2str(out):
    return ''.join(map(chr, out))

def find(src, dst):
    seen = set()
    found = []
    def _r(path, node):
        if found: return
        if node == dst:
            found.extend(path)
            return
        seen.add(node)
        for f, t, d in ARCS:
            if f == node and t not in seen:
                _r(path + [d], t)
    _r([], src)
    return found

c = Computer(PRG)
c.run([])
room, dirs, objs = parse(output2str(c.OUTPUT))
ARCS = set()
queue = deque([d] for d in dirs)
seen = set()
while queue:
    path = queue.popleft()
    c = Computer(PRG)
    c.run([])
    dst, _, _ = parse(output2str(c.OUTPUT))
    for d in path:
        c.run(dir2input(d))
        room, dirs, objs = parse(output2str(c.OUTPUT))
        src = dst
        dst = room
    ARCS.add((src, dst, d))
    if room in seen: continue
    seen.add(room)
    for d in dirs: queue.append(path + [d])

DANGER = {'molten lava', 'escape pod', 'infinite loop', 'giant electromagnet', 'photons'}
DEST = 'Crew Quarters', 'Stables', 'Storage', 'Navigation', 'Passages', 'Observatory'

visit = []
for d in DEST:
    visit.extend(find('Hull Breach', d) + find(d, 'Hull Breach'))
visit.extend(find('Hull Breach', 'Security Checkpoint'))

c = Computer(PRG)
c.run([])
inv = set()
for d in visit:
    c.run(dir2input(d))
    room, dirs, objs = parse(output2str(c.OUTPUT))
    for o in objs:
        if o in DANGER: continue
        inv.add(o)
        c.run(dir2input('take ' + o))
for o in inv:
    c.run(dir2input('drop ' + o))

for ss in powerset(inv):
    if not ss: continue
    for o in ss: c.run(dir2input('take ' + o))
    c.run(dir2input('south'))
    out = output2str(c.OUTPUT)
    if 'lighter' in out:
        print('lighter = ', ss)
    elif 'heavier' in out:
        print('heavier = ', ss)
    else:
        print(out)
        break
        print('? = ', ss)
    for o in ss: c.run(dir2input('drop ' + o))
