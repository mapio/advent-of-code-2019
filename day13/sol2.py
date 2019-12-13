from intcomp import Computer

with open('program.intcode') as inf:
  PRG = list(map(int,inf.read().split(',')))
PRG[0] = 2

c = Computer(PRG)
c.run([])

max_x = -1
max_y = -1
out = c.OUTPUT
for x, y, t in zip(out[::3], out[1::3], out[2::3]):
    if x > max_x: max_x = x
    if y > max_y: max_y = y

n2t = {
    0: ' ',
    1: '|',
    2: '#',
    3: '-',
    4: '*'
}

board = [['#' for c in range(max_x + 1)] for r in range(max_y + 1)]

ball_x = None
paddle_x = None

print('\033[2J')
while any('#' in row for row in board):
    out = c.OUTPUT

    for x, y, t in zip(out[::3], out[1::3], out[2::3]):
        if x == -1 and y == 0:
            score = t
        else:
            board[y][x] = n2t[t]
            if n2t[t] == '*': ball_x = x
            elif n2t[t] == '-': paddle_x = x

    if paddle_x < ball_x:
        joystic =  1
    elif paddle_x == ball_x:
        joystic = 0
    else:
        joystic = -1

    print('\033[H')
    print(score)
    print('\n'.join(''.join(row) for row in board))

    c.run([joystic])