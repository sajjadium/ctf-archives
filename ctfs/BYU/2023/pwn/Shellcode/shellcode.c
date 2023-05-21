#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

#define MAP_ANONYMOUS 0x20

__attribute__((constructor)) void flush_buf() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main() {
    // create memory for shellcode to reside in
    mmap((char *)0x777777000, 71, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_SHARED|MAP_ANONYMOUS, -1, 0);

    // set first 51 bytes to 0s
    memset((char *)0x777777000, 0x00, 51);

    // get first 10 bytes of shellcode
    char shellcode_one[10];
    puts("Enter first 10 bytes of shellcode: ");
    read(0, shellcode_one, 10);
    memcpy((char *)0x777777000, shellcode_one, 10);

    // get second 10 bytes of shellcode
    char shellcode_two[10];
    puts("Enter second 10 bytes of shellcode: ");
    read(0, shellcode_two, 10);
    memcpy((char *)0x777777020, shellcode_two, 10);

    // get third 10 bytes of shellcode
    char shellcode_three[10];
    puts("Enter third 10 bytes of shellcode: ");
    read(0, shellcode_three, 10);
    memcpy((char *)0x777777040, shellcode_three, 10);

    // get last 10 bytes of shellcode
    char shellcode_four[10];
    puts("Enter last 10 bytes of shellcode: ");
    read(0, shellcode_four, 10);
    memcpy((char *)0x777777060, shellcode_four, 10);

    // call shellcode
    ((void (*)())0x777777000)();
    return 0;
}