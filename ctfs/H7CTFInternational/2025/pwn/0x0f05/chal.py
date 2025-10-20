import sys
import mmap
import ctypes
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from prettytable import PrettyTable

def disassemble(shellcode):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    
    table = PrettyTable()
    table.field_names = ["Address", "Bytes", "Instruction"]
    table.align["Address"] = "l"
    table.align["Bytes"] = "l"
    table.align["Instruction"] = "l"
    
    instructions = []
    
    for insn in md.disasm(shellcode, 0x1000):
        address = f"0x{insn.address:08x}"
        bytes_hex = ' '.join(f"{b:02x}" for b in insn.bytes)  
        instruction = f"{insn.mnemonic} {insn.op_str}".strip()
        
        table.add_row([address, bytes_hex, instruction])
        instructions.append((insn.mnemonic, insn.op_str))
    
    print("\n[+] Disassembled Instructions:")
    print(table)
    
    return instructions

def check_syscall(instructions):
    for mnemonic, op_str in instructions:
        if mnemonic == "syscall" or (mnemonic == "int" and op_str == "0x80"):
            print("[!] Detected syscall or int 0x80. Execution blocked.")
            sys.exit(1)

def execute_shellcode(shellcode):
    size = len(shellcode)
    
    mem = mmap.mmap(-1, size, mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS, mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
    mem.write(shellcode)
    mem.seek(0)

    libc = ctypes.CDLL(None)
    libc.mprotect.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int)
    libc.mprotect(ctypes.c_void_p(ctypes.addressof(ctypes.c_char.from_buffer(mem))), size, mmap.PROT_READ | mmap.PROT_EXEC)

    shell_func = ctypes.CFUNCTYPE(None)(ctypes.addressof(ctypes.c_char.from_buffer(mem)))
    
    print("[+] Executing shellcode...")
    try:
        shell_func()
    except Exception as e:
        print(f"[!] Error executing shellcode: {e}")

if __name__ == "__main__":
    print("0xWelcome to ex-code-0x02!")
    print("[+] Enter shellcode (hex format, without 0x prefix):")
    hex_shellcode = input().strip()
    shellcode = bytes.fromhex(hex_shellcode)
    
    print("[+] Disassembling shellcode...")
    instructions = disassemble(shellcode)
    
    print("[+] Checking for restricted syscalls...")
    check_syscall(instructions)
    
    execute_shellcode(shellcode)
