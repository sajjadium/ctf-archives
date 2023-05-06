#define _GNU_SOURCE
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/wait.h>
#include <unistd.h>

#include "shellcodeverifier.h"

#define MIN(a, b) ({        \
    __typeof__(a) _a = (a); \
    __typeof__(b) _b = (b); \
    _a < _b ? _a : _b;      \
})

#define CHECK(x) ({                         \
    __typeof__(x) _x = (x);                 \
    if (_x == -1) {                         \
        err(1, "failure at %d", __LINE__);  \
    }                                       \
    _x;                                     \
})

#define EXPECT(x, v) ({                                         \
    __typeof__(x) _x = (x);                                     \
    if (_x != (v)) {                                            \
        errx(1, "unexpected value returned at %d", __LINE__);   \
    }                                                           \
    _x;                                                         \
})

uid_t g_uid;
gid_t g_gid;

static void init_stuff(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    g_uid = getuid();
    g_gid = getgid();

    CHECK(mkdir(SANDBOX_DIR, 0777));

    CHECK(prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0));
}

static void writen(int fd, const char* buf, size_t size) {
    while (size) {
        ssize_t x = CHECK(write(fd, buf, size));
        if (x == 0) {
            errx(1, "fd full");
        }
        buf += x;
        size -= x;
    }
}

static void write_str_to_path(const char* path, const char* str) {
    int fd = CHECK(open(path, O_WRONLY));
    writen(fd, str, strlen(str));
    CHECK(close(fd));
}

static void read_to_fd(int fd, size_t size) {
    char buf[0x800];

    while (size) {
        ssize_t x = CHECK(read(0, buf, MIN(sizeof buf, size)));
        if (x == 0) {
            errx(1, "unexpected end of input");
        }
        writen(fd, buf, x);
        size -= x;
    }
}

static void wait_for_all_children(void) {
    while (1) {
        pid_t p = waitpid(-1, NULL, __WALL);
        if (p == -1) {
            if (errno != ECHILD) {
                err(1, "waitpid");
            }
            return;
        }
    }
}

static void get_file(const char* fname) {
    size_t size = 0;

    printf("File size: ");
    EXPECT(scanf("%zu", &size), 1);
    if (size > MAX_FILE_SIZE) {
        errx(1, "CANNOT HANDLE SUCH A BIG FILE");
    }

    int fd = CHECK(open(fname, O_WRONLY | O_CREAT | O_EXCL, 0777));
    printf("File contents: ");
    read_to_fd(fd, size);
    CHECK(close(fd));
}

static void setup_id_maps(pid_t p) {
    char buf[0x100];
    char path[0x100];

    if (snprintf(path, sizeof path, "/proc/%d/setgroups", p) < 0) {
        err(1, "cannot create path to setgroups");
    }
    write_str_to_path(path, "deny\n");

    if (snprintf(path, sizeof path, "/proc/%d/gid_map", p) < 0) {
        err(1, "cannot create path to gid_map");
    }
    if (snprintf(buf, sizeof buf, "%d %d 1\n", g_gid, g_gid) < 0) {
        err(1, "cannot create map string");
    }
    write_str_to_path(path, buf);

    if (snprintf(path, sizeof path, "/proc/%d/uid_map", p) < 0) {
        err(1, "cannot create path to uid_map");
    }
    if (snprintf(buf, sizeof buf, "%d %d 1\n", g_uid, g_uid) < 0) {
        err(1, "cannot create map string");
    }
    write_str_to_path(path, buf);
}

static void spawn_compiler(const char* compiler, const char* source_file, const char* output_file) {
    int pipes[2] = { -1, -1 };
    CHECK(socketpair(AF_UNIX, SOCK_STREAM, 0, pipes));

    unsigned long flags = CLONE_NEWUSER |
                          CLONE_NEWCGROUP |
                          CLONE_NEWIPC |
                          CLONE_NEWNET |
                          CLONE_NEWNS |
                          CLONE_NEWPID |
                          CLONE_NEWUTS;
    pid_t p = CHECK(syscall(SYS_clone, SIGCHLD | flags, NULL, NULL, NULL, 0l));
    if (p == 0) {
        CHECK(close(pipes[0]));
        char c = 0;
        EXPECT(CHECK(write(pipes[1], &c, 1)), 1);
        EXPECT(CHECK(read(pipes[1], &c, 1)), 1);
        CHECK(close(pipes[1]));

        CHECK(setsid());
        CHECK(chroot(SANDBOX_DIR));
        CHECK(chdir("/"));
        CHECK(setresgid(g_gid, g_gid, g_gid));
        CHECK(setresuid(g_uid, g_uid, g_uid));

        const char* const argv[] = { compiler, source_file, output_file, NULL };
        execve(compiler, (char* const*)argv, NULL);
        err(1, "execve failed");
    }

    CHECK(close(pipes[1]));

    char c = 0;
    EXPECT(CHECK(read(pipes[0], &c, 1)), 1);

    setup_id_maps(p);

    EXPECT(CHECK(write(pipes[0], &c, 1)), 1);

    CHECK(close(pipes[0]));
}

static void exec_output(const char* fname) {
    int fd = CHECK(open(fname, O_RDONLY | O_NOFOLLOW));

    struct stat statbuf = { 0 };
    CHECK(fstat(fd, &statbuf));
    if ((statbuf.st_mode & S_IFMT) != S_IFREG) {
        errx(1, "not a file");
    }

    size_t size = statbuf.st_size;
    if (size > MAX_FILE_SIZE) {
        errx(1, "file too big");
    }

    void* ptr = mmap(NULL, size, PROT_READ | PROT_EXEC, MAP_PRIVATE, fd, 0);
    if (ptr == MAP_FAILED) {
        err(1, "mmap");
    }

    CHECK(close(fd));

    if (!verify_buffer(ptr, size)) {
        errx(1, "unsafe code");
    }

    unsigned long ret = call_shellcode(ptr);
    printf("Your code returned: %#lx\n", ret);
}

int main(void) {
    init_stuff();

    puts("Compiler:");
    get_file(SANDBOX_DIR "/" COMPILER_NAME);
    puts("Input prog:");
    get_file(SANDBOX_DIR "/" SOURCE_NAME);

    spawn_compiler(COMPILER_NAME, SOURCE_NAME, OUTPUT_NAME);

    /* Wait for the compiler to finish the work. */
    wait_for_all_children();

    /* Try the output file. */
    exec_output(SANDBOX_DIR "/" OUTPUT_NAME);

    return 0;
}
