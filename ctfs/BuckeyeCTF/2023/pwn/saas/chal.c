#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <ctype.h>

#include <capstone/capstone.h>


#define die(x) do { puts(x); exit(-1); } while (0)


#define SHELLCODE_ADDR 0xdead0000
#define SHELLCODE_MAX_SIZE 0x100
#define INPUT_SIZE SHELLCODE_MAX_SIZE*2

size_t parsehex(char *src, char *dest) {
    size_t len = strlen(src);
    if (src[len-1] == '\n') {
        src[len-1] = '\0';
        len--;
    }
    if (len % 2 == 1)
        die("*** Bad hex (odd length) ***");
    size_t final_len = len / 2;
    for (size_t i=0, j=0; j<final_len; i+=2, j++) {
        if (!(isxdigit(src[i]) && isxdigit(src[i+1])))
            die("*** Bad hex (invalid char) ***");
        dest[j] = (src[i] % 32 + 9) % 25 * 16 + (src[i+1] % 32 + 9) % 25;
    }

    return final_len;
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    
    printf("Welcome to shell code as a shell\n");
    printf("Enter your shellcode (in hex please) up to %d chars\n", INPUT_SIZE);
    char input[INPUT_SIZE+1];
    void *shellcode;
    shellcode = mmap(SHELLCODE_ADDR, SHELLCODE_MAX_SIZE, PROT_WRITE | PROT_READ, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    fgets(input, sizeof(input), stdin);
    
    size_t sz = parsehex(input, shellcode);
    if (sz < 4)
        die("Not enough bytes for an instruction!");

    csh handle;
    cs_insn *insn;

    if (cs_open(CS_ARCH_ARM, CS_MODE_ARM, &handle) != CS_ERR_OK)
        exit(-1);
    if (cs_option(handle, CS_OPT_DETAIL, CS_OPT_ON) != CS_ERR_OK)
        exit(-1);

    size_t count = cs_disasm(handle, shellcode, sz, SHELLCODE_ADDR, 0, &insn);
    if (count < 0) {
        cs_close(&handle);
        die("*** Failed to disassemble shellcode! ***");
    }

    printf("*** Read %d instructions ***\n", count);

    uint64_t end_pos = SHELLCODE_ADDR;
    for (size_t i = 0; i < count; ++i) {
        printf("0x%" PRIx64 ":\t%s\t\t%s\n", insn[i].address, insn[i].mnemonic,
            insn[i].op_str);

        // Check for syscalls
        cs_detail *detail = insn[i].detail;
        if (detail->groups_count > 0) {
        for (int n = 0; n < detail->groups_count; n++)
            if (detail->groups[n] == ARM_GRP_INT) {
                die("*** No syscalls for you! ***");
            }
        }
        end_pos += insn[i].size;
    }
    cs_free(insn, count);
    cs_close(&handle);

    if (count != sz / 4) {
        die("*** Incorect number of disassembled instructions. Make sure instructions are correct. ***");
    }
    
    // Setup environment and run
    puts("*** Shellcode looks good, let's roll! ***");

    mprotect(shellcode, SHELLCODE_ADDR, PROT_READ | PROT_EXEC);

    // Clear registers
    asm("mov r0, #0\n"
        "mov r1, #0\n"
        "mov r2, #0\n"
        "mov r3, #0\n"
        "mov r4, #0\n"
        "mov r5, #0\n"
        "mov r6, #0\n"
        "mov r7, #0\n"
        "mov r8, #0\n"
        "mov r9, #0\n"
        "mov r10, #0\n");
    void (*code)() = shellcode;
    code();
}
