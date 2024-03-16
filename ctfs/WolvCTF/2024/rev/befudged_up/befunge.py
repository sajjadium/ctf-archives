
import sys


def read_in(filename):
    GRID = []

    r = 0
    c = 0

    row = []

    with open(filename, 'r') as f:
        contents = f.read()

    for x in contents:
        if x == '\n':
            r += 1
            c = 0
            GRID.append(row)
            row = []
        else:
            row.append(x)
            c += 1

    # right pad with spaces
    maxlen = max(len(r) for r in GRID)
    for i in range(len(GRID)):
        GRID[i] += [' '] * (maxlen - len(GRID[i]))
    return GRID


def befunge(GRID):
    PC = [0, 0]
    DIR = 0
    DIR_DELTAS = [0, 1, 0, -1, 0]
    STACK = []
    STRINGMODE = False

    MAXITER = 2**20

    for _ in range(MAXITER):
        try:
            ch = GRID[PC[0]][PC[1]]
            if STRINGMODE:
                if ch == '"':
                    STRINGMODE = False
                else:
                    STACK.append(ord(ch))
            else:
                match ch:
                    case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                        STACK.append(int(ch))
                    case '+':
                        a = STACK.pop()
                        b = STACK.pop()
                        STACK.append(a+b)
                    case '-':
                        a = STACK.pop()
                        b = STACK.pop()
                        STACK.append(b-a)
                    case '*':
                        a = STACK.pop()
                        b = STACK.pop()
                        STACK.append(a*b)
                    case '/':
                        a = STACK.pop()
                        b = STACK.pop()
                        STACK.append(b//a)
                    case '%':
                        a = STACK.pop()
                        b = STACK.pop()
                        STACK.append(b%a)
                    case '!':
                        a = STACK.pop()
                        if a == 0:
                            STACK.append(1)
                        else:
                            STACK.append(0)
                    case '`':
                        a = STACK.pop()
                        b = STACK.pop()
                        if b > a:
                            STACK.append(1)
                        else:
                            STACK.append(0)
                    case '>' | '^' | '<' | 'v':
                        DIR = '>v<^'.index(ch)
                    case '_':
                        a = STACK.pop()
                        if a == 0:
                            DIR = 0
                        else:
                            DIR = 2
                    case '|':
                        a = STACK.pop()
                        if a == 0:
                            DIR = 1
                        else:
                            DIR = 3
                    case '"':
                        STRINGMODE = True
                    case ':':
                        STACK.append(STACK[-1])
                    case '\\':
                        STACK[-2], STACK[-1] = STACK[-1], STACK[-2]
                    case '$':
                        STACK.pop()
                    case '.':
                        print(STACK.pop(), end=' ')
                    case ',':
                        print(chr(STACK.pop()), end='')
                    case '#':
                        PC[0] += DIR_DELTAS[DIR]
                        PC[1] += DIR_DELTAS[DIR + 1]
                    case 'p':
                        y = STACK.pop()
                        x = STACK.pop()
                        v = STACK.pop()
                        GRID[y][x] = chr(v)
                    case 'g':
                        y = STACK.pop()
                        x = STACK.pop()
                        STACK.append(ord(GRID[y][x]))
                    case '~':
                        x = sys.stdin.read(1)
                        STACK.append(ord(x))
                    case '@':
                        break
                    case ' ':
                        pass
                    case _:
                        print(f'Error: unknown character "{ch}"')
                        break
                # end match
            PC[0] += DIR_DELTAS[DIR]
            PC[1] += DIR_DELTAS[DIR + 1]
        except Exception as e:
            print('oh no', e, PC)
            break
