#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <malloc.h>
#include <assert.h>

char* buf;
void get(int num)
{
        fgets(buf, num, stdin);
}

int main()
{

       char sbuf[0x10];
       buf = sbuf;

       get(0x10);

       ((void (*)())buf)();  

       exit(-1);
}