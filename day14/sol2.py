RAW = """
8 SPJN, 2 LJRB, 1 QMDTJ => 1 TFPRF
111 ORE => 5 GCFP
5 NGCKP => 6 QXQZ
21 RGRLZ => 7 DKVN
2 DCKF => 9 FCMVJ
7 SGHSV, 4 LZPCS => 9 DQRCZ
4 QNRH => 8 WGKHJ
135 ORE => 6 BPLFB
4 SPJN, 1 DCKF, 9 KJVZ, 1 DKVN, 4 ZKVPL, 11 TFPRF, 1 CWPVT => 8 BVMK
8 TGPV, 4 MQPLD => 2 SPFZ
11 QMDTJ, 15 LVPK, 5 LZPCS => 3 KJVZ
2 RNXF, 3 MKMQ => 6 LJRB
11 RKCXJ, 4 BJHW, 2 DKDST => 3 QNRH
3 NZHP, 1 QMDTJ => 9 BCMKN
10 DQRCZ, 1 GBJF => 7 RGRLZ
2 WLKC, 1 GBJF, 7 SPJN => 5 GBWQT
4 TGPV, 1 LTSB => 2 LZPCS
6 LJRB => 4 LQHB
3 LZPCS, 3 MDTZL, 12 DLHS => 2 CBTK
1 TGPV, 1 CQPR => 9 XQZFV
26 FSQBL => 8 HQPG
9 LQHB => 1 GBJF
7 NGCKP => 5 WLKC
9 DKDST, 1 XQZFV => 9 TPZBM
144 ORE => 9 RNXF
1 LJRB => 6 CQPR
9 MKMQ, 12 RNXF => 9 JWPLZ
5 LZPCS, 28 QMDTJ, 1 QNRH => 5 LVPK
5 TGPV, 1 HQPG => 6 FCBLK
8 LVPK, 9 DQRCZ, 1 MDTZL => 6 DCKF
1 RKCXJ, 2 LZPCS, 13 LJNJ => 1 QWFG
4 DKDST, 1 XQZFV, 10 NSXFK => 4 JRDXQ
7 QWFG, 1 BVMK, 4 BJHW, 21 QNSWJ, 3 FBTW, 3 FCBLK, 59 SPFZ, 4 GBWQT => 1 FUEL
28 LZPCS, 17 NGCKP, 1 MQPLD => 5 MDTZL
1 FCBLK, 5 WGKHJ => 7 ZKVPL
7 LJNJ => 9 BLDJP
11 FSQBL, 2 BCMKN, 1 CBTK => 9 CWPVT
1 BJHW => 1 MQPLD
11 SGHSV, 3 LJNJ => 1 NGCKP
2 FSQBL, 7 FCBLK, 1 CQPR => 4 RKCXJ
1 JRDXQ => 4 SGHSV
107 ORE => 6 MKMQ
1 DQRCZ, 3 QMDTJ, 9 XQZFV => 4 FZVH
6 NSXFK, 1 MKMQ => 6 DLHS
4 CQPR, 1 RNXF, 1 HQPG => 5 DKDST
9 RNXF => 8 LTZTR
1 LTSB, 8 BLDJP => 4 SPJN
1 FCBLK => 4 LJNJ
1 NGCKP => 3 NZHP
11 LZPCS, 22 DQRCZ, 1 QWFG, 1 QXQZ, 6 DKVN, 16 FZVH, 3 MQPLD, 23 HQPG => 3 QNSWJ
26 DLHS, 1 NSXFK => 9 BJHW
3 FCBLK, 10 HQPG => 3 LTSB
10 LTZTR, 13 JWPLZ, 16 FSQBL => 4 TGPV
11 LTSB, 1 XQZFV, 3 DQRCZ => 4 CZCJ
1 HQPG, 12 XQZFV, 17 TPZBM => 6 QMDTJ
2 LTZTR => 7 FSQBL
1 GCFP, 5 BPLFB => 1 NSXFK
3 KJVZ, 1 QXQZ, 6 DKDST, 1 FCMVJ, 2 CZCJ, 1 QNRH, 7 WLKC => 4 FBTW
"""

from collections import namedtuple, defaultdict
from math import ceil

from IPython.display import clear_output

Chem = namedtuple('Chem', 'name, qt')

def toChem(s):
    qt, name = s.strip().split(' ', 1)
    elements.add(name)
    return Chem(name, int(qt))

elements = set()
reactions = dict()
for line in RAW.splitlines()[1:]:
    frm, to = line.split('=>')
    toc = toChem(to)
    reactions[toc.name] = (toc, tuple(toChem(_) for _ in frm.split(',')))

def topsort(reactions, elements):
    L = []

    e2m = {e: None for e in elements}

    def visit(e):
        if e == 'ORE':
            e2m[e] = 'PERM'
            return
        if e2m[e] == 'PERM': return
        if e2m[e] == 'TEMP': print('Not DAG')
        e2m[e] = 'TEMP'
        for ch in reactions[e][1]:
            visit(ch.name)
        e2m[e] = 'PERM'
        L.append(e)

    while True:
        for e, m in e2m.items():
            if m == None:
                visit(e)
                break
        else:
            break

    return L[::-1]

TOPSORT = topsort(reactions, elements)

leftover = defaultdict(int)
ore = 1000_000_000_000
fuel = 0
for step in 1000_000, 100_000, 10_000, 1000, 100, 1:
    while ore >= 0:
        reqs = defaultdict(int)
        reqs['FUEL'] = step
        safe = dict(leftover)
        for e in TOPSORT:
            req = reqs[e]
            if leftover[e] < req:
                req -= leftover[e]
                leftover[e] = 0
            else:
                leftover[e] -= req
                continue
            need = reactions[e][0]
            alpha = ceil(req / need.qt)
            leftover[e] +=  alpha * need.qt - req
            #print(e, req, need, alpha, leftover[e])
            for frm in reactions[e][1]:
                reqs[frm.name] += alpha * frm.qt
            #del reqs[e]
        if reqs['ORE'] < ore:
            ore -= reqs['ORE']
            fuel += step
        else:
            leftover = defaultdict()
            leftover.update(safe)
            break

print(fuel)
