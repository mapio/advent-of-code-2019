MEM = list(input())
MEM[1] = 12
MEM[2] = 2
print(len(MEM))
pc = 0
while MEM[pc] in (1, 2):
  op, addr1, addr2, addr3 = MEM[pc:pc + 4]
  op1, op2 = MEM[addr1], MEM[addr2]
  print(op, addr1, op1, addr2, op2, addr3)
  MEM[addr3] = (op1 + op2) if op == 1 else (op1 * op2)
  pc += 4
  print(MEM[pc])

print(MEM)