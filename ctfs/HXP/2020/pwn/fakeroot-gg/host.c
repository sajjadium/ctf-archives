#define _GNU_SOURCE
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <linux/memfd.h>
#include <sys/syscall.h>
#include <sys/prctl.h>
#include <sys/fcntl.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#include <unistd.h>

#define ROOT "/jail"

int init_seccomp();
ssize_t from_hex(char *, char const *);

int main() {

    char *empty[1] = {NULL};
    setbuf(stdout, NULL);

    {
        fprintf(stderr, "pivoting to %s\n", ROOT);
        if (chdir(ROOT)) { perror("chdir"); exit(1); }
        if (chroot(ROOT)) { perror("chroot"); exit(1); }
    }

    int prog = syscall(SYS_memfd_create, "guest", MFD_CLOEXEC);
    if (prog < 0) { perror("memfd_create"); exit(1); }

    {
        char *hex = NULL;
        size_t sz = 0;

        for (size_t len = 0; len < (4ul << 20); ) {

            printf("program: ");

            ssize_t l = getline(&hex, &sz, stdin);
            if (l <= 0) { perror("getline"); exit(1); }
            hex[l-1] = 0; // remove \n

            if (!strcmp(hex, "end"))
                break;

            char *bytes = malloc((l + 5) / 2);
            if (!bytes) { perror("malloc"); exit(1); }

            ssize_t n = from_hex(bytes, hex);
            if (n < 0) { puts("bad hex"); exit(1); }

            for (size_t o = 0; o < (size_t) n; ) {
                ssize_t res = write(prog, bytes + o, n - o);
                if (res <= 0) { perror("write"); exit(1); }
                o += res;
            }
            len += n;

            free(bytes);
        }

        free(hex);
    }

    if (init_seccomp())
        exit(1);

    fprintf(stderr, "starting guest\n");

    syscall(SYS_execveat, prog, "", empty, empty, AT_EMPTY_PATH);

    perror("execveat");
    exit(1);
}

int init_seccomp()
{
    struct sock_filter filter[] = {
        BPF_STMT(BPF_LD + BPF_W + BPF_ABS, offsetof(struct seccomp_data, arch)),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL),

        BPF_STMT(BPF_LD + BPF_W + BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_open_by_handle_at, 4, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_process_vm_writev, 3, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_ptrace, 2, 0),
        BPF_JUMP(BPF_JMP + BPF_JGE + BPF_K, 400, 1, 0),
        BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL)
    };

    struct sock_fprog prog = {
        .len = sizeof(filter) / sizeof(*filter),
        .filter = filter,
    };

    return prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) || prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}

ssize_t from_hex(char *r, char const *s)
{
#define DECODE_HEX_CHAR_OR_RETURN_ERROR(T, C) \
    do { \
        if ((C) >= 'a' && (C) <= 'f') (T) = (unsigned) ((C) - 'a' + 10); \
        else if ((C) >= 'A' && (C) <= 'F') (T) = (unsigned) ((C) - 'A' + 10); \
        else if ((C) >= '0' && (C) <= '9') (T) = (unsigned) ((C) - '0'); \
        else return (ssize_t) -1; \
    } while (0)

    size_t l = strlen(s);
    unsigned char nibble;

    /* make sure strlen is even (although macro will return 0 on \0) */
    if (l & 1) return (ssize_t) -1;

    /* convert byte by byte */
    for (size_t i = 0; i < l; ) {
        r[i / 2] = 0;
        DECODE_HEX_CHAR_OR_RETURN_ERROR(nibble, s[i]);
        r[i++ / 2] |= nibble << 4;
        DECODE_HEX_CHAR_OR_RETURN_ERROR(nibble, s[i]);
        r[i++ / 2] |= nibble;
    }

    return (ssize_t) (l / 2);
#undef DECODE_HEX_CHAR_OR_RETURN_ERROR
}

