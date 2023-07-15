#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>
#include <unistd.h>
#include <sys/mman.h>

struct MmapArgs {
    uint64_t * addr;
    uint64_t length;
    int protection;
    int flags;
    int fd;
    uint64_t offset;
};

extern struct MmapArgs mmap_args();

int main () {
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    struct MmapArgs args = mmap_args();
    char * buf = mmap(args.addr, args.length, args.protection, MAP_PRIVATE | MAP_ANON, args.fd, args.offset);
    if (buf < 0) {
        perror("failed to mmap");
    }

    read(0, buf, 0x1000);

    printf("> ");
    int op;
    if (scanf("%d", &op) == 1) {
        switch (op) {
            case 0:
                ((void (*)(void))buf)();
                break;
            case 1:
                puts(buf);
                break;
        }
    }
}
