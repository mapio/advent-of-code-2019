from collections import Counter

X, Y = 25, 6
with open('input.txt') as inf: IMG = inf.read().strip()

split = 0
min_z = X * Y
while split < len(IMG):
  c = Counter(IMG[split:split + X * Y])
  split += X * Y
  if c['0'] < min_z:
    min_z = c['0']
    res = c['1'] * c['2']

print(res)