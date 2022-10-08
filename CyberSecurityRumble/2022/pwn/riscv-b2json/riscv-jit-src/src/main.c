#include "codebuf.h"
#include "vm.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void handle_ecall(void) {
    // Get `ecall` number and arguments
    vm_word_t num = vm_state.regs[17];
    vm_word_t arg1 = vm_state.regs[10];
    vm_word_t arg2 = vm_state.regs[11];

    if (vm_verbose)
        printf("ecall_%d(0x%x, 0x%x) = ", num, arg1, arg2);

    // Default return value for error case
    vm_word_t ret = (vm_word_t)-1;

    switch (num) {
        case 0:
            // `exit()`
            exit(EXIT_SUCCESS);
            break;

        case 1:
            // `read(buf, len)`
            if ((vm_word_t)-1 - arg1 >= arg2 && arg1 <= vm_state.mem_size
                    && arg1 + arg2 <= vm_state.mem_size) {
                // Perform read
                ret = (vm_word_t)read(0, vm_state.mem + arg1, arg2);
            }
            break;

        case 2:
            // `write(buf, len)`
            if ((vm_word_t)-1 - arg1 >= arg2 && arg1 <= vm_state.mem_size
                    && arg1 + arg2 <= vm_state.mem_size) {
                // Perform write
                ret = (vm_word_t)write(1, vm_state.mem + arg1, arg2);
            }
            break;

        case 3: {
            // `flag()`
            FILE *f = fopen("flag_b2json.txt", "r");
            if (!f)
                vm_error("Failed to open flag, contact admin");
            char buf[0x100];
            size_t r = fread(buf, 1, sizeof buf, f);
            if (!r)
                vm_error("Failed to read flag, contact admin");
            if (!fwrite(buf, 1, r, stdout))
                vm_error("Failed to print flag, contact admin");
            fclose(f);
            ret = 0;
            break;
        }
    }

    if (vm_verbose)
        printf("0x%x\n", ret);

    vm_state.regs[10] = ret;
}

int main(int argc, char **argv) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    // Parse command line arguments
    const char *path = NULL;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-v")) {
            vm_verbose = true;
        } else {
            path = argv[i];
            if (i != argc - 1)
                vm_error("Invalid trailing command line arguments");
            break;
        }
    }
    if (!path)
        vm_error("Missing program file");

    // Initialize components
    codebuf_init();
    vm_init();

    // Read in program from file
    FILE *f = fopen(path, "r");
    if (!f)
        vm_error("Failed to open program file");
    if (!fread(vm_state.mem, 1, VM_MEM_SIZE, f))
        vm_error("Failed to read program file");
    fclose(f);

    // Execute the VM
    for (;;) {
        vm_exit_t exit = vm_run();

        // Handle VM exits
        switch (exit.reason) {
            case VM_EXIT_JUMP:
                // Continue normally on jump
                break;
            case VM_EXIT_FAULT:
                // Error on fault
                vm_error("Memory access fault");
                break;
            case VM_EXIT_EBREAK:
                // Print VM state on `ebreak`
                vm_print();
                break;
            case VM_EXIT_ECALL:
                // Handle various `ecall`s
                handle_ecall();
                break;
            case VM_EXIT_FENCE_I:
                // The code buffer appears like an instruction cache to code inside the VM, so we
                // clear it on instruction fences
                codebuf_clear();
                break;
        }
    }
}
