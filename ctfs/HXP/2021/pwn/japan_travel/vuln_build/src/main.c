#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <sched.h>
//#include <seccomp.h>
#include <signal.h>
#include <stdio.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

#include <sys/mman.h>
#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <linux/ptrace.h>
#include <sys/syscall.h>

#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>

#include "ptrace.h"
#include "process.h"

#ifndef SYS_memfd_create
#define SYS_memfd_create 319
#define MFD_CLOEXEC 1U
#define SYS_execveat 322
#endif
#define AT_EMPTY_PATH 0x1000

int is_path_ok(char *path) {
    if (path == NULL) {
        return 1;
    }
    if (path[0] != '/' || strstr(path, "..")) {
        return 0;
    }

    char *canon_path = canonicalize_file_name(path);
    if (!canon_path) {
        return 1;
    }
    fprintf(stderr, "canonicalized path: %s\n", canon_path);
    if (canon_path
        && strncmp(canon_path, "/usr/", 5)
        && strncmp(canon_path, "/bin/", 5)
        && strncmp(canon_path, "/lib/", 5)
        && strncmp(canon_path, "/etc/", 5)
        && strncmp(canon_path, "/lib64/", 7)) {
        free(canon_path);
        return 0;
    }
    free(canon_path);
    return 1;
}

void handle_syscall(struct pt_stop *stop) {
    char *path = NULL;
    switch(stop->syscall_regs.orig_rax) {
    case SYS_openat:
        readstr(stop->pid, &path, (void*) stop->syscall_regs.rsi);
        fprintf(stderr, "openat of file %s\n", path);
        if (!is_path_ok(path)) {
            puts("ごめんなさい、入るのは禁断です。");
            stop->syscall_regs.rax = -EACCES;
            stop->syscall_regs.orig_rax = -1;
        }
        free(path);
        ptrace(PTRACE_SETREGS, stop->pid, NULL, &stop->syscall_regs);
        ptrace(PTRACE_SYSCALL, stop->pid, NULL, NULL);
        break;
    case SYS_open:
        readstr(stop->pid, &path, (void*) stop->syscall_regs.rdi);
        fprintf(stderr, "open of file: %s\n", path);
        if (!is_path_ok(path)) {
            puts("ごめんなさい、入るのは禁断です。");
            stop->syscall_regs.rax = -EACCES;
            stop->syscall_regs.orig_rax = -1;
        }
        free(path);
        ptrace(PTRACE_SETREGS, stop->pid, NULL, &stop->syscall_regs);
        ptrace(PTRACE_SYSCALL, stop->pid, NULL, NULL);
        break;
    }
}

struct linux_dirent64 {
    ino64_t d_ino;
    off64_t d_off;
    unsigned short d_reclen;
    unsigned char d_type;
    char d_name[];
};

void handle_sysexit(struct pt_stop *stop) {
    if (stop->syscall_regs.orig_rax == SYS_getdents64 && stop->syscall_regs.rax > 0) {
        size_t bytes = stop->syscall_regs.rax;
        uint8_t *ents = calloc(1, bytes);
        if (!ents) return;
        ssize_t nlen = 0;
        readvm(stop->pid, ents, (void*) stop->syscall_regs.rsi, bytes);
        ssize_t off = 0;
        ssize_t censored = 0;
        while (off < bytes) {
            struct linux_dirent64 *de = (struct linux_dirent64*) &ents[off + censored];
            if (de->d_reclen < sizeof(struct linux_dirent64))
                break;
            off += de->d_reclen;
            if (!strstr(de->d_name, "staff")) {
                nlen += de->d_reclen;
                if (censored) {
                    memmove(&ents[off - censored], &ents[off], de->d_reclen);
                }
            } else {
                censored += de->d_reclen;
            }
        }
        for (ssize_t cp = nlen; cp < bytes; ++cp) {
            ents[cp] = 0;
        }
        writevm(stop->pid, ents, (void*) stop->syscall_regs.rsi, bytes);
        stop->syscall_regs.rax = nlen;
        ptrace(PTRACE_SETREGS, stop->pid, NULL, &stop->syscall_regs);
    }
}

void guardian(void) {
    struct pt_stop stop;
    while (live) {
        pt_wait(-1, &stop, false);
        struct process *proc = get_or_insert(stop.pid);

        uint64_t chld;
        switch (stop.type) {
        case ST_EXITED:
        case ST_SIGNALED:
            fprintf(stderr, "[%5u] perished\n", stop.pid);
            drop(stop.pid);
            break;
        case ST_SYSCALL:
            fprintf(stderr, "[%5u] [%16llx] %s syscall %lld\n", stop.pid, stop.syscall_regs.rip, (proc->in_syscall) ? "exited" : "entered", stop.syscall_regs.orig_rax);
            proc->in_syscall ^= 1;
            if (proc->in_syscall) {
                handle_syscall(&stop);
            } else {
                handle_sysexit(&stop);
            }
            ptrace(PTRACE_SYSCALL, stop.pid, NULL, NULL);
            if (!proc->in_syscall && proc->paus_requested)
                ptrace(PTRACE_INTERRUPT, stop.pid, 0, 0);
            break;
        case ST_EVENT:
            switch (stop.event.event) {
            case PTRACE_EVENT_FORK:
            case PTRACE_EVENT_CLONE:
            case PTRACE_EVENT_VFORK:
                ptrace(PTRACE_GETEVENTMSG, stop.pid, 0, &chld);
                get_or_insert(chld);
                fprintf(stderr, "[%5u] is proud parent of %5lu\n", stop.pid, chld);
                ptrace(PTRACE_SYSCALL, stop.pid, 0, 0);
                if (proc->paus_requested) {
                    puts("pausing\n");
                    ptrace(PTRACE_INTERRUPT, stop.pid, 0, 0);
                }
                break;
            case PTRACE_EVENT_STOP:
                if (proc->paus_requested == 1) {
                    ptrace(PTRACE_LISTEN, stop.pid, 0, 0);
                } else {
                    fprintf(stderr, "[%5u] stray stop, continuing\n", stop.pid);
                    ptrace(PTRACE_SYSCALL, stop.pid, 0, 0);
                }
                break;
            case PTRACE_EVENT_EXIT:
                fprintf(stderr, "[%5u] is exiting\n", stop.pid);
                ptrace(PTRACE_CONT, stop.pid, 0, 0);
                break;
            case PTRACE_EVENT_EXEC:
                fprintf(stderr, "[%5u] is execing\n", stop.pid);
                ptrace(PTRACE_SYSCALL, stop.pid, 0, 0);
                break;
            default:
                fprintf(stderr, "[%5u] unexpected event\n", stop.pid);
                break;
            }
            break;
        case ST_STOPPED:
            fprintf(stderr, "[%5u] received signal %u\n", stop.pid, stop.stopped.signal);
            if (stop.stopped.signal == SIGSTOP) {
                if (!proc->paus_requested) {
                    proc->paus_requested = 1;
                    ptrace(PTRACE_SYSCALL, stop.pid, 0, 0);
                    ptrace(PTRACE_INTERRUPT, stop.pid, 0, 0);
                }
            } else {
                ptrace(PTRACE_SYSCALL, stop.pid, 0, stop.stopped.signal);
                if (proc->paus_requested)
                    ptrace(PTRACE_INTERRUPT, stop.pid, 0, 0);
            }
            break;
        case ST_STILLALIVE:
            // nice for you
            break;
        }
    }
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

int init_seccomp()
{
    struct sock_filter filter[] = {
        BPF_STMT(BPF_LD + BPF_W + BPF_ABS, offsetof(struct seccomp_data, arch)),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL),

        BPF_STMT(BPF_LD + BPF_W + BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_clone, 31, 0), // blacklist some
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_linkat, 30, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_link, 29, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_symlink, 28, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_symlinkat, 27, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_fork, 26, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_vfork, 25, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_socket, 24, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_socketpair, 23, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_semget, 22, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_shmat, 21, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_msgget, 20, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_chdir, 19, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_fchdir, 18, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_chmod, 17, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_fchmod, 16, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_chown, 15, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_fchown, 14, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_lchown, 13, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_ptrace, 12, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_sched_setparam, 11, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_sched_setscheduler, 10, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_gettid, 8, 0), // whitelist some
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_set_tid_address, 7, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_time, 6, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_getdents64, 5, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_exit_group, 4, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_openat, 3, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_newfstatat, 2, 0),
        BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, SYS_execveat, 1, 0),
        BPF_JUMP(BPF_JMP + BPF_JGE + BPF_K, SYS_adjtimex, 1, 0),

        BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ERRNO | (38 & SECCOMP_RET_DATA))
    };

    struct sock_fprog prog = {
        .len = sizeof(filter) / sizeof(*filter),
        .filter = filter,
    };

    return prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) || prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}

int tracee(void *arg) {
    (void) arg;
    char *args[2] = {"行け", NULL};

    int prog = syscall(SYS_memfd_create, "guest", MFD_CLOEXEC);
    if (prog < 0) { perror("memfd_create"); exit(1); }

    {
        char *hex = NULL;
        size_t sz = 0;

        printf("命令: ");
        ssize_t l = getline(&hex, &sz, stdin);
        if (l > (4l << 20) || l < 1) {
            free(hex);
            return 1;
        }
        hex[l - 1] = 0;

        char *bytes = malloc((l + 5) / 2);
        if (!bytes) { perror("malloc"); exit(1); }

        ssize_t n = from_hex(bytes, hex);
        if (n < 0) { puts("bad hex"); exit(1); }

        for (size_t o = 0; o < n; ++o) {
            ssize_t res = write(prog, bytes + o, n - o);
            if (res <= 0) { perror("write"); exit(1); }
            o += res;
        }

        free(bytes);
        free(hex);
    }

    if (init_seccomp())
        exit(1);

    fprintf(stderr, "starting guest\n");

    syscall(SYS_execveat, prog, "", args, args + 1, AT_EMPTY_PATH);

    perror("execveat");
    exit(1);
}

int main(int argc, char **argv) {
    (void) argc;
    (void) argv;
    setbuf(stdout, NULL);
    puts("店員:いらっしゃいませぇ");
    puts("君: Hello");
    puts("店員:こんばんは私はクレアク、自動店員です。どうすれば支援できますか。");
    puts("君: I locked myself out of my room and forgot passport and flag there, but i want to meet some ctf friends for 焼肉 in 新宿, could you please let me in.");
    puts("店員：ごめんなさい、最後質問がわかりませんから、繰り返してくださいおねがいします。");
    puts("君: Aaaa.. あのぉぉ。。。部屋の鍵が忘れました、部屋を開いてください。");
    puts("店員: はい、識別くださいおねがいします。");
    puts("君: I forgot it in the room, man this situation is so dumb, a human clerk would actually be helpful now... can you maybe at least speak English?");
    puts("店員: 外国語サポートはロードします。。。100パーセント。外国語モードは従事しています。");
    puts("店員:　ヘロ、アイ　アム　クレアク。プリース　シャオ　ハーヴ　アイ　カン　アシスト。アイ　ウイル　レッペート　アクション　ポオシブルの場合");
    pid_t init = start_trace(NULL, NULL, tracee, NULL);
    get_or_insert(init);
    ptrace(PTRACE_SYSCALL, init, 0, 0);
    guardian();
    return EXIT_SUCCESS;
}
