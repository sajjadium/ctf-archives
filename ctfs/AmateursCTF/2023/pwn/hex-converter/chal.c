#include <stdio.h>
#include <stdlib.h>

int main()
{
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    int i = 0;

    char name[16];
    printf("input text to convert to hex: \n");
    gets(name);

    char flag[64];
    fgets(flag, 64, fopen("flag.txt", "r"));
    // TODO: PRINT FLAG for cool people ... but maybe later

    while (i < 16)
    {
        // the & 0xFF... is to do some typecasting and make sure only two characters are printed ^_^ hehe
        printf("%02X", (unsigned int)(name[i] & 0xFF));
        i++;
    }
    printf("\n");
}