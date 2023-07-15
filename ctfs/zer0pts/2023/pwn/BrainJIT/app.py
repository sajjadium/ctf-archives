#!/usr/bin/env python3
import ctypes
import mmap
import signal
import struct
import sys

class BrainJIT(object):
    MAX_SIZE = mmap.PAGESIZE * 8

    def __init__(self, insns: str):
        self._insns = insns
        self._mem = self._alloc(self.MAX_SIZE)
        self._code = self._alloc(self.MAX_SIZE)

    def _alloc(self, size: int):
        return mmap.mmap(
            -1, size, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC
        )

    @property
    def _code_len(self):
        return self._code.tell()

    def _emit(self, code):
        try:
            assert self._code.write(code) == len(code)
        except (ValueError, AssertionError):
            raise MemoryError("Code is too long")

    def compile(self):
        addr_mem = ctypes.addressof(ctypes.c_int.from_buffer(self._mem))
        p8  = lambda v: struct.pack('<B', v)
        p32 = lambda v: struct.pack('<i', v)
        p64 = lambda v: struct.pack('<Q', v)
        # push r8
        # push rbp
        # xor ebx, ebx
        # mov rbp, addr_mem
        emit_enter = b'\x41\x50\x55\x45\x31\xc0\x48\xbd' + p64(addr_mem)
        # pop rbp
        # pop r8
        # ret
        emit_leave = b'\x5d\x41\x58\xc3'

        self._emit(emit_enter)
        index = 0
        jumps = []
        while index < len(self._insns):
            insn = self._insns[index]
            length = 1
            if insn in ['<', '>', '+', '-']:
                while index + length < len(self._insns) \
                      and self._insns[index + length] == insn:
                    length += 1

            emit = b''
            if insn == '<':
                if length == 1:
                    # dec r8
                    emit += b'\x49\xff\xc8'
                else:
                    # sub r8, length
                    emit += b'\x49\x81\xe8' + p32(length)
                # cmp r8, self.MAX_SIZE
                # jb rip+1
                # int3
                emit += b'\x49\x81\xf8' + p32(self.MAX_SIZE) + b'\x72\x01\xcc'

            elif insn == '>':
                if length == 1:
                    # inc r8
                    emit += b'\x49\xff\xc0'
                else:
                    # add r8, length
                    emit += b'\x49\x81\xc0' + p32(length)
                # cmp r8, self.MAX_SIZE
                # jb rip+1
                # int3
                emit += b'\x49\x81\xf8' + p32(self.MAX_SIZE) + b'\x72\x01\xcc'

            elif insn == '+':
                if length == 1:
                    # inc byte ptr [rbp+r8]
                    emit += b'\x42\xfe\x44\x05\x00'
                else:
                    # add byte ptr [rbp+rbx], length
                    emit += b'\x42\x80\x44\x05\x00' + p8(length % 0x100)

            elif insn == '-':
                if length == 1:
                    # dec byte ptr [rbp+rbx]
                    emit += b'\x42\xfe\x4c\x05\x00'
                else:
                    # sub byte ptr [rbp+rbx], length
                    emit += b'\x42\x80\x6c\x05\x00' + p8(length % 0x100)

            elif insn == ',':
                # mov edx, 1
                # lea rsi, [rbp+rbx]
                # xor edi, edi
                # xor eax, eax ; SYS_read
                # syscall
                emit += b'\xba\x01\x00\x00\x00\x4a\x8d\x74\x05\x00'
                emit += b'\x31\xff\x31\xc0\x0f\x05'

            elif insn == '.':
                # mov edx, 1
                # lea rsi, [rbp+rbx]
                # mov edi, edx
                # mov eax, edx ; SYS_write
                # syscall
                emit += b'\xba\x01\x00\x00\x00\x4a\x8d\x74\x05\x00'
                emit += b'\x89\xd7\x89\xd0\x0f\x05'

            elif insn == '[':
                # mov al, byte ptr [rbp+rbx]
                # test al, al
                # jz ??? (address will be fixed later)
                emit += b'\x42\x8a\x44\x05\x00\x84\xc0'
                emit += b'\x0f\x84' + p32(-1)
                jumps.append(self._code_len + len(emit))

            elif insn == ']':
                if len(jumps) == 0:
                    raise SyntaxError(f"Unmatching loop ']' at position {index}")
                # mov al, byte ptr [rbp+rbx]
                # test al, al
                # jnz dest
                dest = jumps.pop()
                emit += b'\x42\x8a\x44\x05\x00\x84\xc0'
                emit += b'\x0f\x85' + p32(dest - self._code_len - len(emit) - 6)
                self._code[dest-4:dest] = p32(self._code_len + len(emit) - dest)

            else:
                raise SyntaxError(f"Unexpected instruction '{insn}' at position {index}")

            self._emit(emit)
            index += length

        self._emit(emit_leave)

    def run(self):
        ctypes.CFUNCTYPE(ctypes.c_int, *tuple())(
            ctypes.addressof(ctypes.c_int.from_buffer(self._code))
        )()

if __name__ == '__main__':
    print("Brainf*ck code: ", end="", flush=True)
    code = ''
    for _ in range(0x8000):
        c = sys.stdin.read(1)
        if c == '\n': break
        code += c
    else:
        raise MemoryError("Code must be less than 0x8000 bytes.")

    signal.alarm(15)
    jit = BrainJIT(code)
    jit.compile()
    jit.run()
