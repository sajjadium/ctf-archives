from pwn import *
import sys
import os

f = open(sys.argv[1], 'rb')
size = int(f.readline())

ops = []

for i in range(size):
    ops.append(p32(int(f.readline()) & 0xffffffff))
f.close()

regs = {
    '0': {'size': 0, 'data': 0},
    '1': {'size': 0, 'data': 0},
    '2': {'size': 0, 'data': 0},
    '3': {'size': 0, 'data': 0},
}

for op in ops:
    inst = op[0]
    print(inst)

    if inst == 0:
        idx = op[1]
        data = u16(op[2:])
        assert 0 <= idx <= 3
        regs[str(idx)]['data'] = data
    elif inst == 1:
        dest  = op[1]
        pad  = op[2]
        src = op[3]
        assert 0 <= src <= 3
        assert pad == 0
        assert 0 <= dest <= 3
        regs[str(dest)]['data'] = regs[str(src)]['data']

    elif inst == 2:
        idx  = op[1]
        size = u16(op[2:])
        assert 0 <= idx <= 3

        regs[str(idx)]['size'] = size
        regs[str(idx)]['data'] = [0 for i in range(size)]

    elif inst == 3:
        reg  = op[1]
        idx  = op[2]
        data = op[3]
        assert 0 <= reg <= 3
        assert isinstance(regs[str(reg)]['data'], list)
        assert idx < regs[str(reg)]['size']

        regs[str(reg)]['data'][idx] = data

    elif inst == 4:
        dest  = op[1]
        reg  = op[2]
        idx = op[3]
        assert 0 <= dest <= 3
        assert 0 <= reg <= 3
        assert isinstance(regs[str(reg)]['data'], list)
        assert idx < regs[str(reg)]['size']    

        regs[str(dest)]['data'] = regs[str(reg)]['data'][idx]
    elif inst == 5:
        reg  = op[1]
        pad  = op[2]
        data = op[3]
        assert 0 <= reg <= 3
        assert pad == 0
        assert isinstance(regs[str(reg)]['data'], list)
        assert isinstance(regs['0']['data'], int)
        assert regs['0']['data'] < regs[str(reg)]['size']    

        regs[str(reg)]['data'][regs['0']['data']] = data
    elif inst == 6:
        dest  = op[1]
        pad = op[2]
        reg  = op[3]
        assert 0 <= dest <= 3
        assert 0 <= reg <= 3
        assert pad == 0
        assert isinstance(regs[str(reg)]['data'], list)
        assert isinstance(regs['0']['data'], int)
        assert regs['0']['data'] < regs[str(reg)]['size']    

        regs[str(dest)]['data'] = regs[str(reg)]['data'][regs['0']['data']]
    elif inst == 7:
        pass
    else:
        assert 0 <= inst <= 7