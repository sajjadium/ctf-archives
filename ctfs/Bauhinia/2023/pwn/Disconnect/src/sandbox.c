#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <sys/socket.h>
#include <linux/seccomp.h>
#include "seccomp-bpf.h"
#include <sys/ptrace.h>
#include <sys/user.h>

char *filename;

struct sock_filter filter[] = {
    VALIDATE_ARCHITECTURE,
    EXAMINE_SYSCALL,
    DISALLOW_SYSCALL(socket),
    DISALLOW_SYSCALL(ptrace),
    ALLOW_PROCESS
};

void activate_seccomp()
{
    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(struct sock_filter)),
        .filter = filter,
    };

    // Initialize seccomp filter
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) {
        perror("prctl");
        exit(EXIT_FAILURE);
    }

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog) < 0) {
        perror("prctl");
        exit(EXIT_FAILURE);
    }

}


int main(int argc, char **argv)
{
    pid_t pid;
    int status;
 
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }
   
    close(0);
    close(1);
    close(2);

    filename = argv[1];
    activate_seccomp();
    execve(filename, 0, 0);
}
