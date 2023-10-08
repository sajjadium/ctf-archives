#include <stdio.h>

int main(int argc, char *argv[]) {
    seteuid(0);
    setegid(0);
    setuid(0);
    setgid(0);
    
    if(argc != 2) {
        puts("Usage: ./readflag --give-me-the-flag");
        return 1;
    }

    if (strcmp(argv[1], "--give-me-the-flag") != 0) {
        puts("You are not worthy");
        return 1;
    }

    char flag[256] = { 0 };
    FILE* fp = fopen("/flag", "r");
    if (!fp) {
        perror("fopen");
        return 1;
    }
    if (fread(flag, 1, 256, fp) < 0) {
        perror("fread");
        return 1;
    }
    puts(flag);
    fclose(fp);
    return 0;
}