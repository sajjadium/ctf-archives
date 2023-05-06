// gcc -fno-stack-protector -no-pie -z execstack
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init_proc() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

void read_string(char* buf, size_t length) {
    ssize_t n;
    n = read(STDIN_FILENO, buf, length);
    if (n == -1)
        exit(1);
    buf[n] = '\0';
}

int main(void) {
    char buf[0x100]; 
    init_proc();
    printf("Hello CTF Players!\nThis is a warmup challenge for pwnable.\nDo you know about Format String Attack(FSA) and write the exploit code?\nPlease pwn me!\n");
    while (1) {
        printf("> ");
        read_string(buf, 0x100);
        if (buf[0] == 'q')
            break;
        printf(buf);
    }
    return 0;
}