from collections import deque

from intcomp import Computer

cs = []
qs = []
for addr in range(50):
    c = Computer('program.intcode')
    c.run([addr])
    cs.append(c)
    qs.append(deque())

NAT = None, None
pNAT = None, None
done = False
while not done:
    active = 0
    for c, q in zip(cs, qs):
        if q:
            x, y = q.popleft()
            c.run([x,y])
        else:
            c.run([-1])
        if c.OUTPUT:
            active += 1
            for addr, x, y in zip(c.OUTPUT[::3], c.OUTPUT[1::3], c.OUTPUT[2::3]):
                if addr == 255:
                    if NAT[1] == None:
                        print('1)', y)
                    NAT = x, y
                else:
                    qs[addr].append((x, y))
    if not (any(map(len, qs)) or active):
        if pNAT == NAT:
            print('2)', NAT[1])
            done = True
        pNAT = NAT
        qs[0].append(NAT)
