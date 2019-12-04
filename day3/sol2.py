def points(path):
  pos = (0, 0)
  res = set()
  p2s = dict()
  steps = 0
  for step in path.split(','):
    dr, am = step[0], int(step[1:])
    for d in range(am):
      steps += 1
      if dr == 'R':
        pos = pos[0], pos[1] + 1
      elif dr == 'L':
        pos = pos[0], pos[1] - 1
      elif dr == 'U':
        pos = pos[0] + 1, pos[1]
      elif dr == 'D':
        pos = pos[0] - 1, pos[1]
      res.add(pos)
      if not pos in p2s:
        p2s[pos] = steps
  return res, p2s

a, sa = points(input())
b, sb = points(input())
x = a & b
m = min(x, key = lambda p: sa[p] + sb[p])
print(sa[m] + sb[m])