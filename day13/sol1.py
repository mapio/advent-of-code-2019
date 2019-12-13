from intcomp import Computer

with open('program.intcode') as inf:
  PRG = list(map(int,inf.read().split(',')))

c = Computer(PRG)
c.run([])

print(len(list(filter(lambda _: _ == 2, c.OUTPUT[2::3]))))