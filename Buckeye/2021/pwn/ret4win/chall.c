#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void ignore_me() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void win(int arg0, int arg1, int arg2, int arg3, int arg4, int arg5) {
    char* cmd = "cat flag.txt";
    if (arg0 == 0xdeadbeef && arg1 == 0xcafebabe && arg2 == 0xbeeeeeef &&
        arg3 == 0x13333337 && arg4 == 0x12345678 && arg5 == 0xabcdefed) {
        system(cmd);
    }
}

void vuln() {
    char buf[32];
    puts("Please leave a message at the tone: **beep**");
    read(0, buf, 32 + 8 + 16);
    close(0);
}

int main() {
    vuln();
    return 0;
}
