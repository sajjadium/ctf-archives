#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_flag(void) {
    FILE* fp = fopen("flag.txt", "r");
    char flag[100];
    fgets(flag, sizeof(flag), fp);
    puts(flag);
}

int main(void) {
    // Ignore me
    setbuf(stdout, NULL);

    int flag = 0xaabdcdee;
    char buf[50] = {0};
	printf("Enter your favorite number: ");
	fgets(buf, 0x50, stdin);

    if(flag == 0x45454545){
        print_flag();
    }
    else{
        printf("Too bad! The flag is 0x%x\n", flag);
    }

    return 0;
}