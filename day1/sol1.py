import fileinput

def fuel(n):
  return n / 3 - 2

sum = 0
for line in fileinput.input():
  n = int(line)
  sum += fuel(n)

print(sum)