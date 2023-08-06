#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>

void win() {
    char buf[0x100];
    int fd_s = open("secret.txt", O_RDONLY);
    int fd_w = open("win.txt", O_WRONLY | O_CREAT, S_IRWXU);
    int sz = read(fd_s, buf, sizeof(buf));
    write(fd_w, buf, sz);
    exit(0);
}

int main() {
    char buf[0x100];
    setbuf(stdout, NULL);
    fgets(buf, sizeof(buf), stdin);
    printf(buf);
    exit(1);
}