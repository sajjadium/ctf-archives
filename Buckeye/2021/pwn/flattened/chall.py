#!/usr/bin/env python3
import qiling
import pwn
import subprocess
import capstone.x86_const

pwn.context.arch = "amd64"
dump = []


def code_hook(ql, address, size):
    global dump
    buf = ql.mem.read(address, size)
    for i in md.disasm(buf, address):
        allowed_syscalls = {1, 0x3c}
        if (
            capstone.x86_const.X86_GRP_INT in i.groups
            and ql.reg.eax not in allowed_syscalls
        ):
            print(f"[-] syscall = {hex(ql.reg.eax)}")
            raise ValueError("HACKING DETECTED!")

        ignored_groups = {
            capstone.x86_const.X86_GRP_JUMP,
            capstone.x86_const.X86_GRP_CALL,
            capstone.x86_const.X86_GRP_RET,
            capstone.x86_const.X86_GRP_IRET,
            capstone.x86_const.X86_GRP_BRANCH_RELATIVE,
        }
        ignore = len(set(i.groups) & ignored_groups) > 0

        print(
            f"[{' ' if ignore else '+'}] {hex(i.address)}: {i.mnemonic} {i.op_str}"
        )
        if not ignore:
            dump.append(bytes(i.bytes))


inp = input("Enter code in hex:\n")
code = bytes.fromhex(inp)

ql = qiling.Qiling(
    code=code,
    rootfs="/",
    ostype="linux",
    archtype="x8664",
)

ql.hook_code(code_hook)
md = ql.create_disassembler()
md.detail = True
ql.run()

print("[+] Your program has been flattened! Executing ...")
new_code = b"".join(dump)
filename = pwn.make_elf(new_code, extract=False, vma=0x11FF000)
subprocess.run([filename])
