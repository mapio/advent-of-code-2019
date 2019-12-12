from collections import namedtuple
from itertools import combinations
from math import gcd
from operator import attrgetter

def lcm(*lst):
    lcm = lst[0]
    for n in lst[1:]:
        lcm = lcm * n // gcd(lcm, n)
    return lcm

def sign(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0

Point = namedtuple('Point', 'x, y, z')
Point.sumabs = lambda self: abs(self.x) + abs(self.y) + abs(self.z)
Point.sign = lambda self: Point(sign(self.x), sign(self.y), sign(self.z))
Point.minus = lambda self, other: Point(self.x - other.x, self.y - other.y, self.z - other.z)
Point.plus = lambda self, other: Point(self.x + other.x, self.y + other.y, self.z + other.z)

class Moon:

    def __init__(self, x, y, z):
        self.pos = Point(x, y, z)
        self.vel = Point(0, 0, 0)

    def __eq__(self, other):
        return self.pos == other.pos and slef.vel == other.vel

    def __hash__(self):
        return hash(self.pos) + 31 * hash(self.vel)

    def __repr__(self):
        return 'pos = {}, vel = {}'.format(self.pos, self.vel)

    def apply_velocity(self):
        self.pos = self.pos.plus(self.velocity)

    def energy(self):
        return self.pos.sumabs() * self.vel.sumabs()

def apply_gravity(moons):
    def uv(m, n):
        first = n.pos.minus(m.pos).sign()
        second = m.pos.minus(n.pos).sign()
        m.vel = m.vel.plus(first)
        n.vel = n.vel.plus(second)
    for m, n in combinations(moons, 2):
        uv(m, n)

def apply_velocity(moons):
    for m in moons:
        m.pos = m.pos.plus(m.vel)

def simulate(moons, steps):
    for _ in range(steps):
        apply_gravity(moons)
        apply_velocity(moons)
        #print(energy(moons))

def determine_cycle(moons):
    moons = tuple(moons[:])
    seen = set()
    seen.add(moons)
    n = 1
    while True:
        if n % 1000 == 0: print('.', end = '')
        simulate(moons, 1)
        if moons in seen: return n
        seen.add(moons)
        n += 1

def energy(moons):
    return sum(m.energy() for m in moons)

def proj(v):
    gv = attrgetter(v)
    def p(moon):
        return (gv(moon.pos), gv(moon.vel))
    return p

def determine_proj_cycle(moons, v):
    pv = proj(v)
    seen = set()
    pm = lambda : tuple(pv(m) for m in moons)
    seen.add(pm())
    n = 1
    while True:
        simulate(moons, 1)
        np = pm()
        if np in seen: return n
        n += 1
        seen.add(np)

def better_determine_cycle(moons):
    return lcm(
        determine_proj_cycle(tuple(moons[:]), 'x'),
        determine_proj_cycle(tuple(moons[:]), 'y'),
        determine_proj_cycle(tuple(moons[:]), 'z')
    )

moons = (Moon(x=-7, y=17, z=-11), Moon(x=9, y=12, z=5), Moon(x=-9, y=0, z=-4), Moon(x=4, y=6, z=0))

simulate(moons, 1000)
print(energy(moons))
print(better_determine_cycle(moons))

