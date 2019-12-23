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
        i = pow(n, -1, self.N)
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

an = pow(c.expr[0], T, N)
sn = ((an - 1 ) * pow(c.expr[0] - 1, -1, N)) % N
k = 2020
r = (an * k + sn * c.expr[1]) % N

print('2)', r)
