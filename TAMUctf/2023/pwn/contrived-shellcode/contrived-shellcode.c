#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned char whitelist[] = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0d\x0e\x0f";

void check(unsigned char* code, int len) {
    for (int i = 0; i < len; i++) {
        if (memchr(whitelist, code[i], sizeof(whitelist)) == NULL) {
            printf("Oops, shellcode contains blacklisted character %02X at offset %d.\n", code[i], i);
            exit(-1);
        }
    }
}

int main() {
    unsigned char* code = mmap(NULL, 0x1000, PROT_EXEC|PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);

    int len = read(0, code, 0x100);

    if (len > 0) {
        if (code[len - 1] == '\n') {
            code[len - 1] = '\0';
        }
        check(code, len); 
        ((void (*)())(code))();
    }
}
