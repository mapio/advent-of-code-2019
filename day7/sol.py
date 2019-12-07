from itertools import permutations
from collections import namedtuple

Result = namedtuple('Result', 'value, next_pc')
Instruction = namedtuple('Instruction', 'opcode, num_param, writes, func')

RUN, PAUSE, STOP = 'RUN', 'PAUSE', 'STOP'

decoder = {i.opcode: i for i in [
  Instruction('01', 2, True, lambda c, p: Result(p[0] + p[1], None)),
  Instruction('02', 2, True, lambda c, p: Result(p[0] * p[1], None)),
  Instruction('03', 0, True, lambda c, p: Result(c.input(), None)),
  Instruction('04', 1, False, lambda c, p: Result(c.OUTPUT.append(p[0]), None)),
  Instruction('05', 2, False, lambda c, p: Result(None, p[1] if p[0] else None)),
  Instruction('06', 2, False, lambda c, p: Result(None, None if p[0] else p[1])),
  Instruction('07', 2, True, lambda c, p: Result(int(p[0] < p[1]), None)),
  Instruction('08', 2, True, lambda c, p: Result(int(p[0] == p[1]), None))
]}

modes = {
  '0': lambda c, p: c.MEM[p],
  '1': lambda c, p: p
}

class Computer:

  def __init__(self, PRG):
    self.MEM = PRG[:]
    self.STATUS = -1
    self.pc = 0

  def decode(self, mem):
    mem = '000000' + str(mem)
    instr = decoder[mem[-2:]]
    self.pc += 1
    accessor = list(map(modes.__getitem__, mem[-3:-(3 + instr.num_param):-1]))
    return instr, accessor

  def step(self):
    instr, accessor = self.decode(self.MEM[self.pc])
    params = [a(self, m) for a, m in zip(accessor, self.MEM[self.pc:self.pc + instr.num_param])]
    address = self.MEM[self.pc + instr.num_param:self.pc + instr.num_param + instr.writes][0] if instr.writes else None
    result = instr.func(self, params)
    if instr.writes: self.MEM[address] = result.value
    self.pc = result.next_pc if result.next_pc else self.pc + instr.num_param + instr.writes

  def input(self):
    if self.INPUT == None:
      self.STATUS = PAUSE
      self.pc -= 2
      return None
    ret = self.INPUT
    self.INPUT = next(self._INPUT)
    return ret

  def run(self, IN):
    #print('RUN ', self.STATUS, self.pc, IN)
    self._INPUT = iter(IN + [None])
    self.INPUT = next(self._INPUT)
    self.STATUS = RUN
    self.OUTPUT = []
    while self.STATUS == RUN and self.MEM[self.pc] != 99:
      self.step()
    if self.MEM[self.pc] == 99:
      self.STATUS = STOP
    #print('OUTPUT', n, self.STATUS, self.pc, self.OUTPUT)

CODES0 = [
  [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
  [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
  [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
]

CODES1 = [
  [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],
  [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
]

CODE = [3,8,1001,8,10,8,105,1,0,0,21,30,51,72,81,94,175,256,337,418,99999,3,9,101,5,9,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,1001,9,2,9,1002,9,5,9,4,9,99,3,9,1002,9,4,9,101,4,9,9,102,5,9,9,101,3,9,9,4,9,99,3,9,1002,9,4,9,4,9,99,3,9,102,3,9,9,1001,9,4,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,99]

max_signal = -1
witness = None

for tps in permutations(range(5, 10)):
  signal = 0
  computers = [Computer(CODE) for _ in range(5)]
  while True:
    for n, tp in enumerate(tps):
      c = computers[n]
      if c.STATUS == STOP: break
      if c.STATUS == PAUSE:
        c.run([signal])
      else:
        c.run([tp, signal])
      signal = c.OUTPUT[0]
    if signal > max_signal:
      max_signal = signal
      witness = tps[:]
    if all(_.STATUS == STOP for _ in computers): break

print(max_signal, witness)