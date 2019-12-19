from itertools import repeat, chain, islice, cycle, tee

import numpy as np

PATTERN = 0, 1, 0, -1
IN = '59718730609456731351293131043954182702121108074562978243742884161871544398977055503320958653307507508966449714414337735187580549358362555889812919496045724040642138706110661041990885362374435198119936583163910712480088609327792784217885605021161016819501165393890652993818130542242768441596060007838133531024988331598293657823801146846652173678159937295632636340994166521987674402071483406418370292035144241585262551324299766286455164775266890428904814988362921594953203336562273760946178800473700853809323954113201123479775212494228741821718730597221148998454224256326346654873824296052279974200167736410629219931381311353792034748731880630444730593'

def pat(i, j, k = None):
    base = chain.from_iterable(repeat(d, i + 1) for d in PATTERN)
    return islice(cycle(base), j + 1, k)

def fft(l):
    if len(l) <= 2: return l
    h = len(l)//2
    a, b = l[:h], l[h:]
    u = fft(a) + np.array([np.dot(b, list(pat(i, h, 1 + 2 * h))) for i in range(h)])
    return np.concatenate((u, np.cumsum(b[::-1])[::-1]))

def sfft(s):
    return ''.join(str(abs(d) % 10) for d in fft(np.array(list(map(int, s)))))

s = IN + '0' * (1024 - len(IN))
for _ in range(100):
    s = sfft(s)

print('1)', s[:8])


TAIL = np.array(list(map(int, (IN * 10000)[int(IN[:7]):])))[::-1]
for _ in range(100):
    TAIL = TAIL.cumsum() % 10

print('2)', ''.join(map(str, TAIL[::-1][:8])))
