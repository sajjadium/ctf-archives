#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

#define MAX_STR_LEN 128

typedef struct req {
    unsigned char len;
    char shift;
    char buf[MAX_STR_LEN];
} shm_req_t;

void shift_str(char* str, int len, char shift, char out[MAX_STR_LEN]) {
    for(int i = 0; i < len; i++) {
        out[i] = str[i] + shift;
    }
    out[len] = '\0';
}

void win() {
    char flag[0x100];
    int fd = open("/home/ctf/chal/flag.txt", O_RDONLY);
    read(fd, flag, 0x100);
    printf("%s\n", flag);
}

int main(int argc, char** argv) {
    char out[MAX_STR_LEN];

    if(argc != 2) {
        fprintf(stderr, "Usage: %s <name>\n", argv[0]);
        exit(1);
    }

    char* name = argv[1];
    mode_t old_umask = umask(0);
    int fd = shm_open(name, O_CREAT | O_RDWR | O_TRUNC | O_EXCL, S_IRWXU | S_IRWXG | S_IRWXO);
    umask(old_umask);
    if(fd == -1) {
        fprintf(stderr, "shm_open error");
        exit(1);
    }

    if(ftruncate(fd, sizeof(shm_req_t)) == -1) {
        fprintf(stderr, "ftruncate error");
        exit(1);
    }

    shm_req_t* shm_req = mmap(NULL, sizeof(shm_req_t), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if(shm_req == MAP_FAILED) {
        fprintf(stderr, "mmap error");
        exit(1);
    }

    shm_req->len = -1;
    shm_req->shift = 0;

    usleep(10000);
    close(fd);
    shm_unlink(name);

    while(1) {
        if(shm_req->len < 0 || shm_req->len > MAX_STR_LEN) {
            continue;
        }

        if(shm_req->len == 0) {
            return 0;
        }

        shift_str(shm_req->buf, shm_req->len, shm_req->shift, out);
        printf("%s\n", out);
    }
}
