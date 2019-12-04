def points(path):
  pos = (0, 0)
  res = set()
  for step in path.split(','):
    dr, am = step[0], int(step[1:])
    for d in range(am):
      if dr == 'R':
        pos = pos[0], pos[1] + 1
      elif dr == 'L':
        pos = pos[0], pos[1] - 1
      elif dr == 'U':
        pos = pos[0] + 1, pos[1]
      elif dr == 'D':
        pos = pos[0] - 1, pos[1]
      res.add(pos)
  return res

a = input()
b = input()
x = points(a) & points(b)
m = min(x, key = lambda p: abs(p[0]) + abs(p[1]))
print(abs(m[0]) + abs(m[1]))