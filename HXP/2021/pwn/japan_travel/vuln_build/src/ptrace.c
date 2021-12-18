#define _GNU_SOURCE

#include <sys/prctl.h>
#include <sys/ptrace.h>
#include <linux/ptrace.h>
#include <sys/uio.h>
#include <sys/user.h>
#include <sys/wait.h>

#include <errno.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "ptrace.h"

#define PTRACE_OPTIONS PTRACE_O_EXITKILL | PTRACE_O_TRACECLONE | PTRACE_O_TRACEFORK | PTRACE_O_TRACESYSGOOD | PTRACE_O_TRACEVFORK | PTRACE_O_TRACEEXEC | PTRACE_O_TRACEEXIT | PTRACE_O_TRACEVFORKDONE
#define check(c,msg) {if ((c) == - 1) {perror(msg); exit(1);}} 

static volatile size_t go = 0;

/***
* Starts to trace after calling pre(pre_args) in the tracees context waits 
*/
pid_t start_trace(int (*pre)(void *), void *pre_args, int (*fun)(void *), void *args) {
    int status;

    if (fun == NULL) {
        errno = EINVAL;
        return -1;
    }

    struct {
        int pout, pin;
    } __attribute__((packed)) p;
    check(pipe((int *) &p), "pipe");

    int pid = fork();
    check(pid, "fork");
    if (pid != 0) {
        //parent
        close(p.pout);
        prctl(PR_SET_PTRACER, pid);
        pid = getpid();
        write(p.pin, &pid, sizeof(pid));
        close(p.pin);

        char buf[4] = {0};
        fputs("waiting for go", stderr);
        if (pre != NULL)
            if (!pre(pre_args))
                exit(1);
        do {} while(go == 0);
        exit(fun(args));
    }

    //child
    close(p.pin);
    fputs("waiting for parent", stderr);
    read(p.pout, &pid, sizeof(pid));
    close(p.pout);

    check(ptrace(PTRACE_SEIZE, pid, 0, PTRACE_OPTIONS), "seize");
    check(ptrace(PTRACE_INTERRUPT, pid, 0, 0), "interrupt");
    waitpid(pid, &status, 0);
    if (!WIFSTOPPED(status) || WSTOPSIG(status) != SIGTRAP || status >> 16 != PTRACE_EVENT_STOP) {
        fputs("unexpected stop state", stderr);
        kill(pid, SIGKILL);
        errno = EIO;
        return -1;
    }
    check(ptrace(PTRACE_POKEDATA, pid, &go, 1), "poke");
    return pid;
}

void pt_wait(pid_t pid, struct pt_stop *out, bool noblock) {
    int status;
    pid_t rpid;

    rpid = waitpid(pid ? pid : -1, &status, __WALL | (noblock ? WNOHANG : 0));

    if (rpid == 0) {
        out->type = ST_STILLALIVE;
        return;
    }

    out->pid = rpid;
    if (WIFSTOPPED(status)) {
        int stopsig = WSTOPSIG(status);
        if (stopsig == (0x80 | SIGTRAP)) {
            out->type = ST_SYSCALL;
            check(ptrace(PTRACE_GETREGS, rpid, NULL, &out->syscall_regs), "loading tracee registers");
        } else if (status >> 16) {
            out->type = ST_EVENT;
            out->event.signal = stopsig;
            out->event.event = status >> 16;
        } else {
            out->type = ST_STOPPED;
            out->stopped.signal = stopsig;
        }
    } else if (WIFSIGNALED(status)) {
        out->type = ST_SIGNALED;
        out->signaled.signal = WTERMSIG(status);
        out->signaled.dumped = WCOREDUMP(status);
    } else if (WIFEXITED(status)) {
        out->type = ST_EXITED;
        out->exited.exit_code = WEXITSTATUS(status);
    }
}

ssize_t readvm(pid_t pid, void *local, void *remote, size_t len) {
    struct iovec loc = {.iov_base = local, .iov_len = len};
    struct iovec rem = {.iov_base = remote, .iov_len = len};

    return process_vm_readv(pid, &loc, 1, &rem, 1, 0);
}

struct rb {
    ssize_t size;
    char *buf;
    struct rb *nxt;
};

ssize_t readstr(pid_t pid, char **local, void *remote) {
    struct rb list = {0, NULL, NULL};

    uintptr_t rcur = (uintptr_t) remote;
    struct rb *cur = &list;

    while (1) {
        uintptr_t nxt = ((rcur + 0x1000) & ~0xfffllu);
        ssize_t size = nxt - rcur;
        cur->buf = malloc(size);
        if (cur->buf == NULL) { perror("malloc"); exit(1); }

//        printf("reading %zd bytes from %llx into %p\n", size, rcur, cur->buf);

        struct iovec loc = {.iov_base = cur->buf, .iov_len = size};
        struct iovec rem = {.iov_base = (void*) rcur, .iov_len = size};

        cur->size = process_vm_readv(pid, &loc, 1, &rem, 1, 0);
        if (cur->size != size) {
            cur->size = 0;
//            printf("did not read the requested size! (%ld vs %ld)\n", cur->size, size);
            break;
        }
        char *nb = memchr(cur->buf, 0, cur->size);
        if (nb) {
            cur->size = nb - cur->buf;
//            printf("found 0 byte after %zd bytes\n", cur->size);
            break;
        }

        cur->nxt = calloc(1, sizeof(struct rb));
        if (cur->nxt == NULL) { perror("calloc"); exit(1); }
        cur = cur->nxt;
        rcur = nxt;
    }

    size_t ges_size = 0;
    for (cur = &list; cur; cur = cur->nxt) {
        ges_size += cur->size;
    }

    char *cw = malloc(ges_size + 1);
    cw[ges_size] = 0;

    if (cw == NULL) { perror("malloc"); exit(1); }
    *local = cw;
    for (cur = &list; cur; cur = cur->nxt) {
        memcpy(cw, cur->buf, cur->size);
        cw += cur->size;
    }
//    printf("%s\n", *local);

    free(list.buf);
    struct rb *tmp;
    for (cur = list.nxt; cur; cur = tmp) {
        tmp = cur->nxt;
        free(cur->buf);
        free(cur);
    }

    return ges_size;
}

ssize_t writevm(pid_t pid, void *local, void *remote, size_t len) {
    struct iovec loc = {.iov_base = local, .iov_len = len};
    struct iovec rem = {.iov_base = remote, .iov_len = len};

    return process_vm_readv(pid, &loc, 1, &rem, 1, 0);
}
