#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void write(char what, long long int where, char* buf) {
    buf[where] = what;
}

char what() {
    char what;
    scanf("%c", &what);
    getchar();
    return what;
}

long long int where() {
    long long int where;
    scanf("%lld", &where);
    getchar();
    return where;
}

int main(void) {
	setvbuf(stdout, NULL, _IONBF, 0);
    int amount = 1;
    char buf[] = "Hello World!";
    while (amount--) {
        write(what(), where(), buf);
    }
    printf(buf);
}