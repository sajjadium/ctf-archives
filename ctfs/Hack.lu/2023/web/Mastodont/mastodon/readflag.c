#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/sendfile.h>

void main() {
    struct stat buf;
    int fd = open("/flag", O_RDONLY);
    if (fd < 0) {
        return;
    }
    fstat(fd, &buf);
    sendfile(1, fd, 0, buf.st_size);
}