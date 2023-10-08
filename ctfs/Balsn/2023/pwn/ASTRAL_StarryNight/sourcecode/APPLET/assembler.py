from pwn import *

def aasm(code):
    def check(condition):
        if not condition:
            print(f'invalid argument on line {lnum + 1} : {origLine}')
            exit()
    def getReg(rs):
        if rs == 'pc':
            return 4
        elif rs == 'lr':
            return 5
        elif rs == 'inplen':
            return 11
        elif rs == 'caller':
            return 12
        elif rs == 'flag':
            return 13
        elif rs == 'sp':
            return 14
        elif rs == 'bp':
            return 15
        check(rs[0] == 'r')
        try:
            reg = int(rs[1:])
        except:
            check(False)
        check(reg >= 0 and reg < 16)
        return reg
    def getNum(n, size, unsigned = False, dontCareSign = False):
        if n[0] == '-':
            sign = -1
            n = n[1:]
        else:
            sign = 1
        if len(n) > 2 and n[:2] == '0x':
            base = 16
        else:
            base = 10
        try:
            n = int(n, base)
        except:
            check(False)
        n *= sign
        if dontCareSign:
            Min = -(1 << size) // 2
            Max = (1 << size) - 1
        else:
            if unsigned is False:
                Min = -(1 << size) // 2
                Max = (1 << size) // 2 - 1
            else:
                Min = 0
                Max = (1 << size) - 1
        check(n >= Min and n <= Max)
        if n < 0:
            n += (1 << size)
        return n
    JMP = {
        'call': 0x40,
        'jmp' : 0x41,
        'jb'  : 0x42,
        'jae' : 0x43,
        'je'  : 0x44,
        'jne' : 0x45,
        'jbe' : 0x46,
        'ja'  : 0x47,
    }
    ALU = {
        'add' : 0x50,
        'sub' : 0x51,
        'mul' : 0x52,
        'div' : 0x53,
        'and' : 0x54,
        'or'  : 0x55,
        'xor' : 0x56,
        'shr' : 0x57,
        'shl' : 0x58,
        'mov' : 0x59,
        'cmp' : 0x5a,
    }
    JMPDST = {}
    RESOLVE = {}
    code = code.strip().split('\n')
    bcode = b''
    for lnum, line in enumerate(code):
        origLine = line
        comment = line.find('//')
        if comment != -1:
            line = line[:comment]
        line = line.strip()
        if line=='':
            continue
        #print(line)
        line = line.split()
        if line[0] == 'push':
            check(len(line) == 2 or len(line) == 3)
            if len(line) == 2:
                #shorthand to not specify push imm size
                n = getNum(line[1], 64, dontCareSign = True)
                if n == 0:
                    S = 1
                else:
                    S = (n.bit_length() + 7) // 8
                bcode += p8(0x08 | (S - 1)) + int.to_bytes(n, S, 'little')
            else:
                check(len(line[1]) > 2 and line[1][0] == '<' and line[1][-1] == '>')
                S = getNum(line[1][1:-1], 4, unsigned = True)
                check(1 <= S and S <= 8)
                if line[2][0].isdigit():
                    n = getNum(line[2], S * 8, dontCareSign = True)
                    bcode += p8(0x08 | (S - 1)) + int.to_bytes(n, S, 'little')
                else:
                    r0 = getReg(line[2])
                    bcode += p8(0x18 | (S - 1)) + p8(r0)
        elif line[0] == 'pop':
            check(len(line) == 3)
            check(len(line[1]) > 2 and line[1][0] == '<' and line[1][-1] == '>')
            S = getNum(line[1][1:-1], 4, unsigned = True)
            check(1 <= S and S <=8)
            r0 = getReg(line[2])
            bcode += p8(0x10 | (S - 1)) + p8(r0)
        elif line[0] == 'load':
            line = ' '.join(line[1:]).split(',')
            check(len(line) == 2)
            hasSize = line[0][0] == '<'
            if not hasSize:
                #shorthand to not specify load imm size
                r0 = getReg(line[0].strip())
                n = getNum(line[1].strip(), 64, dontCareSign = True)
                if n == 0:
                    S = 1
                else:
                    S = (n.bit_length() + 7) // 8
                bcode += p8(0x30 | (S - 1)) + p8(r0) + int.to_bytes(n, S, 'little')
            else:
                S, r0 = line[0].strip().split()
                check(len(S) > 2 and S[0] == '<' and S[-1] == '>')
                S = getNum(S[1:-1], 4, unsigned = True)
                check(1 <= S and S <= 8)
                r0 = getReg(r0)
                line[1] = line[1].strip()
                if line[1][0] != '[':
                    n = getNum(line[1], S * 8, dontCareSign = True)
                    bcode += p8(0x30 | (S - 1)) + p8(r0) + int.to_bytes(n, S, 'little')
                else:
                    check(line[1][0] == '[' and line[1][-1] == ']')
                    r1 = getReg(line[1][1:-1])
                    bcode += p8(0x20 | (S - 1)) + p8(r0 | (r1 << 4))
        elif line[0] == 'store':
            line = ' '.join(line[1:]).split(',')
            check(len(line) == 2)
            hasSize = line[0][0] == '<'
            if not hasSize:
                #shorthand to not specify store imm size
                line[0] = line[0].strip()
                check(line[0][0] == '[' and line[0][-1] == ']')
                r0 = getReg(line[0][1:-1])
                n = getNum(line[1].strip(), 64, dontCareSign = True)
                if n == 0:
                    S = 1
                else:
                    S = (n.bit_length() + 7) // 8
                bcode += p8(0x38 | (S - 1)) + p8(r0) + int.to_bytes(n, S, 'little')
            else:
                S = line[0].strip().split()[0]
                dst = line[0][len(S):].strip()
                check(len(S) > 2 and S[0] == '<' and S[-1] == '>')
                S = getNum(S[1:-1], 4, unsigned = True)
                check(1 <= S and S <= 8)
                dst = dst.strip()
                check(dst[0] == '[' and dst[-1] == ']')
                dst = dst[1:-1]
                line[1] = line[1].strip()
                if line[1][0] != 'r':
                    r0 = getReg(dst)
                    n = getNum(line[1], S * 8, dontCareSign = True)
                    bcode += p8(0x38 | (S - 1)) + p8(r0) + int.to_bytes(n, S, 'little')
                else:
                    r0 = getReg(dst)
                    r1 = getReg(line[1])
                    bcode += p8(0x28 | (S - 1)) + p8(r0 | (r1 << 4))
        elif line[0] in JMP:
            check(len(line) == 2)
            if line[1][0].isdigit() or line[1] not in ('r0','r1','r2','r3','r4','r5','r6','r7','r8','r9','r10','r11','r12','r13','r14','r15','pc','lr','inplen','caller','flag','sp','bp'):
                if line[1][0].isdigit():
                    #Theoretically, we shouldn't do this, jumping to static offset is error prone, but allow for flexibility
                    n = getNum(line[1], 16)
                    bcode += p8(JMP[line[0]]) + p16(n)
                else:
                    tag = line[1]
                    offset = len(bcode) + 3
                    if tag in JMPDST:
                        #This is a backward jump, so delta must be negative
                        delta = JMPDST[tag] - offset + (1 << 16)
                        bcode += p8(JMP[line[0]]) + p16(delta)
                    else:
                        RESOLVE[offset] = (tag, lnum, origLine)
                        bcode += p8(JMP[line[0]]) + p16(0)
            else:
                check(False)
            '''
            else:
                r0 = getReg(line[1])
                bcode += p8(JMP[line[0]] | 0x08) + p8(r0)
            '''
        elif line[0] in ALU:
            opc = line[0]
            line = ' '.join(line[1:]).strip().split(',')
            check(len(line) == 2)
            r0, r1 = getReg(line[0].strip()), getReg(line[1].strip())
            bcode += p8(ALU[opc]) + p8(r0 | (r1 << 4))
        elif line[0] == 'return':
            check(len(line) == 1)
            bcode += b'\xfd'
        elif line[0] == 'invoke':
            check(len(line) == 1)
            bcode += b'\xfe'
        elif line[0] == 'exit':
            check(len(line) == 1)
            bcode += b'\xff'
        else:
            check(len(line) == 1 and len(line[0]) > 1)
            check(line[0][-1] == ':')
            check(not line[0][0].isdigit())
            tag = line[0][:-1]
            check(tag not in JMPDST)
            JMPDST[tag] = len(bcode)
    for offset in RESOLVE:
        tag, lnum, origLine = RESOLVE[offset]
        if tag not in JMPDST:
            print(f'unknown tag on line {lnum} : {origLine}')
            exit()
        delta = JMPDST[tag] - offset
        bcode = bcode[:offset-2] + p16(delta) + bcode[offset:]
    return bcode
