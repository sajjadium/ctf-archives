#pragma once

#include <sys/types.h>

struct process {
    struct process *nxt;
    pid_t pid;
    int in_syscall;
    int paus_requested;
};

extern struct process *live;

struct process *find(pid_t pid);
struct process *get_or_insert(pid_t pid);
int drop(pid_t pid);
