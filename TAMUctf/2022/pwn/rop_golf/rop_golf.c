#include <stdio.h>
#include <unistd.h>

void vuln() {
    char buf[32];
    read(0, buf, 72);
}

void main() {
    setvbuf(stdout, 0, 2, 0);
    puts("hi!");
    vuln();
}
