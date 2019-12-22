def inverse(a, n):
    t = 0
    newt = 1
    r = n
    newr = a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:return "a is not invertible"
    if t < 0: t = t + n
    return t

def pown(a, n, N):
    if n == 0: return 1
    p = pown(a, n // 2, N)
    if n % 2 == 0:
        return (p * p) % N
    else:
        return (a * p * p) % N

def sumn(a, n, N):
    if n == 0: return 1
    if n % 2 == 0:
        return (sumn(a, n - 1, N) + pown(a, n, N)) % N
    else:
        s = sumn(a, n // 2, N)
        return (s + s * pown(a, 1 + n // 2, N)) % N

class Stack:
    def __init__(self, N):
        self.N = N
        self.expr = (1, 0)

    def deal_into_new_stack(self, ignore = None):
        a, b = self.expr
        self.expr = -a % self.N, (self.N - 1 -b) % self.N

    def cut(self, n):
        a, b = self.expr
        self.expr = a % self.N, (b + n) % self.N

    def deal_with_increment(self, n):
        i = inverse(n, self.N)
        a, b = self.expr
        self.expr = (a * i) % self.N, (b * i) % self.N

    def apply(self, i):
        a, b = self.expr
        return (a * i + b) % self.N

    def shuffle(self, lines):
        for line in lines[::-1]:
            line = line.strip().split()
            try:
                cmd = '_'.join(line[:-1])
                val = int(line[-1])
            except ValueError:
                cmd = '_'.join(line)
                val = None
            getattr(self, cmd)(val)

with open('input.txt') as inf: ss = inf.read().splitlines()

c = Stack(10007)
c.shuffle(ss)
print('1)', list(map(c.apply, range(10007))).index(2019))

N = 119315717514047
T = 101741582076661
c = Stack(N)
c.shuffle(ss)

an = pown(c.expr[0], T, N)
sn = sumn(c.expr[0], T - 1, N)
k = 2020
r = (an * k + sn * c.expr[1]) % N

print('2)', r)
