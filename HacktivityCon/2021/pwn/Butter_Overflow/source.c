#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/stat.h>

void give_flag();

void handler(int sig) {
    if (sig == SIGSEGV)
        give_flag();
}

void give_flag() {
    char *flag = NULL;
    FILE *fp = NULL;
    struct stat sbuf;

    if ((fp = fopen("flag.txt", "r")) == NULL) {
        puts("Could not open flag file.");
        exit(EXIT_FAILURE);
    }

    fstat(fileno(fp), &sbuf);

    flag = malloc(sbuf.st_size + 1);
    if (flag == NULL) {
        puts("Failed to allocate memory for the flag.");
        exit(EXIT_FAILURE);
    }

    fread(flag, sizeof(char), sbuf.st_size, fp);
    flag[sbuf.st_size] = '\0';

    puts(flag);

    fclose(fp);
    free(flag);

    exit(EXIT_SUCCESS);
}

int main() {
    char buffer[0x200];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    signal(SIGSEGV, handler);

    puts("How many bytes does it take to overflow this buffer?");
    gets(buffer);

    return 0;
}
