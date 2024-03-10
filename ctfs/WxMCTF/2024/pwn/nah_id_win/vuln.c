#include <stdio.h>
#include <stdlib.h>

int vuln() {
    char buf[0x20];
    printf("My cursed technique is revealing libc... %p\n",printf);
    gets(buf);
    if(__builtin_return_address(0) < 0x90000000) {
        return 0;
    }
    printf("NAH I'D WIN!\n");
    exit(0);
}
int main() {
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    vuln();
    return 0;
}
