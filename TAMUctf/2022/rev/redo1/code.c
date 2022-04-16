#include <stdio.h>
#include <string.h>

#define STR_LEN 34

#define EXIT printf("Sorry that's not the flag\n"); return 1;
#define SUCCESS printf("THAT'S THE FLAG!\n"); return 0;
#define PARAMS printf("Usage: ./code <flag>\n"); return 1;
#define POINTER char* flag = (char*)(&a);

int main(int argc, char** argv) 
{
    int a[] = {0x65676967,0x00000000,0x34427b6d,0x5f433153,0x616c5f43,0x00000000,0x4175476e,0x525f4567,0x00000000,0x78305f45,0x53414c47,0x00007d53};

    if(argc != 2){ PARAMS }
    if(strlen(argv[1]) != STR_LEN){ EXIT }

    POINTER

    for(int i = 0; i < STR_LEN; i++)
    {
        int idx = i;
        if(i >= 4 && i <= 15){ idx += 4; }
        if(i >= 16 && i <= 23){ idx += 8; }
        if(i > 23){ idx += 12; }

        if(argv[1][i] != flag[idx]){ EXIT }
    }

    SUCCESS
}
