#define _GNU_SOURCE
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>


#define MAX_PIDS 0x100000
#define MAX_ELF_SIZE 0x100000

#define PATH_SIZE 0x100

#define JAILS_PATH_PREFIX "/tmp/jails"

#define INIT_PATH "/dummy_init"


#define CHECK(x) ({                                     \
    __typeof__(x) _x = (x);                             \
    if (_x == -1) {                                     \
        err(1, "error at %s (line %d)", #x, __LINE__);  \
    }                                                   \
    _x;                                                 \
})


struct sandbox {
    char* path;
};


static unsigned long g_pid_max;
static uid_t g_uid;
static int g_init_fd;
static struct sandbox* g_sandboxes;


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

static void readn(int fd, char* buf, size_t n) {
    size_t i = 0;
    while (i < n) {
        ssize_t x = read(fd, buf + i, n - i);
        if (x < 0) {
            if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) {
                continue;
            }
            err(1, "read");
        } else if (x == 0) {
            errx(1, "read waaat");
        }
        i += x;
    }
}

static void writen(int fd, const char* buf, size_t n) {
    size_t i = 0;
    while (i < n) {
        ssize_t x = write(fd, buf + i, n - i);
        if (x < 0) {
            if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) {
                continue;
            }
            err(1, "write");
        } else if (x == 0) {
            errx(1, "write waaat");
        }
        i += x;
    }
}

static void read_to_fd(int fd, size_t size) {
    char* buf = malloc(size);
    if (!buf) {
        err(1, "OOM");
    }
    readn(0, buf, size);
    writen(fd, buf, size);
    free(buf);
}

static char* read_file(const char* path) {
    int fd = CHECK(open(path, O_RDONLY));

#define BUF_CHUNK_SIZE 0x80
    size_t size = 0;
    char* buf = NULL;
    size_t i = 0;
    while (1) {
        if (size - i < BUF_CHUNK_SIZE) {
            size += BUF_CHUNK_SIZE;
            buf = realloc(buf, size + 1);
            if (!buf) {
                err(1, "OOM");
            }
        }

        ssize_t x = read(fd, buf + i, size - i);
        if (x < 0) {
            if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) {
                continue;
            }
            err(1, "read");
        } else if (x == 0) {
            break;
        }
        i += x;
    }
#undef BUF_CHUNK_SIZE

    buf[i] = '\0';

    CHECK(close(fd));

    return buf;
}

static char* gen_jail_path(pid_t p) {
    char* path = NULL;
    int x = asprintf(&path, JAILS_PATH_PREFIX "/%d", p);
    if (x < 0) {
        path = NULL;
    }
    return path;
}

static void rmrf(const char* path) {
    char* buf = NULL;
    CHECK(asprintf(&buf, "rm -rf %s", path));
    system(buf);
    free(buf);
}

static void block_sigchld(void) {
    sigset_t set;
    CHECK(sigemptyset(&set));
    CHECK(sigaddset(&set, SIGCHLD));
    CHECK(sigprocmask(SIG_BLOCK, &set, NULL));
}

static void unblock_sigchld(void) {
    sigset_t set;
    CHECK(sigemptyset(&set));
    CHECK(sigaddset(&set, SIGCHLD));
    CHECK(sigprocmask(SIG_UNBLOCK, &set, NULL));
}

static void sigchld_handler(int sig) {
    if (sig != SIGCHLD) {
        errx(1, "WTF");
    }

    while (1) {
        siginfo_t infop = { 0 };
        int x = waitid(P_ALL, 0, &infop, WEXITED | WNOHANG);
        if (x < 0) {
            if (errno == ECHILD) {
                break;
            }
            err(1, "waitid");
        }
        if (x == 0 && infop.si_pid == 0) {
            break;
        }

        rmrf(g_sandboxes[infop.si_pid].path);
        free(g_sandboxes[infop.si_pid].path);
    }
}

static __attribute__((constructor)) void do_inits(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    errno = 0;
    if (waitpid(-1, NULL, WNOHANG) != -1 || errno != ECHILD) {
        err(1, "huh");
    }

    g_uid = getuid();

    CHECK(setresuid(0, 0, 0));
    CHECK(setresgid(0, 0, 0));

    g_init_fd = CHECK(open(INIT_PATH, O_RDONLY | O_CLOEXEC));

    char* pid_max_str = read_file("/proc/sys/kernel/pid_max");
    errno = 0;
    g_pid_max = strtoul(pid_max_str, NULL, 10);
    if (errno) {
        err(1, "strtoul on pid_max");
    }
    free(pid_max_str);

    if (g_pid_max == 0 || g_pid_max > MAX_PIDS) {
        errx(1, "invalid pid_max");
    }

    g_sandboxes = calloc(g_pid_max, sizeof(*g_sandboxes));
    if (!g_sandboxes) {
        err(1, "OOM");
    }

    if (mkdir(JAILS_PATH_PREFIX, S_IRWXU) < 0) {
        if (errno != EEXIST) {
            err(1, "mkdir");
        }
        struct stat statbuf = { 0 };
        CHECK(lstat(JAILS_PATH_PREFIX, &statbuf));
        if (statbuf.st_uid != 0 || (statbuf.st_mode & S_IFMT) != S_IFDIR) {
            errx(1, "hacking detected");
        }
    }

    struct sigaction sa = {
        .sa_handler = sigchld_handler,
        .sa_flags = SA_NOCLDSTOP | SA_RESTART,
    };
    CHECK(sigaction(SIGCHLD, &sa, NULL));
}

static int get_elf(void) {
    size_t size = 0;
    printf("Binary size: ");
    scanf("%zu", &size);

    if (size == 0 || size > MAX_ELF_SIZE) {
        errx(1, "binary size too big");
    }

    int memfd = CHECK(memfd_create("exec", 0));

    printf("Binary data: ");
    read_to_fd(memfd, size);

    printf("\n");

    return memfd;
}

static int enter_chroot(const char* path) {
    if (chroot(path) < 0) {
        return -1;
    }
    if (chdir("/") < 0) {
        return -1;
    }
    return 0;
}

static void new_sandbox(void) {
    int elf_fd = get_elf();

    int sfd[2];
    CHECK(socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sfd));

    block_sigchld();

    pid_t p = CHECK(fork());
    if (p == 0) {
        if (close(sfd[0]) < 0) {
            _exit(1);
        }
        if (unshare(CLONE_FS | CLONE_NEWNS | CLONE_NEWNET | CLONE_NEWIPC | CLONE_NEWUTS | CLONE_SYSVSEM) < 0) {
            _exit(1);
        }

        char c = 0;
        if (read(sfd[1], &c, 1) != 1 || c != 1) {
            _exit(1);
        }

        char* path = gen_jail_path(getpid());
        if (enter_chroot(path) < 0) {
            _exit(1);
        }
        free(path);

        if (setresgid(g_uid, g_uid, g_uid) < 0) {
            _exit(1);
        }
        if (setresuid(g_uid, g_uid, g_uid) < 0) {
            _exit(1);
        }

        unblock_sigchld();

        char fd_buf[0x40] = { 0 };
        snprintf(fd_buf, sizeof(fd_buf), "%d", elf_fd);

        char* argv[] = { "init", fd_buf, NULL };
        (void)execveat(g_init_fd, "", argv, NULL, AT_EMPTY_PATH);
        write(sfd[1], &errno, 4);
        _exit(1);
    }

    CHECK(close(sfd[1]));
    CHECK(close(elf_fd));

    g_sandboxes[p].path = gen_jail_path(p);
    if (!g_sandboxes[p].path) {
        err(1, "OOM");
    }

    rmrf(g_sandboxes[p].path);
    CHECK(mkdir(g_sandboxes[p].path, S_IRWXU | S_IRWXG | S_IRWXO));

    writen(sfd[0], "\x01", 1);

    int c = 0;
    ssize_t x = CHECK(read(sfd[0], &c, sizeof(c)));
    if (x != 0) {
        errx(1, "spawning init failed: %d", c);
    }

    CHECK(close(sfd[0]));

    unblock_sigchld();
}

static void print_banner(void) {
    puts(
        "  _________                  .______.\n"
        " /   _____/____    ____    __| _/\\_ |__   _______  ___\n"
        " \\_____  \\\\__  \\  /    \\  / __ |  | __ \\ /  _ \\  \\/  /\n"
        " /        \\/ __ \\|   |  \\/ /_/ |  | \\_\\ (  <_> >    <\n"
        "/_______  (____  /___|  /\\____ |  |___  /\\____/__/\\_ \\\n"
        "        \\/     \\/     \\/      \\/      \\/            \\/\n"
    );
}

static void print_menu(void) {
    puts("1. Spawn new sandbox");
    puts("2. Exit");
}

int main(void) {
    print_banner();

    while (1) {
        print_menu();
        int option = 0;
        scanf("%d", &option);
        switch (option) {
            case 1:
                new_sandbox();
                break;
            case 2:
                exit(0);
            default:
                puts("Invalid option!");
                exit(0);
        }
    }

    return 0;
}
