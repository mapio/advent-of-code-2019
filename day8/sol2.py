from collections import Counter

X, Y = 25, 6
with open('input.txt') as inf: IMG = inf.read().strip()

def render(layer, cur):
  nxt = []
  for l, c in zip(layer, cur):
    nxt.append(c if c != '2' else l)
  return nxt

split = 0
RES = ['2'] * (X * Y)
while split < len(IMG):
  RES = render(IMG[split:split + X * Y], RES)
  split += X * Y

print(''.join(RES))
for n, p in enumerate(RES):
  if n % X == 0: print()
  print(' ' if p == '0' else '█', end = '')

