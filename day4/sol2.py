from collections import Counter

dgt = list(map(int, '234444'))
end = list(map(int, '765869'))
i = len(dgt) - 1

def pair(dgt):
  c = Counter(dgt[i] for i in range(len(dgt) - 1) if dgt[i] == dgt[i + 1])
  for k, v in c.items():
    if v == 1: return True
  return False

cnt = 0
while dgt < end:
  if pair(dgt):
    print(dgt)
    cnt += 1
  while i >= 0 and dgt[i] == 9: i -= 1
  if i < 0: break
  n = dgt[i] + 1
  while i < len(dgt):
    dgt[i] = n
    i += 1
  i -= 1

print(cnt)