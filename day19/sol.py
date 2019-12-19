from intcomp import Computer
from operator import itemgetter

c = Computer('program.intcode')
PRG = c.MEM[:]

def row(y, f, l):
    res = []
    for x in range(f, l + 1):
        c = Computer(PRG)
        c.run([x, y])
        res.append((x, y, c.OUTPUT[0]))
    return res

def first_last(y):
    x = y // 2
    first_x = -1
    last_x = -1
    while x < 2 * y:
        c = Computer(PRG)
        c.run([x, y])
        if c.OUTPUT[0]:
            if first_x < 0: first_x = x
        else:
            if first_x >= 0: break
        x += 1

    last_x = x - 1
    return first_x, last_x

tot = 0
for y in range(50):
    tot += sum(map(itemgetter(2), row(y, 0, 50)))

print('1)', tot)

res = []
for y in range(945, 945 + 110):
    res.append(first_last(y))

found = 0
for h in range(0, 10):
    delta = 1 + min(map(itemgetter(1), res[h: h + 100])) - max(map(itemgetter(0), res[h : h + 100]))
    if delta == 100:
        found = 945 + h
        break

print('2)', 10000 * (first_last(found)[1] - 100 + 1) + 948)

