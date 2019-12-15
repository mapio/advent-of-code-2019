from collections import namedtuple, defaultdict

Result = namedtuple('Result', 'value, next_pc')
Instruction = namedtuple('Instruction', 'name, opcode, num_param, writes, func')

DEBUG = False
RUN, PAUSE, STOP = 'RUN', 'PAUSE', 'STOP'

decoder = {i.opcode: i for i in [
  Instruction('ADD',  '01',  2, True,  lambda c, p: Result(p[0] + p[1], None)),
  Instruction('MUL',  '02',  2, True,  lambda c, p: Result(p[0] * p[1], None)),
  Instruction('IN',   '03',  0, True,  lambda c, p: Result(c.input(), None)),
  Instruction('OUT',  '04',  1, False, lambda c, p: Result(c.output(p[0]), None)),
  Instruction('JNZ',  '05',  2, False, lambda c, p: Result(None, p[1] if p[0] else None)),
  Instruction('JZ',   '06',  2, False, lambda c, p: Result(None, None if p[0] else p[1])),
  Instruction('LT',   '07',  2, True,  lambda c, p: Result(int(p[0] < p[1]), None)),
  Instruction('EQ',   '08',  2, True,  lambda c, p: Result(int(p[0] == p[1]), None)),
  Instruction('SRB',  '09',  1, False, lambda c, p: Result(c.setrb(p[0]), None)),
  Instruction('HALT', '99',  0, False, lambda c, p: None),
  Instruction('NOP',   None, 0, False, lambda c, p: None)
]}

read_modes = {
  '0': lambda c, p: c.MEM[p] if p < len(c.MEM) else 0,
  '1': lambda c, p: p,
  '2': lambda c, p: c.MEM[c.RB + p] if c.RB + p < len(c.MEM) else 0
}

write_modes = {
  '0': lambda c, p: p,
  '2': lambda c, p: c.RB + p
}

class Computer:

  def __init__(self, PRG, debug = False):
    self.DEBUG = debug
    if isinstance(PRG, str):
      with open(PRG) as inf:
        self.MEM = list(map(int, inf.read().split(',')))
    else:
      self.MEM = PRG[:]
    self.STATUS = -1
    self.pc = 0
    self.RB = 0

  def setrb(self, p):
    self.RB += p

  def decode(self, mem):
    mem = '000000' + str(mem)
    instr = decoder[mem[-2:]]
    self.pc += 1
    accessor = list(map(read_modes.__getitem__, mem[-3:-(3 + instr.num_param):-1]))
    return instr, accessor, write_modes[mem[-(3 + instr.num_param)]] if instr.writes else None

  def dis(self):
    dpc = self.pc
    mem = '000000' + str(self.MEM[dpc])
    instr = decoder[mem[-2:]]
    read_modes = mem[-3:-(3 + instr.num_param):-1]
    write_mode = mem[-(3 + instr.num_param)]
    dpc += 1
    r2s = {'0': '*', '1': '', '2': '!'}
    w2s = {'0': '', '2':'!'}
    params = ' '.join('{}{}'.format(r2s[m], p) for m, p in zip(read_modes, self.MEM[dpc:dpc + instr.num_param]))
    addr = '-> {}{}'.format(w2s[write_mode], self.MEM[dpc + instr.num_param]) if instr.writes else ''
    print('> DIS', '{:04} [{}] {} {} {}'.format(self.pc, self.RB, instr.name, params, addr))

  def step(self):
    if self.DEBUG: self.dis()
    instr, accessor, addr_mode = self.decode(self.MEM[self.pc])
    params = [a(self, m) for a, m in zip(accessor, self.MEM[self.pc:self.pc + instr.num_param])]
    result = instr.func(self, params)
    if result.value is not None and instr.writes: self.write(result.value, addr_mode(self, self.MEM[self.pc + instr.num_param]))
    self.pc = result.next_pc if result.next_pc is not None else self.pc + instr.num_param + instr.writes

  def write(self, value, address):
    if address < 0: raise IndexError()
    if address >= len(self.MEM): self.MEM = self.MEM + [0] * (1 + address - len(self.MEM))
    self.MEM[address] = value

  def output(self, p):
    self.OUTPUT.append(p)

  def input(self):
    if self.INPUT == None:
      self.STATUS = PAUSE
      self.pc -= 2
      return None
    ret = self.INPUT
    self.INPUT = next(self._INPUT)
    return ret

  def run(self, IN):
    if self.DEBUG: print('> RUN', self.STATUS, self.pc, IN)
    self._INPUT = iter(IN + [None])
    self.INPUT = next(self._INPUT)
    self.STATUS = RUN
    self.OUTPUT = []
    while self.STATUS == RUN and self.MEM[self.pc] != 99:
      self.step()
    if self.MEM[self.pc] == 99:
      self.STATUS = STOP
    if self.DEBUG: print('> OUTPUT', self.STATUS, self.pc, self.OUTPUT)