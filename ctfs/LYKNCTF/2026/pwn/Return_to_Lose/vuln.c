#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

void win(void)
{
    char flag[128];
    int fd = open("flag.txt", O_RDONLY);
    if (fd < 0) {
        write(1, "flag.txt not found on this server.\n", 35);
        _exit(1);
    }
    ssize_t n = read(fd, flag, sizeof(flag));
    if (n > 0)
        write(1, flag, (size_t)n);
    _exit(0);
}

void vuln(void)
{
    char buf[64];
    write(1, "What's your name, traveler?\n> ", 30);
    read(0, buf, 256);
    write(1, "Safe travels!\n", 14);
}

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    vuln();
    return 0;
}
