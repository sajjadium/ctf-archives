#include <stdio.h>
#include <ctype.h>
int init(){
    fclose(stderr);
    setvbuf(stdin,  0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
}
int check(char *s){
    char *ptr = s;
    while(*ptr!=0)
    {
        if(*ptr=='\n')
        {
            *ptr = 0; break;
        }
        if(isalpha(*ptr) || *ptr==' ')
            ptr++;
        else
        {
            puts("Hey Hacker! Welcome to CSAW'22!");
            exit(1);
        }
    }
    printf("Nice to meet you, %s! Welcome to CSAW'22!\n",s);
    return 1;
}
char * str1 = "My friend, what's your name?";
void readn(char * buf, size_t len){
    if(read(0,buf,len)<=0)
        exit(1);
    return ;
}
void vul(void *buf){
    size_t rdi = 0x00000000004015a3;
    size_t rsi = rdi-2;
    size_t rop[0x100]; 
    size_t ct = 0 ; 
    memset(rop,0,sizeof(rop));

    rop[ct++] = buf+0x70; // real ret address
    rop[ct++] = rdi;
    rop[ct++] = str1;
    rop[ct++] = puts;

    rop[ct++] = rsi;
    rop[ct++] = 0x100; // rsi
    rop[ct++] = 0x999; // Pad

    rop[ct++] = rdi; 
    rop[ct++] = buf; // rdi

    rop[ct++] = readn;

    rop[ct++] = rdi;
    rop[ct++] = buf;
    rop[ct++] = check;

    rop[ct++] = 0x40152d;

    rop[0x104] = rop;
    return ;
}
int main(){
    char buf[100];
    init();
    vul(buf);
}

