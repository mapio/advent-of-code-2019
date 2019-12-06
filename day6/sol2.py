with open('input.txt') as inf:
    DATA = inf.read()

arcs = [l.split(')') for l in DATA.splitlines()]
reverse = dict(list(zip(*list(zip(*arcs))[::-1])))

def path(start):
    inpath = []
    curr = start
    while curr != 'COM':
        inpath.append(curr)
        curr = reverse[curr]

    return inpath[1:]

y = path('YOU')
s = path('SAN')

print(min([(y.index(ca) + s.index(ca), ca) for ca in set(s) & set(y)]))