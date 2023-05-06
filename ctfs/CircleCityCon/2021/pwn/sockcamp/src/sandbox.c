// Literally copy-and-pasted from the seccomp manpage

#include <errno.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>
#include <unistd.h>

#define X32_SYSCALL_BIT 0x40000000
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

static int install_filter(int syscall_nr, int t_arch, int f_errno) {
    unsigned int upper_nr_limit = 0xffffffff;

    /* Assume that AUDIT_ARCH_X86_64 means the normal x86-64 ABI
       (in the x32 ABI, all system calls have bit 30 set in the
       'nr' field, meaning the numbers are >= X32_SYSCALL_BIT). */
    if (t_arch == AUDIT_ARCH_X86_64)
        upper_nr_limit = X32_SYSCALL_BIT - 1;

    struct sock_filter filter[] = {
        /* [0] Load architecture from 'seccomp_data' buffer into
           accumulator. */
        BPF_STMT(
            BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, arch))),

        /* [1] Jump forward 5 instructions if architecture does not
           match 't_arch'. */
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, t_arch, 0, 5),

        /* [2] Load system call number from 'seccomp_data' buffer into
           accumulator. */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, nr))),

        /* [3] Check ABI - only needed for x86-64 in deny-list use
           cases.  Use BPF_JGT instead of checking against the bit
           mask to avoid having to reload the syscall number. */
        BPF_JUMP(BPF_JMP | BPF_JGT | BPF_K, upper_nr_limit, 3, 0),

        /* [4] Jump forward 1 instruction if system call number
           does not match 'syscall_nr'. */
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, syscall_nr, 0, 1),

        /* [5] Matching architecture and system call: don't execute
           the system call, and return 'f_errno' in 'errno'. */
        BPF_STMT(
            BPF_RET | BPF_K, SECCOMP_RET_ERRNO | (f_errno & SECCOMP_RET_DATA)),

        /* [6] Destination of system call number mismatch: allow other
           system calls. */
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

        /* [7] Destination of architecture mismatch: kill process. */
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
    };

    struct sock_fprog prog = {
        .len = ARRAY_SIZE(filter),
        .filter = filter,
    };

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)) {
        perror("seccomp");
        return 1;
    }

    return 0;
}

int main(int argc, char** argv) {
    if (argc < 5) {
        fprintf(
            stderr,
            "Usage: "
            "%s <syscall_nr> <arch> <errno> <prog> [<args>]\n"
            "Hint for <arch>: AUDIT_ARCH_I386: 0x%X\n"
            "                 AUDIT_ARCH_X86_64: 0x%X\n"
            "\n",
            argv[0], AUDIT_ARCH_I386, AUDIT_ARCH_X86_64);
        exit(EXIT_FAILURE);
    }

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
        perror("prctl");
        exit(EXIT_FAILURE);
    }

    if (install_filter(
            strtol(argv[1], NULL, 0), strtol(argv[2], NULL, 0),
            strtol(argv[3], NULL, 0)))
        exit(EXIT_FAILURE);

    execv(argv[4], &argv[4]);
    perror("execv");
    exit(EXIT_FAILURE);
}
