#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>

void handler(int sig) {
    fprintf(stderr, "looks like you crashed buddy\n");
    exit(0);
}

int main() {
    struct sigaction sa;
    memset(&sa, '\0', sizeof(sa));
    sa.sa_sigaction = &handler;
    sa.sa_flags = SA_SIGINFO;
    sigaction(SIGSEGV, &sa, NULL);

    char buf[128];

    puts("pwn me pls");
    gets(buf);
}