#include <stdio.h>

int main() {
    FILE *fp;
    char flag[100];

    fp = fopen("/flag", "r");
    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    fgets(flag, 100, fp);
    printf("%s\n", flag);

    fclose(fp);
    return 0;
}