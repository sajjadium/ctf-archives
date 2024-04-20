#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <sys/ptrace.h>

#define DEBUG 0
#define MAIN_START 0x401988
#define MALLOC_ADDR 0x401a2f
#define AFTER_MALLOC_ADDR 0x401a34
#define REALLOC_ADDR 0x401b64
#define AFTER_REALLOC_ADDR 0x401b69
#define READ_ADDR 0x401c81

#define FATAL(...) \
    do { \
        if (DEBUG) {\
        fprintf(stderr, "challenge-err: " __VA_ARGS__); \
        fputc('\n', stderr); \
        }\
        exit(EXIT_FAILURE); \
    } while (0)

typedef struct safe_allocation {
    long long addr;
    int size;
} SafeAllocation;
SafeAllocation allocation_array [10];

int find_entry(long long addr) {
    for (int i = 0; i < 10; i++) {
        if (allocation_array[i].addr == addr) {
            if (DEBUG) {
                printf("Found entry: %d\n", i);
            }
            return i;
        }
    }
    return -1;
}

int main() {
    void *args = calloc(0x10, 1);

    pid_t mypid = getpid();
    pid_t pid = fork();
    switch (pid) {
        case -1:
            FATAL("%s", strerror(errno));
        case 0:
            if (ptrace (PTRACE_TRACEME, 0, 0, 0) < 0){
                FATAL("%s", strerror(errno));
            }
            execvp("./chall", args);
    }

    waitpid(pid, 0, 0);

    struct user_regs_struct regs;

    int sz;
    long long addr;
    int cur_alloc_index = 0;
    int realloc_index = 0;

    for (;;) {
        if (ptrace(PTRACE_SINGLESTEP, pid, 0, 0) == -1)
            FATAL("%s", strerror(errno));
        if (waitpid(pid, 0, 0) == -1)
            FATAL("%s", strerror(errno));

        if (ptrace(PTRACE_GETREGS, pid, 0, &regs) == -1)
            FATAL("%s", strerror(errno));

        long pc = (long)regs.rip;
        if (DEBUG) {
            if (pc == MAIN_START) {
                printf("Hit main\n");
            }
        }

        // Handle Option-1: Allocation
        {
            if (pc == MALLOC_ADDR) {
                long sz = (long)regs.rdi;
                allocation_array[cur_alloc_index].size = sz;

                if (DEBUG) {
                    printf("Before alloc\n");
                }
            }

            if (pc == AFTER_MALLOC_ADDR) {
                long long allocated_buffer = (long long)regs.rax;
                allocation_array[cur_alloc_index++].addr = allocated_buffer;

                if (DEBUG) {
                    printf("After alloc\n");
                }
            }
        }

        // Handle Option-2: Realloc
        {
            if (pc == REALLOC_ADDR) {
                sz = (long long) regs.rsi;

                //realloc_index = *((int*)int_sz_buf);
                if (DEBUG) {
                    printf("Before realloc\n");
                }
            }

            if (pc == AFTER_REALLOC_ADDR) {
                addr = (long long)regs.rax;
                realloc_index = find_entry(addr);
                allocation_array[realloc_index].addr = addr;
                allocation_array[realloc_index].size = sz;

                if (DEBUG) {
                    printf("After realloc\n");
                    printf("Realloc called on idx: %d with new-size: %d\n", realloc_index, sz);
                }
            }
        }

        // Handle Option-3 Edit
        {
            if (pc == READ_ADDR) {
                addr = (long long) regs.rsi;
                sz   = (int) regs.rdx;

                int idx = find_entry(addr);
                if (DEBUG) {
                    printf("read called, rlsz: %d, addr: %llx, sz: %d\n", 
                            allocation_array[idx].size, addr, sz);
                }

                if (sz > allocation_array[idx].size) {
                    printf("Didn't I tell you to only do valid sized allocations?\n");
                    exit(1);
                }
            }
        }
    }
}

