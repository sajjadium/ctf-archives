#include <stdio.h>
#include <stdlib.h>

void flag(){
    char flag[128];
    
    FILE *file = fopen("flag.txt","r");
    if (!file) {
        puts("Error: missing flag.txt.");
        exit(1);
    }

    fgets(flag, 128, file);
    puts(flag);
}


int main(){
    setbuf(stdout, NULL);
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
    
    char cry[24];

    printf("Cry: ");

    gets(cry);
    return 0;
}