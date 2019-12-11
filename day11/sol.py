from collections import namedtuple, defaultdict
from operator import itemgetter

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
  '0': lambda p: p,
  '2': lambda p: c.RB + p
}

class Computer:

  def __init__(self, PRG, debug = False):
    self.DEBUG = debug
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
    if result.value is not None and instr.writes: self.write(result.value, addr_mode(self.MEM[self.pc + instr.num_param]))
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


BLACK, WHITE = 0, 1
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Robot:
    def __init__(self):
        self.panels = defaultdict(lambda : BLACK)
        self._painted = set()
        self.pos = (0, 0)
        self.dir = 0

    def painted(self):
        return self._painted

    def camera(self):
        return self.panels[self.pos]

    def paint(self, color, lr):
        self.panels[self.pos] = color
        self._painted.add(self.pos)
        self.dir = (self.dir + (1 if lr else -1)) % 4
        self.pos = self.pos[0] + DIRS[self.dir][0], self.pos[1] + DIRS[self.dir][1]


CODE = [3,8,1005,8,361,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,28,2,1104,18,10,1006,0,65,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,57,1,1101,5,10,2,108,15,10,2,102,12,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,91,2,1005,4,10,2,1107,10,10,1006,0,16,2,109,19,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,129,1,104,3,10,1,1008,9,10,1006,0,65,1,104,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,165,1,1106,11,10,1,1106,18,10,1,8,11,10,1,4,11,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1001,8,0,203,2,1003,11,10,1,1105,13,10,1,101,13,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,237,2,7,4,10,1006,0,73,1,1003,7,10,1006,0,44,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,273,2,108,14,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,299,1,1107,6,10,1006,0,85,1,1107,20,10,1,1008,18,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,337,2,107,18,10,101,1,9,9,1007,9,951,10,1005,10,15,99,109,683,104,0,104,1,21102,1,825594852248,1,21101,378,0,0,1105,1,482,21101,0,387240006552,1,21101,0,389,0,1106,0,482,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,29032025091,1,21101,436,0,0,1106,0,482,21101,29033143299,0,1,21102,1,447,0,1105,1,482,3,10,104,0,104,0,3,10,104,0,104,0,21101,988669698916,0,1,21101,0,470,0,1106,0,482,21101,0,709052072804,1,21102,1,481,0,1106,0,482,99,109,2,21202,-1,1,1,21101,0,40,2,21101,0,513,3,21101,503,0,0,1106,0,546,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,508,509,524,4,0,1001,508,1,508,108,4,508,10,1006,10,540,1101,0,0,508,109,-2,2105,1,0,0,109,4,1202,-1,1,545,1207,-3,0,10,1006,10,563,21102,0,1,-3,21202,-3,1,1,22101,0,-2,2,21102,1,1,3,21101,582,0,0,1105,1,587,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,610,2207,-4,-2,10,1006,10,610,21202,-4,1,-4,1106,0,678,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,629,1,0,1106,0,587,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,648,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,670,21202,-1,1,1,21101,670,0,0,105,1,545,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]

r = Robot()
c = Computer(CODE)
while True:
    c.run([r.camera()])
    if c.STATUS == STOP: break
    color, lr = c.OUTPUT
    r.paint(color, lr)

print(len(r.painted()))

r = Robot()
r.panels[r.pos] = WHITE
c = Computer(CODE)
while True:
    c.run([r.camera()])
    if c.STATUS == STOP: break
    color, lr = c.OUTPUT
    if color not in (0, 1) or lr not in (0, 1):
        print('DIOCANE', c.pc, c.STATUS, c.OUTPUT)
        break
    r.paint(color, lr)

rows = list(map(itemgetter(0), r.painted()))
cols = list(map(itemgetter(1), r.painted()))
rr = min(rows), max(rows)
cr = min(cols), max(cols)

PANELS = [[' ' for c in range(cr[1] - cr[0] + 5)] for r in range(rr[1] - rr[0] + 5)]

for (row, col), pix in r.panels.items():
    y = row - rr[0] + 2
    x = col - cr[0] + 2
    if x < 0 or y < 0:
        print('DIOCANE')
    PANELS[y][x] = '#' if pix == WHITE else '.'

print('\n'.join(''.join(row) for row in PANELS))

