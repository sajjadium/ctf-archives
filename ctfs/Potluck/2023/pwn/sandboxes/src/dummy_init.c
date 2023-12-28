#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <sys/wait.h>
#include <unistd.h>

#if __GLIBC__ < 2 || (__GLIBC__ == 2 && __GLIBC_MINOR__ < 34)
static int execveat(int dirfd, const char* pathname, char* const argv[], char* const envp[],
                    int flags) {
    long x = syscall(SYS_execveat, dirfd, pathname, argv, envp, flags);
    if (x < 0) {
        errno = -x;
    } else {
        errno = EINVAL;
    }
    return -1;
}
#endif

int main(int argc, char* argv[]) {
    if (argc != 2) {
        return 1;
    }

    int fd = atoi(argv[1]);
    if (fd < 0) {
        return 1;
    }

    pid_t p = fork();
    if (p < 0) {
        return 1;
    } else if (p == 0) {
        if (fcntl(fd, F_SETFD, FD_CLOEXEC) < 0) {
            return 1;
        }

        char* argv[] = { "elf", NULL };
        (void)execveat(fd, "", argv, NULL, AT_EMPTY_PATH);
        return 1;
    }

    close(fd);

    while (1) {
        errno = 0;
        int x = wait(NULL);
        if (x == -1 && errno == ECHILD) {
            break;
        }
    }

    return 0;
}
