#include <stdio.h>
#include <unistd.h>

void upkeep() {
    // Not related to the challenge, just some stuff so the remote works correctly
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win() {
    char* argv[] = {"/bin/cat", "flag.txt", NULL};
    execve(argv[0], argv, NULL);
}

void lose() {
    char* argv[] = {"/bin/echo", "loser", NULL};
    execve(argv[0], argv, NULL);
}

void vuln() {
    char buf[010];
    printf("Interaction pls: ");
    read(0, buf, 10);
}

int main() {
    upkeep();
    void* func_ptrs[] = {lose, win};
    printf("All my functions are being stored at %p\n", func_ptrs);
    
    vuln();
    
    void (*poggers)() = func_ptrs[0];
    poggers();
}
