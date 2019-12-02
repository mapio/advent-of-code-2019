def compute(PRG, noun, verb):
  MEM = list(PRG)
  MEM[1] = noun
  MEM[2] = verb
  pc = 0
  while MEM[pc] in (1, 2):
    op, addr1, addr2, addr3 = MEM[pc:pc + 4]
    op1, op2 = MEM[addr1], MEM[addr2]
    MEM[addr3] = (op1 + op2) if op == 1 else (op1 * op2)
    pc += 4
  return MEM[0]

PRG = input()
for noun in range(100):
  for verb in range(100):
    if compute(PRG, noun, verb) == 19690720:
      print(100 * noun + verb)
      break