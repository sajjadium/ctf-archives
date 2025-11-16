#!/usr/local/bin/python

# pip install capstone==5.0.6 pyelftools==0.32

from capstone import *
from capstone.x86 import *
from elftools.elf.elffile import ELFFile
import fcntl, io, os, sys, tempfile

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

checked = set()
def check(offset: int):
    if offset in checked:
        return
    checked.add(offset)

    pprev = None
    prev = None
    for inst in md.disasm(code[offset:], seg.header.p_vaddr + offset):
        # print(inst)
        assert inst.id != X86_INS_INT, "Interrupt instruction is not allowed"
        assert inst.id != X86_INS_SYSENTER, "Sysenter instruction not allowed. Use syscall."

        if inst.id == X86_INS_SYSCALL:
            assert prev is not None, "Must have instruction immediately before syscall"
            assert prev.id == X86_INS_MOV, "Instruction before syscall must be mov"
            _, wr = prev.regs_access()
            assert wr == [X86_REG_EAX], "Instruction before syscall must set eax"
            assert prev.op_count(X86_OP_IMM) == 1, "Instruction before must set eax to immediate"
            syscall_nr = prev.op_find(X86_OP_IMM, 1).value.imm
            assert syscall_nr in [0, 1, 9, 11, 0x3c], "Only read, write, mmap, exit syscalls are allowed"
            if syscall_nr == 9: # mmap
                assert pprev is not None, "Two instructions must precede mmap syscall"
                assert pprev.id == X86_INS_MOV, "Two mov instructions must precede mmap syscall"

                _, wr = pprev.regs_access()
                assert wr == [X86_REG_EDX], "Instruction before instruction before syscall must set edx"
                assert pprev.op_count(X86_OP_IMM) == 1, "Instruction before must set eax to immediate"
                prot = pprev.op_find(X86_OP_IMM, 1).value.imm
                assert prot & ~0b11 == 0, "mmap may only be called with PROT_READ and PROT_WRITE"

        if inst.group(X86_GRP_JUMP) or inst.group(X86_GRP_CALL):
            for i in range(1, inst.op_count(X86_OP_IMM) + 1):
                op = inst.op_find(X86_OP_IMM, i)
                check(op.value.imm - seg.header.p_vaddr)
            assert inst.op_count(X86_OP_MEM) == 0, "Not allowed to jump to/call memory location"
            for i in range(1, inst.op_count(X86_OP_REG) + 1):
                reg = inst.op_find(X86_OP_REG, i).value.reg
                assert prev is not None, "Must have an instruction immediately before register jump/call"
                assert prev.id == X86_INS_MOV, "Instruction before register jump/call must be mov"
                _, [wr] = prev.regs_access()
                assert reg == wr, "mov before register jump/call must set the same register"
                assert prev.op_count(X86_OP_IMM) == 1, "mov before register jump/call must use immediate value"
                check(prev.op_find(X86_OP_IMM, 1).value.imm - seg.header.p_vaddr)
            assert inst.op_count(X86_OP_INVALID) == 0, "Not allowed to jump to/call invalid"
        pprev = prev
        prev = inst

print("Give me a hex encoded 64 bit executable ELF file (end with an empty line):")
hexdata = ""
while (line := input()) != "":
    hexdata += line
data = bytes.fromhex(hexdata)
print(data)
elf = ELFFile(io.BytesIO(data))

assert elf.header.e_ident.EI_CLASS == "ELFCLASS64", "Only 64-bit elf files are allowed"
found_executable = False
for seg in elf.iter_segments():
    if seg.header.p_flags & 0b1 == 0: # not exec
        continue
    assert not found_executable, "Only one segment may be executable"
    found_executable = True
    assert seg.header.p_flags & 0b10 == 0, "Executable segment may not be writable"

    code = data[seg.header.p_offset:][:seg.header.p_filesz]

    # print(seg.header)
    # print(code[elf.header.e_entry - seg.header.p_vaddr:][:10].hex())
    if seg.header.p_vaddr <= elf.header.e_entry < seg.header.p_vaddr + seg.header.p_memsz:
        check(elf.header.e_entry - seg.header.p_vaddr)
    else:
        check(0)

print("This program seems safe, let's run it!", flush=True)

with tempfile.NamedTemporaryFile(delete_on_close=False) as f:
    f.write(data)
    os.fchmod(f.fileno(), 0o500)
    f.close()
    os.execve(f.name, ["your", "program"], {})
