#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include "seccomp-bpf.h"

void activate_seccomp()
{
    struct sock_filter filter[] = {
        VALIDATE_ARCHITECTURE,
        EXAMINE_SYSCALL,
        ALLOW_SYSCALL(mprotect),
        ALLOW_SYSCALL(mmap),
        ALLOW_SYSCALL(munmap),
        ALLOW_SYSCALL(exit_group),
        ALLOW_SYSCALL(read),
        ALLOW_SYSCALL(write),
        ALLOW_SYSCALL(open),
        ALLOW_SYSCALL(close),
        ALLOW_SYSCALL(openat),
        ALLOW_SYSCALL(fstat),
        ALLOW_SYSCALL(brk),
        ALLOW_SYSCALL(newfstatat),
        ALLOW_SYSCALL(ioctl),
        ALLOW_SYSCALL(lseek),
        KILL_PROCESS,
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(struct sock_filter)),
        .filter = filter,
    };

    prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
    prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}


#include <gnu/libc-version.h>
#include <stdio.h>
#include <unistd.h>
int get_libc() {
    // method 1, use macro
    printf("%d.%d\n", __GLIBC__, __GLIBC_MINOR__);

    // method 2, use gnu_get_libc_version 
    puts(gnu_get_libc_version());

    // method 3, use confstr function
    char version[30] = {0};
    confstr(_CS_GNU_LIBC_VERSION, version, 30);
    puts(version);

    return 0;
}

#define NUM_STRINGS 10

typedef struct {
    size_t length;
	char * string;
} safe_string;

safe_string * data_storage[NUM_STRINGS];

void read_safe_string(int i) {
    safe_string * ptr = data_storage[i];
    if(ptr == NULL) {
        fprintf(stdout, "that item does not exist\n");
        fflush(stdout);
        return;
    }

    fprintf(stdout, "Sending %zu hex-encoded bytes\n", ptr->length);
    for(size_t j = 0; j < ptr->length; ++j) {
        fprintf(stdout, " %02x", (unsigned char) ptr->string[j]);
    }
    fprintf(stdout, "\n");
    fflush(stdout);
}

void free_safe_string(int i) {
    safe_string * ptr = data_storage[i];
    free(ptr->string);
    free(ptr);
}

void write_safe_string(int i) {
    safe_string * ptr = data_storage[i];
    if(ptr == NULL) {
        fprintf(stdout, "that item does not exist\n");
        fflush(stdout);
        return;
    }

    fprintf(stdout, "enter your string: ");
    fflush(stdout);

    read(STDIN_FILENO, ptr->string, ptr->length);
}

void create_safe_string(int i) {

    safe_string * ptr = malloc(sizeof(safe_string));

    fprintf(stdout, "How long is your safe_string: ");
    fflush(stdout);
    scanf("%zu", &ptr->length);

    ptr->string = malloc(ptr->length);
    data_storage[i] = ptr;

    write_safe_string(i);

}

// flag.txt
int main() {

    get_libc();
    activate_seccomp();

    int idx;
    int c;
    
    while(1){
        fprintf(stdout, "enter your command: ");
        fflush(stdout);
        while((c = getchar()) == '\n' || c == '\r');

        if(c == EOF) { return 0; }

        fprintf(stdout, "enter your index: ");
        fflush(stdout);
        scanf("%u", &idx);

        if((idx < 0) || (idx >= NUM_STRINGS)) {
            fprintf(stdout, "index out of range: %d\n", idx);
            fflush(stdout);
            continue;
        }

        switch(c) {
            case 'C':
                create_safe_string(idx);
                break;
            case 'F':
                free_safe_string(idx);
                break;
            case 'R':
                read_safe_string(idx);
                break;
            case 'W':
                write_safe_string(idx);
                break;
            case 'E':
                return 0;
        }
    
    }
}

