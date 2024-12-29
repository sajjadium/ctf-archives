#include <sys/types.h>

#include <stddef.h>
#include <stdlib.h>

#include "process.h"

struct process *live = NULL;

struct process *find(pid_t pid) {
    struct process *ret;
    for (ret = live; ret && ret->pid != pid; ret = ret->nxt) {}
    return ret;
}

struct process *get_or_insert(pid_t pid) {
    struct process *ret = find(pid);
    if (ret == NULL) {
        ret = calloc(1, sizeof(*live));
        ret->pid = pid;
        ret->nxt = live;
        live = ret;
    }
    return ret;
}

int drop(pid_t pid) {
    struct process *unlinked = NULL;
    if (live->pid == pid) {
        unlinked = live;
        live = live->nxt;
    } else {
        struct process *pre;
        for (pre = live; pre->nxt && pre->nxt->pid != pid; pre = pre->nxt) {}
        if (!pre->nxt)
            return 1;
        unlinked = pre->nxt;
        pre->nxt = unlinked->nxt;
    }

    free(unlinked);
    return 0;
}

