#define _GNU_SOURCE
#include <arpa/inet.h>
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/limits.h>
#include <netinet/in.h>
#include <pthread.h>
#include <sched.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdnoreturn.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <unistd.h>

static const char flag_file[] = "flag.txt";
static const char pass_file[] = "pass.txt";
static pthread_mutex_t g_daemon_mutex = PTHREAD_MUTEX_INITIALIZER;
static int g_daemon_fds[2] = { -1, -1 };
static uint16_t g_port = 1337;

static char g_username[0x100];
static char g_password[0x100];

static bool readn(int fd, char* buf, size_t size) {
    size_t i = 0;
    while (i < size) {
        ssize_t x = read(fd, buf + i, size - i);
        if (x < 0) {
            if (errno == EINTR || errno == EAGAIN) {
                sched_yield();
                continue;
            }
            return false;
        } else if (x == 0) {
            return false;
        }
        i += x;
    }
    return true;
}

static bool writen(int fd, const char* buf, size_t size) {
    size_t i = 0;
    while (i < size) {
        ssize_t x = write(fd, buf + i, size - i);
        if (x < 0) {
            if (errno == EINTR || errno == EAGAIN) {
                sched_yield();
                continue;
            }
            return false;
        } else if (x == 0) {
            return false;
        }
        i += x;
    }
    return true;
}

static char* read_str(int fd) {
    unsigned int len = 0;
    if (!readn(fd, (char*)&len, sizeof(len))) {
        return NULL;
    }
    char* buf = malloc((size_t)len + 1);
    if (!buf) {
        return NULL;
    }
    if (!readn(fd, buf, len)) {
        return NULL;
    }
    buf[len] = 0;
    return buf;
}

static bool send_str(int fd, const char* str) {
    unsigned int len = strlen(str);
    if (!writen(fd, (char*)&len, sizeof(len))) {
        return false;
    }
    return writen(fd, str, len);
}

static bool send_file(int conn_fd, const char* path) {
    bool ret = false;
    char* buf = NULL;
    int fd = open(path, O_RDONLY);
    if (fd < 0) {
        goto out;
    }

    struct stat statbuf = { 0 };
    if (fstat(fd, &statbuf) < 0) {
        goto out;
    }
    if ((statbuf.st_mode & S_IFMT) != S_IFREG) {
        goto out;
    }
    size_t size = statbuf.st_size & 0xffffffffu;

    buf = malloc(size);
    if (!buf) {
        goto out;
    }

    if (!readn(fd, buf, size)) {
        goto out;
    }

    if (!writen(conn_fd, (char*)&size, sizeof(unsigned int))) {
        goto out_err;
    }
    if (!writen(conn_fd, buf, (unsigned int)size)) {
        goto out_err;
    }
    ret = true;

out:
    if (!ret) {
        ret = send_str(conn_fd, "failed to read the file");
    }
out_err:
    free(buf);
    if (fd >= 0) {
        close(fd);
    }
    return ret;
}

static void set_user(const char* username, const char* password) {
    if (!password) {
        /* Disallow empty pass for security reasons */
        password = "default";
    }
    strcpy(g_username, username);
    strcpy(g_password, password);
}

static bool get_user(int fd) {
    char buf[sizeof(g_username) + 1/*':'*/ + sizeof(g_password)] = { 0 };
    while (1) {
        ssize_t x = read(fd, buf, sizeof(buf) - 1);
        if (x < 0) {
            if (errno == EINTR || errno == EAGAIN) {
                sched_yield();
                continue;
            }
            return false;
        } else if (x == 0) {
            return false;
        }
        if (buf[x - 1] == '\n') {
            buf[x - 1] = 0;
        }
        break;
    }
    char* username = buf;
    char* password = strchr(buf, ':');
    if (password) {
        *password++ = 0;
    }
    set_user(username, password);
    return true;
}

static bool check_user(const char* username, const char* password) {
    int fd = open(pass_file, O_RDONLY);
    if (fd < 0) {
        return false;
    }

    bool ret = false;
    bool end = false;
    while (!end) {
        char buf[0x300] = { 0 };
        size_t i = 0;
        while (1) {
            ssize_t x = read(fd, &buf[i], 1);
            if (x < 0) {
                goto out;
            } else if (x == 0 || buf[i] == '\n') {
                buf[i] = 0;
                end = x == 0;
                break;
            }
            i++;
            if (i >= sizeof(buf) - 1) {
                goto out;
            }
        }
        char* ptr = strchr(buf, ':');
        if (!ptr) {
            goto out;
        }
        *ptr = 0;
        if (!strcmp(buf, username) && !strcmp(ptr+1, password)) {
            ret = true;
            goto out;
        }
    }

out:
    close(fd);
    return ret;
}

static bool check_path(const char* path, const char* username) {
    if (!strcmp(username, "root")) {
        return true;
    }

    const char* fname = strrchr(path, '/');
    if (fname) {
        fname += 1;
    } else {
        fname = path;
    }
    return strcmp(fname, flag_file) && strcmp(fname, pass_file);
}

static noreturn void do_pass_daemon(void) {
    while (1) {
        char* path = read_str(g_daemon_fds[1]);
        if (!path) {
            errx(1, "error reading path");
        }
        char* username = read_str(g_daemon_fds[1]);
        if (!username) {
            errx(1, "error reading username");
        }
        char* password = read_str(g_daemon_fds[1]);
        if (!password) {
            errx(1, "error reading password");
        }

        if (!check_user(username, password)) {
            if (!send_str(g_daemon_fds[1], "no")) {
                errx(1, "error sending response");
            }
        } else if (!check_path(path, username)) {
            if (!send_str(g_daemon_fds[1], "no")) {
                errx(1, "error sending response");
            }
        } else {
            if (!send_str(g_daemon_fds[1], "yes")) {
                errx(1, "error sending response");
            }
        }

        free(path);
        free(username);
        free(password);
    }
}

static int g_flags;

static bool spawn_daemon(void) {
    int x = socketpair(AF_UNIX, SOCK_STREAM | g_flags, 0, g_daemon_fds);
    if (x < 0) {
        return false;
    }
    pid_t p = fork();
    if (p < 0) {
        return false;
    } else if (p == 0) {
        close(g_daemon_fds[0]);
        do_pass_daemon();
    }
    return true;
}

static bool user_has_perm(const char* path, const char* username, const char* password) {
    bool ret = false;

    if (pthread_mutex_lock(&g_daemon_mutex)) {
        return false;
    }
    if (g_daemon_fds[0] == -1) {
        if (!spawn_daemon()) {
            goto out;
        }
    }

    if (!send_str(g_daemon_fds[0], path)) {
        goto out;
    }
    if (!send_str(g_daemon_fds[0], username)) {
        goto out;
    }
    if (!send_str(g_daemon_fds[0], password)) {
        goto out;
    }

    char* resp = read_str(g_daemon_fds[0]);
    if (!resp) {
        goto out;
    }
    if (!strcmp(resp, "yes")) {
        ret = true;
    }
    free(resp);

out:
    if (pthread_mutex_unlock(&g_daemon_mutex)) {
        return false;
    }
    return ret;
}

static void* handle_connection(void* arg) {
    int client_fd = (long)arg;

    if (!get_user(client_fd)) {
        goto out;
    }

    if (!send_str(client_fd, "Welcome!")) {
        goto out;
    }

    while (1) {
        char c = 0;
        if (!readn(client_fd, &c, 1)) {
            goto out;
        }
        switch (c) {
            case '1':;
                char* path = read_str(client_fd);
                if (!path) {
                    goto out;
                }
                if (strlen(path) >= PATH_MAX) {
                    free(path);
                    if (!send_str(client_fd, "such long paths do no exist")) {
                        goto out;
                    }
                    break;
                }
                if (user_has_perm(path, g_username, g_password)) {
                    if (!send_file(client_fd, path)) {
                        free(path);
                        goto out;
                    }
                } else {
                    if (!send_str(client_fd, "permission denied")) {
                        free(path);
                        goto out;
                    }
                }
                free(path);
                break;
            case '2':
                if (!send_str(client_fd, "To upload files you need to buy an enterprise version")) {
                    goto out;
                }
                break;
            default:
                goto out;
        }
    }

out:
    close(client_fd);
    return NULL;
}

static void generate_pass_file(void) {
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0) {
        err(1, "open urandom");
    }
    char pass[32];
    if (!readn(fd, pass, sizeof(pass))) {
        err(1, "urandom read");
    }
    if (close(fd) < 0) {
        err(1, "close");
    }

    fd = open(pass_file, O_WRONLY | O_CREAT, 0777);
    if (fd < 0) {
        err(1, "open pass");
    }

    const char* str = "default:default\nroot:";
    if (!writen(fd, str, strlen(str))) {
        err(1, "pass_file write");
    }

    for (size_t i = 0; i < sizeof(pass); ++i) {
        if (dprintf(fd, "%02x", (unsigned char)pass[i]) != 2) {
            err(1, "dprintf");
        }
    }

    if (close(fd) < 0) {
        err(1, "close");
    }
}

int main(int argc, char* argv[]) {
    for (int i = 1; i < argc; ++i) {
        if (!strcmp(argv[i], "-n")) {
            g_flags |= SOCK_NONBLOCK;
        } else if (!strcmp(argv[i], "-g")) {
            generate_pass_file();
        } else if (!strcmp(argv[i], "-p")) {
            if (++i < argc) {
                g_port = atoi(argv[i]);
            }
        }
    }

    set_user("default", NULL);

    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) {
        err(1, "socket");
    }

    int optval = 1;
    if (setsockopt(s, SOL_SOCKET, SO_REUSEPORT, &optval, sizeof(optval)) < 0) {
        err(1, "setsockopt");
    }

    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(g_port),
        .sin_addr.s_addr = INADDR_ANY,
    };
    if (bind(s, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        err(1, "bind");
    }
    if (listen(s, 5) < 0) {
        err(1, "listen");
    }

    while (1) {
        int client_fd = accept4(s, NULL, NULL, g_flags);
        if (client_fd < 0) {
            err(1, "accept");
        }
        pthread_t th;
        if (pthread_create(&th, NULL, handle_connection, (void*)(long)client_fd)) {
            errx(1, "pthread_create");
        }
        if (pthread_detach(th)) {
            errx(1, "pthread_detach");
        }
    }

    return 0;
}
