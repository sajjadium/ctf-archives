import sys

TAPE_SIZE = 500

def run(code):
    stack = []
    lmatch = dict()
    rmatch = dict()
    for i in range(len(code)):
        if code[i] == '[':
            stack.append(i)
        elif code[i] == ']':
            lmatch[i] = stack[-1]
            rmatch[stack[-1]] = i
            stack.pop()
    tape = [0] * TAPE_SIZE
    iptr = 0 # instruction
    mptr = 0 # memory
    while iptr < len(code):
        instr = code[iptr]
        if instr == '>':
            mptr += 1
        elif instr == '<':
            mptr -= 1
        elif instr == '+':
            tape[mptr] += 1
            tape[mptr] %= 256
        elif instr == '-':
            tape[mptr] -= 1
            tape[mptr] %= 256
        elif instr == '.':
            print(chr(tape[mptr]), end='', flush=True)
        elif instr == ',':
            tape[mptr] = ord(sys.stdin.read(1)) % 256
        elif instr == '[':
            if tape[mptr] == 0:
                iptr = rmatch[iptr]
        elif instr == ']':
            if tape[mptr] != 0:
                iptr = lmatch[iptr]
        iptr += 1

if __name__ == '__main__':
    run(open(sys.argv[1]).read())
