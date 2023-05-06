#define _GNU_SOURCE
#include <err.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define FLAG_PATH "flag.txt"
#define TIMES 0x14000000ul

static void alarm_handler(int _x) {
    (void)_x;
    puts("Time's up!");
    _exit(0);
}

static __attribute__((constructor)) void inits(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    struct sigaction sa = {
        .sa_handler = alarm_handler,
    };
    if (sigaction(SIGALRM, &sa, NULL) < 0) {
        err(1, "sigaction");
    }

    alarm(20);
}

static size_t read_line(char* buf, size_t size) {
    if (size == 0) {
        return 0;
    }

    size_t i = 0;
    while (i < size - 1) {
        char c;
        ssize_t x = read(0, &c, 1);
        if (x < 0) {
            if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) {
                continue;
            }
            err(1, "read");
        } else if (x == 0) {
            break;
        }

        if (c == '\n') {
            break;
        }

        buf[i++] = c;
    }

    buf[i] = '\0';

    return i;
}

static size_t read_file(int fd, char* buf, size_t size) {
    size_t i = 0;

    while (i < size) {
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

    return i;
}

static void read_rand_hexstr(char* buf, size_t size) {
    int fd = open("/dev/urandom", O_RDONLY);
    if (fd < 0) {
        err(1, "read random");
    }

    size_t i = 0;
    while (i < size) {
        char c;
        read_file(fd, &c, 1);
        char hex[3];
        if (snprintf(hex, sizeof(hex), "%02hhx", c) != 2) {
            err(1, "snprintf");
        }
        buf[i++] = hex[0];
        if (i < size) {
            buf[i++] = hex[1];
        }
    }

    if (close(fd) < 0) {
        err(1, "close random");
    }
}

static void print_flag(void) {
    int fd = open(FLAG_PATH, O_RDONLY);
    if (fd < 0) {
        err(1, "open flag");
    }

    char buf[0x100] = { 0 };
    read_file(fd, buf, sizeof(buf) - 1);

    if (close(fd) < 0) {
        err(1, "close flag");
    }

    printf("FLAG: %s\n", buf);
}

int main(void) {
    char buf[0x1000] = { 0 };

    puts("Welcome!");

    read_rand_hexstr(buf, 0x101);

    size_t i;
    for (i = 0; i < TIMES / 0x100; ++i) {
        strfry(buf);
    }

    puts("gib:");
    read_line(buf, sizeof(buf));
    strfry(buf);
    puts(buf);

    char fry_buf[0x100] = { 0 };
    read_rand_hexstr(fry_buf, 64);

    strcpy(buf, fry_buf);
    strfry(buf);
    puts(buf);

    read_line(buf, sizeof(buf));

    if (!strcmp(buf, fry_buf)) {
        print_flag();
    } else {
        puts("WRONG");
    }

    return 0;
}
