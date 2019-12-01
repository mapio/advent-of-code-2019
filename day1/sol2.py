import fileinput

def fuel(n):
  return n / 3 - 2

def total(n):
  sum = 0
  f = fuel(n)
  while f > 0:
    sum += f
    f = fuel(f)
  return sum

sum = 0
for line in fileinput.input():
  n = int(line)
  sum += total(n)

print(sum)