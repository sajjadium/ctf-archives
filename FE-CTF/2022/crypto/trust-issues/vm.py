#!/usr/bin/env python3
import sys
import os
import time
import types

class VM(object):
    OP_VLQ  = 0x80
    OP_NEW  = 0x81

    OP_SHOW = 0x82
    OP_SAVE = 0x83
    OP_DIG  = 0x84
    OP_BURY = 0x85
    OP_ZAP  = 0x86

    OP_POP  = 0x87
    OP_PULL = 0x88
    OP_PEEK = 0x89
    OP_PUSH = 0x8a
    OP_DUP  = 0x8b
    OP_OVER = 0x8c
    OP_SWAP = 0x8d
    OP_SWIZ = 0x8e

    OP_IF   = 0x8f
    OP_JMP  = 0x90
    OP_JZ   = 0x91
    OP_JNZ  = 0x92
    OP_CALL = 0x93
    OP_RET  = 0x94

    OP_ADD  = 0x95
    OP_SUB  = 0x96
    OP_NEG  = 0x97
    OP_INC  = 0x98
    OP_DEC  = 0x99
    OP_MUL  = 0x9a
    OP_DIV  = 0x9b
    OP_MOD  = 0x9c
    OP_AND  = 0x9d
    OP_OR   = 0x9e
    OP_XOR  = 0x9f
    OP_NOT  = 0xa0
    OP_LSH  = 0xa1
    OP_RSH  = 0xa2
    OP_EQ   = 0xa3
    OP_NE   = 0xa4
    OP_LT   = 0xa5
    OP_LE   = 0xa6
    OP_GT   = 0xa7
    OP_GE   = 0xa8

    OP_SYS  = 0xa9
    OP_HLT  = 0xaa
    OP_BRK  = 0xab

    SYS_GETC  = 0
    SYS_PUTC  = 1
    SYS_OPEN  = 2
    SYS_CLOSE = 3
    SYS_READ  = 4
    SYS_WRITE = 5
    SYS_TIME  = 6
    SYS_LIST  = 7

    def __init__(self, code, singlestep=False):
        self.stack = []
        self.rstack = []
        self.pc = 0
        self.prog = []
        self.halted = False
        self.singlestep = singlestep

        self.gen_tables()
        self.decode(code)

    def decode(self, code):
        i = 0

        def next():
            nonlocal i
            if not code:
                raise ValueError
            b = code[i]
            i += 1
            return b

        def vlq():
            n = 0
            i = 0
            while True:
                b = next()
                n |= (b & 0x7f) << i * 7
                i += 1
                if not b & 0x80:
                    break
            n = (n >> 1) * (-1 if n & 1 else 1)
            return n

        while i < len(code):
            b = next()

            op = self.op_table.get(b)
            if op:
                self.prog.append(op)

            elif b == VM.OP_VLQ:
                self.prog.append(vlq())

            else:
                # XXX: ISA requires n < 0x80, we should probably check this
                self.prog.append(b)

    def ctx(self):
        stack = []
        max_stack = 16
        for e in self.stack[:max_stack]:
            x = f'{e:02x}'
            if 32 <= e <= 126:
                c = chr(e)
            elif e == 10:
                c = '\\n'
            else:
                c = None
            if c:
                x += f'(\x1b[32;1m{c}\x1b[m)'
            stack.append(x)
        print('%-3d[ %s%s' % (
            len(self.stack),
            ' '.join(stack),
            ' ...' if len(self.stack) > max_stack else ''),
              end=' ',
              file=sys.stderr,
        )

        op = self.prog[self.pc]
        print(f'0x{self.pc:04x})', file=sys.stderr)
        if isinstance(op, int):
            print(f'# {op:#x}', file=sys.stderr)
        else:
            print(op.__name__[3:], file=sys.stderr)

    def run(self):
        while not self.halted and self.pc < len(self.prog):
            if self.singlestep:
                self.ctx()
            op = self.prog[self.pc]

            self.pc += 1
            if isinstance(op, int):
                self.push(op)
            else:
                op()

    def gen_tables(self):
        optbl = dict()
        systbl = dict()
        for uname in dir(self):
            lname = uname.lower()
            if uname.isupper() and hasattr(self, lname):
                n = getattr(self, uname)
                if uname.startswith('OP_'):
                    optbl[n] = getattr(self, lname)
                elif uname.startswith('SYS_'):
                    systbl[n] = getattr(self, lname)
        self.op_table = optbl
        self.sys_table = systbl

    def push(self, *xs):
        self.stack[0:0] = xs

    def pop(self, i=0):
        return self.stack.pop(i)

    def show(self, n, i=0):
        return self.stack[i:i+n]

    def save(self, xs, i=0):
        self.stack[i:i] = xs

    def zap(self, n, i=0):
        xs = self.show(n, i)
        self.stack[i:i+n] = []
        return xs

    def op_new(self):
        self.stack += [0] * self.pop()

    def op_show(self):
        n = self.pop()
        i = self.pop()
        self.save(self.show(n, i))

    def op_save(self):
        n = self.pop()
        i = self.pop()
        self.save(self.show(n), n + i)

    def op_dig(self):
        n = self.pop()
        i = self.pop()
        self.save(self.zap(n, i))

    def op_bury(self):
        n = self.pop()
        i = self.pop()
        self.save(self.zap(n), i)

    def op_zap(self):
        n = self.pop()
        i = self.pop()
        self.zap(n, i)

    op_pop = pop
    op_pop.__name__ = 'op_pop'

    def op_pull(self):
        self.save(self.zap(1, self.pop()))

    def op_peek(self):
        self.save(self.show(1, self.pop()))

    def op_push(self):
        n = self.pop()
        self.save(self.zap(1), n)

    def op_dup(self):
        self.save(self.show(1, 0))

    def op_over(self):
        self.save(self.show(1, 1))

    def op_swap(self):
        self.push(self.pop(1))

    def op_swiz(self):
        self.push(self.pop(2))

    def op_if(self):
        f = self.pop()
        t = self.pop()
        c = self.pop()
        self.push(t if c else f)

    def op_jmp(self):
        self.pc = self.pop()

    def op_jz(self):
        x = self.pop()
        if self.pop() == 0:
            self.pc = x

    def op_jnz(self):
        x = self.pop()
        if self.pop() != 0:
            self.pc = x

    def op_call(self):
        self.rstack.append(self.pc)
        self.op_jmp()

    def op_ret(self):
        self.pc = self.rstack.pop()

    def op_add(self):
        self.push(self.pop() + self.pop())

    def op_sub(self):
        x = self.pop()
        self.push(self.pop() - x)

    def op_neg(self):
        self.push(-self.pop())

    def op_inc(self):
        self.push(self.pop() + 1)

    def op_dec(self):
        self.push(self.pop() - 1)

    def op_mul(self):
        self.push(self.pop() * self.pop())

    def op_div(self):
        x = self.pop()
        self.push(self.pop() // x)

    def op_mod(self):
        x = self.pop()
        self.push(self.pop() % x)

    def op_and(self):
        self.push(self.pop() & self.pop())

    def op_or(self):
        self.push(self.pop() | self.pop())

    def op_xor(self):
        self.push(self.pop() ^ self.pop())

    def op_not(self):
        self.push(~self.pop())

    def op_lsh(self):
        x = self.pop()
        self.push(self.pop() << x)

    def op_rsh(self):
        x = self.pop()
        self.push(self.pop() >> x)

    def op_eq(self):
        self.push(int(self.pop() == self.pop()))

    def op_ne(self):
        self.push(int(self.pop() != self.pop()))

    def op_lt(self):
        x = self.pop()
        self.push(int(self.pop() < x))

    def op_le(self):
        x = self.pop()
        self.push(int(self.pop() <= x))

    def op_gt(self):
        x = self.pop()
        self.push(int(self.pop() > x))

    def op_ge(self):
        x = self.pop()
        self.push(int(self.pop() >= x))

    def op_sys(self):
        self.sys_table[self.pop()]()

    def op_hlt(self):
        self.halted = True

    def op_brk(self):
        self.ctx()

    def sys_getc(self):
        self.push(*sys.stdin.buffer.read(1) or [0])

    def sys_putc(self):
        sys.stdout.write(chr(self.pop() & 0xff))
        sys.stdout.flush()

    def popstr(self):
        s = ''
        while True:
            b = self.pop()
            if not b:
                break
            s += chr(b)
        return s

    def pushstr(self, s):
        self.save(list(s))

    def sys_open(self):
        flag = self.pop()
        try:
            self.push(os.open(self.popstr(), flag, 0o644))
        except:
            self.push(-1)

    def sys_close(self):
        os.close(self.pop())

    def sys_read(self):
        n = self.pop()
        s = os.read(self.pop(), n)
        self.pushstr(s)
        self.push(len(s))

    def sys_list(self):
        try:
            ds = os.listdir(self.popstr())
        except:
            self.push(-1)
            return
        for d in sorted(ds, reverse=True):
            self.pushstr(d.encode())
            self.push(len(d))
        self.push(len(ds))

if __name__ == '__main__':
    import click
    import mac
    import signal
    import base64
    import pwd
    import grp
    signal.alarm(300)

    @click.command()
    @click.argument(
        'program', required=False, type=click.File('rb'))
    @click.option(
        '--singlestep', '-s', is_flag=True,
        help='Break after every step.')
    @click.option(
        '--key-file', metavar='FILE',
        help='MAC key used to verify signed programs.')
    @click.option(
        '--user', '-u', metavar='USER',
        help='Set user.')
    def main(program, singlestep, key_file, user):
        '''Stack machine emulator.'''
        if program:
            program = program.read()
        else:
            program = base64.b64decode(sys.stdin.buffer.readline())
        if program.startswith(b'-----BEGIN MAC-----'):
            if not key_file:
                print('Program is signed; a key is required', file=sys.stderr)
                exit(1)
            program = mac.verify(mac.import_key(key_file), program)
            if not program:
                print('MAC error', file=sys.stderr)
                exit(1)
        elif key_file:
            print('Program must be signed', file=sys.stderr)
            exit(1)
        if user:
            try:
                uid = pwd.getpwnam(user).pw_uid
                os.setgroups([])
                os.setgid(uid)
                os.setuid(uid)
            except OSError:
                print('Could not change user', file=sys.stderr)
                exit(1)
            except KeyError:
                print('No such user:', user, file=sys.stderr)
                exit(1)

        try:
            vm = VM(program, singlestep)
            vm.run()
        except:
            print('Magic smoke got out', file=sys.stderr)
            exit(1)

    main()
