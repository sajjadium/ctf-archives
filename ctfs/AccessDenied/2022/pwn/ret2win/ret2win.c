#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win(){
    system("cat flag.txt");
}

void vuln(){
    char name[32];
    fgets(name, 64, stdin);
    puts(name);
}

void main() {
    alarm(0x20);
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    vuln();
}